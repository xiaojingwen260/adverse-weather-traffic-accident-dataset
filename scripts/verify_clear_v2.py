# -*- coding: utf-8 -*-
"""verify_clear_v2.py — 540 条 clear 事故下载验收 + MAD 峰复核

验收项：
 1) mp4 数量=540、文件名唯一、无 0 字节
 2) 每条 ffprobe 验证：25 帧 / 1280x720 / 5fps / 可解码（帧数=25）
 3) md5 重复检查（跨文件）
 4) manifest.json 与实际文件 1:1 对应（video_id/path/weather/scenario/frames/collision_frame/town）
 5) MAD 峰：对 25 帧 JPG 相邻灰度差 argmax（peak_frame=argmax+1），映射碰撞实际位置，
    峰<18 → quality_flag=['early_motion_peak']、prediction_eligible=False（保留用于检测）
输出：
   reports/clear_verify.json        （每条 peak_frame_mad + 质量标记，供 build_master.py 使用）
   reports/clear_download_acceptance.json （本验收报告）
"""
import json, os, sys, subprocess, hashlib, time
import cv2
import numpy as np

ROOT = r'D:\dataset\carla_clear_out_v2'
MANIFEST = os.path.join(ROOT, 'manifest.json')
FRAMES_OUT = r'D:\dataset_final_export\dataset_final\frames\CARLA_ACCIDENT'
REPORTS = r'D:\dataset_final_export\dataset_final\reports'
FFPROBE = r'D:\workbuddyworkplatform\2026-09-29-dataset-v2\tools\ffmpeg\ffmpeg-9.0.2-essentials_build\bin\ffprobe.exe'


def ffprobe_stream(path):
    r = subprocess.run([FFPROBE, '-v', 'error', '-select_streams', 'v:0',
                        '-show_entries', 'stream=codec_name,width,height,avg_frame_rate,nb_frames',
                        '-of', 'json', path], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return None, r.stderr[:300]
    import json as j
    try:
        st = j.loads(r.stdout)['streams'][0]
        num, den = st['avg_frame_rate'].split('/')
        fps = float(num) / float(den) if float(den) else None
        return {'codec': st.get('codec_name'), 'width': st.get('width'),
                'height': st.get('height'), 'fps': fps,
                'nb_frames': st.get('nb_frames')}, None
    except Exception as e:
        return None, repr(e)[:300]


def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def extract_frames(vid, src_mp4, dst_dir):
    """cv2 顺序读帧 -> 000001..000025.jpg（q95，不 resize）"""
    os.makedirs(dst_dir, exist_ok=True)
    cap = cv2.VideoCapture(src_mp4)
    if not cap.isOpened():
        return 0, 'open fail'
    n = 0
    try:
        while True:
            okk, fr = cap.read()
            if not okk:
                break
            if not cv2.imwrite(os.path.join(dst_dir, '%06d.jpg' % (n + 1)), fr,
                               [cv2.IMWRITE_JPEG_QUALITY, 95]):
                return n, 'write fail'
            n += 1
    except Exception as e:
        return n, repr(e)[:200]
    finally:
        cap.release()
    return n, None


def main():
    if not os.path.exists(MANIFEST):
        print('FATAL: 未找到 %s —— 先完成下载' % MANIFEST)
        sys.exit(2)
    man = json.load(open(MANIFEST, encoding='utf-8'))
    print('manifest entries:', len(man))

    files = []
    for wd in os.listdir(ROOT):
        d = os.path.join(ROOT, wd)
        if os.path.isdir(d):
            files += [os.path.join(d, f) for f in os.listdir(d) if f.endswith('.mp4')]
    mp4_by_name = {os.path.basename(f): f for f in files}
    print('mp4 files:', len(files))

    issues = []
    # 1) 数量/唯一/0 字节
    if len(files) != 540:
        issues.append('mp4 总数=%d 应=540' % len(files))
    if len(mp4_by_name) != len(files):
        issues.append('mp4 重名 %d' % (len(files) - len(mp4_by_name)))
    zeros = [f for f in files if os.path.getsize(f) == 0]
    if zeros:
        issues.append('0 字节 %d 条: %s' % (len(zeros), zeros[:5]))

    # 2) 每条 ffprobe
    probe_ok = probe_bad = 0
    probe_fails = []
    for f in files:
        st, err = ffprobe_stream(f)
        if st is None:
            probe_bad += 1
            probe_fails.append({'file': f, 'issue': 'ffprobe失败: ' + (err or '')})
        elif (st['width'], st['height'], st['fps'],
              int(st['nb_frames']) if st.get('nb_frames') else None) != (1280, 720, 5.0, 25):
            probe_bad += 1
            probe_fails.append({'file': f, 'issue': '规格不符: %r' % st})
        else:
            probe_ok += 1
    if probe_bad:
        issues.append('ffprobe 规格不符 %d 条' % probe_bad)

    # 3) md5 重复
    sums = {}
    dup = []
    for f in files:
        m = md5(f)
        if m in sums:
            dup.append((sums[m], os.path.basename(f)))
        else:
            sums[m] = os.path.basename(f)
    if dup:
        issues.append('md5 重复 %d 对: %s' % (len(dup), dup[:5]))

    # 4) manifest 1:1
    man_names = {}
    for m in man:
        base = os.path.basename(m['path'])
        man_names[base] = m
    missing_files = [b for b in man_names if b not in mp4_by_name]
    extra_files = [b for b in mp4_by_name if b not in man_names]
    if missing_files or extra_files:
        issues.append('manifest 与实际 1:1 不符: missing=%d extra=%d'
                      % (len(missing_files), len(extra_files)))
    # manifest 字段校验
    man_bad = []
    for m in man:
        if m.get('weather') != 'clear' or m.get('scenario') not in ('rear_end', 'side_impact', 'pedestrian') \
                or m.get('frames') != 25 or m.get('collision_frame') != 20:
            man_bad.append(m.get('video_id'))
    if man_bad:
        issues.append('manifest 字段异常 %d: %s' % (len(man_bad), man_bad[:5]))

    # 5) 提取帧 + MAD 峰
    peaks = {}
    extract_fails = []
    t0 = time.time()
    for i, m in enumerate(man):
        vid = m['video_id']
        src = mp4_by_name[os.path.basename(m['path'])]
        dst = os.path.join(FRAMES_OUT, vid)
        n, err = extract_frames(vid, src, dst)
        if err is not None or n != 25:
            extract_fails.append({'video_id': vid, 'issue': err or 'frame_count=%d' % n})
            continue
        # MAD 峰
        imgs = []
        for k in range(1, 26):
            im = cv2.imread(os.path.join(dst, '%06d.jpg' % k), cv2.IMREAD_GRAYSCALE)
            if im is None:
                imgs = None
                break
            imgs.append(im.astype(np.float32))
        if imgs is None:
            extract_fails.append({'video_id': vid, 'issue': '帧不可读'})
            continue
        diffs = [float(np.abs(imgs[k + 1] - imgs[k]).mean()) for k in range(24)]
        peak = int(np.argmax(diffs)) + 1
        rec = {'video_id': vid, 'peak_frame_mad': peak, 'mad_max': diffs[peak - 1],
               'weather': m['weather'], 'scenario': m['scenario'], 'town': m['town'],
               'collision_frame': m.get('collision_frame'),
               'quality_flag': [], 'prediction_eligible': True}
        if peak < 18:
            rec['quality_flag'] = ['early_motion_peak']
            rec['prediction_eligible'] = False
        peaks[vid] = rec
        if (i + 1) % 100 == 0:
            print('  extract+peak %d/%d %.0fs' % (i + 1, len(man), time.time() - t0), flush=True)

    from collections import Counter
    dist = Counter(v['peak_frame_mad'] for v in peaks.values())
    early = [v['video_id'] for v in peaks.values() if v['peak_frame_mad'] < 18]
    print('extract fails:', len(extract_fails), extract_fails[:5])
    print('peak dist:', {str(k): v for k, v in sorted(dist.items())})
    print('early_peak(<18):', len(early), early[:10])

    result = {
        'accepted': len(files) == 540 and not issues and not extract_fails and not probe_fails,
        'mp4_total': len(files),
        'probe_ok': probe_ok, 'probe_bad': probe_bad,
        'extract_ok': len(peaks), 'extract_fail': len(extract_fails),
        'issues': issues,
        'probe_fails': probe_fails[:20],
        'extract_fails': extract_fails,
        'duplicate_md5_pairs': dup,
        'manifest_entries': len(man),
        'peak_distribution': {str(k): v for k, v in sorted(dist.items())},
        'early_peak_count': len(early),
        'early_peak_videos': early,
    }
    os.makedirs(REPORTS, exist_ok=True)
    json.dump(result, open(os.path.join(REPORTS, 'clear_download_acceptance.json'),
                           'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump({'items': list(peaks.values())},
              open(os.path.join(REPORTS, 'clear_verify.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('accepted:', result['accepted'])
    print('->', os.path.join(REPORTS, 'clear_download_acceptance.json'))
    print('->', os.path.join(REPORTS, 'clear_verify.json'))


if __name__ == '__main__':
    main()
