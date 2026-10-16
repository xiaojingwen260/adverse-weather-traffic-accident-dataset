# -*- coding: utf-8 -*-
"""audit_integrity.py — v1.0 最终验收审计：文件完整性（独立复核，不沿用旧结论）

双向核对：master 4971 条 ↔ frames 实际文件。
  1) 每条 frame_dir 存在、恰 25 张 jpg、非零大小、全部可解码（cv2.imread 全量）
  2) 全量逐帧 MD5（完全重复帧）+ 每条 25 帧序列 MD5 拼接哈希（整条重复）
  3) 未登记目录（frames 下有、master 无）+ 登记目录内多余/缺失文件
  4) sample_id 唯一性、frame_dir 唯一性
输出：reports/audit_integrity.json + reports/audit_integrity.md
"""
import json
import os
import hashlib
import collections
import datetime

ROOT = r'D:\dataset_final_export\dataset_final'
M = os.path.join(ROOT, 'manifests', 'dataset_master.json')
FR = os.path.join(ROOT, 'frames')
R = os.path.join(ROOT, 'reports')
OUT_JSON = os.path.join(R, 'audit_integrity.json')
OUT_MD = os.path.join(R, 'audit_integrity.md')


def md5_file(p, chunk=1 << 20):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main():
    import cv2
    m = json.load(open(M, encoding='utf-8'))
    t0 = datetime.datetime.now()

    # 1) 逐条检查 + 全量 MD5 + 全量解码
    per_sample = {}
    frame_md5 = collections.Counter()   # 逐帧 MD5
    dup_frames = []                     # 完全重复帧对（跨样本）
    missing = []
    empty = []
    undecodable = []
    wrong_count = []
    total_jpg = 0
    for i, it in enumerate(m):
        d = os.path.join(ROOT, it['frame_dir'])
        sid = it['sample_id']
        if not os.path.isdir(d):
            missing.append({'sample_id': sid, 'frame_dir': it['frame_dir']})
            per_sample[sid] = {'status': 'dir_missing'}
            continue
        jpgs = [f for f in os.listdir(d) if f.lower().endswith('.jpg')]
        if len(jpgs) != 25:
            wrong_count.append({'sample_id': sid, 'jpg_count': len(jpgs)})
        seq_hashes = []
        for jp in sorted(jpgs):
            p = os.path.join(d, jp)
            sz = os.path.getsize(p)
            total_jpg += 1
            if sz == 0:
                empty.append({'sample_id': sid, 'file': jp})
            h = md5_file(p)
            frame_md5[h] += 1
            seq_hashes.append(h)
            img = cv2.imread(p, cv2.IMREAD_COLOR)
            if img is None:
                undecodable.append({'sample_id': sid, 'file': jp})
        per_sample[sid] = {
            'jpg_count': len(jpgs),
            'seq_md5': hashlib.md5(','.join(seq_hashes).encode()).hexdigest(),
            'total_bytes': sum(os.path.getsize(os.path.join(d, j)) for j in jpgs),
        }
        if (i + 1) % 500 == 0:
            print('progress %d/%d' % (i + 1, len(m)), flush=True)

    # 2) 逐条重复（25 帧序列完全一致）
    seq_groups = collections.defaultdict(list)
    for sid, info in per_sample.items():
        if 'seq_md5' in info:
            seq_groups[info['seq_md5']].append(sid)
    dup_samples = {h: v for h, v in seq_groups.items() if len(v) > 1}

    # 逐帧重复（跨样本、同帧内容）
    dup_frames = [{ 'md5': h, 'count': c } for h, c in frame_md5.items() if c > 1]
    dup_frame_instances = sum(c - 1 for c in frame_md5.values() if c > 1)

    # 3) 未登记目录
    registered = {it['frame_dir'] for it in m}
    orphan_dirs = []
    for src in os.listdir(FR):
        sdir = os.path.join(FR, src)
        if not os.path.isdir(sdir):
            continue
        for sub in os.listdir(sdir):
            rel = os.path.join('frames', src, sub)
            if not os.path.isdir(os.path.join(sdir, sub)):
                continue
            if rel.replace('/', '\\') not in registered and rel not in registered:
                n = len([f for f in os.listdir(os.path.join(sdir, sub)) if f.lower().endswith('.jpg')])
                orphan_dirs.append({'rel_dir': rel, 'jpg_count': n})

    # 4) 唯一性
    ids = [it['sample_id'] for it in m]
    dup_ids = sorted({x for x in ids if ids.count(x) > 1})
    dirs = [it['frame_dir'] for it in m]
    dup_dirs = sorted({x for x in dirs if dirs.count(x) > 1})

    result = {
        'audit_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'elapsed_sec': (datetime.datetime.now() - t0).total_seconds(),
        'total_samples': len(m),
        'total_jpg_scanned': total_jpg,
        'valid_samples': len(per_sample) - len(missing),
        'missing_dir_samples': missing,
        'missing_dir_count': len(missing),
        'empty_file_count': len(empty),
        'undecodable_count': len(undecodable),
        'undecodable_files': undecodable[:100],
        'wrong_jpg_count_samples': wrong_count,
        'orphan_dir_count': len(orphan_dirs),
        'orphan_dirs': orphan_dirs[:100],
        'duplicate_sample_id': len(dup_ids),
        'duplicate_sample_ids': dup_ids,
        'duplicate_frame_dir': len(dup_dirs),
        'duplicate_frame_dir_values': dup_dirs,
        'duplicate_frame_md5_groups': len(dup_frames),
        'duplicate_frame_instance_excess': dup_frame_instances,
        'duplicate_frame_groups': dup_frames[:100],
        'duplicate_sample_sequence_groups': len(dup_samples),
        'duplicate_sample_sequences': {h: v for h, v in list(dup_samples.items())[:50]},
        'conclusion': 'PASS' if (not missing and not undecodable and not dup_ids and
                                 not dup_dirs and not dup_samples and not wrong_count) else 'FAIL',
    }
    json.dump(result, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    lines = ['# v1.0 最终验收审计 · 文件完整性', '',
             '审计时间：%s（耗时 %.0fs）' % (result['audit_time'], result['elapsed_sec']), '',
             '| 项 | 结果 |', '|---|---|',
             '| 总样本 | %d |' % len(m),
             '| 扫描 JPG | %d |' % total_jpg,
             '| 有效样本（目录存在） | %d |' % result['valid_samples'],
             '| 缺失目录 | %d |' % len(missing),
             '| 空文件 | %d |' % len(empty),
             '| 坏解码 | %d |' % len(undecodable),
             '| 帧数≠25 的样本 | %d |' % len(wrong_count),
             '| 未登记目录 | %d |' % len(orphan_dirs),
             '| 重复 sample_id | %d |' % len(dup_ids),
             '| 重复 frame_dir | %d |' % len(dup_dirs),
             '| 完全重复帧组（MD5） | %d（额外实例 %d） |' % (len(dup_frames), dup_frame_instances),
             '| 整条重复（25 帧序列） | %d 组 |' % len(dup_samples),
             '| 结论 | **%s** |' % result['conclusion'], '']
    if missing:
        lines += ['### 缺失目录清单', '', '```']
        lines += [x['frame_dir'] for x in missing]
        lines += ['```', '']
    if undecodable:
        lines += ['### 坏解码清单（前 100）', '', '```']
        lines += ['%s %s' % (x['sample_id'], x['file']) for x in undecodable[:100]]
        lines += ['```', '']
    if orphan_dirs:
        lines += ['### 未登记目录（前 100）', '', '```']
        lines += ['%s (%d jpg)' % (x['rel_dir'], x['jpg_count']) for x in orphan_dirs[:100]]
        lines += ['```', '']
    if dup_samples:
        lines += ['### 整条重复组', '', '```']
        for h, v in dup_samples.items():
            lines += ['seq_md5=%s: %s' % (h, ', '.join(v))]
        lines += ['```', '']
    open(OUT_MD, 'w', encoding='utf-8').write('\n'.join(lines))
    print('DONE integrity: samples=%d jpg=%d missing=%d undecodable=%d empty=%d wrongcount=%d '
          'orphan=%d dup_id=%d dup_seq_groups=%d dup_frame_groups=%d excess=%d' % (
              len(m), total_jpg, len(missing), len(undecodable), len(empty), len(wrong_count),
              len(orphan_dirs), len(dup_ids), len(dup_samples), len(dup_frames), dup_frame_instances))


if __name__ == '__main__':
    main()
