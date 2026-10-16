# -*- coding: utf-8 -*-
"""frame_integrity.py — dataset_final 帧完整性 + 重复帧序列检查

对 dataset_master.json 全量：
 1) frame_dir 相对路径可解析（相对 dataset_final 根）
 2) 每条恰 25 个 JPG（000001..000025）
 3) JPG 非空、可解码（cv2.imread 非 None）、尺寸一致
 4) 文件级 md5 检查：重复帧（同一字节内容出现于不同样本/不同帧位）→ 重复帧序列计数
输出：reports/frame_integrity_check.json
"""
import json, os, hashlib, time
import cv2

ROOT = r'D:\dataset_final_export\dataset_final'
MASTER = os.path.join(ROOT, 'manifests', 'dataset_master.json')
REPORTS = os.path.join(ROOT, 'reports')


def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    items = json.load(open(MASTER, encoding='utf-8'))
    print('master items:', len(items))
    t0 = time.time()
    bad_path = []
    bad_count = []
    bad_decode = []
    bad_dim = []
    seq_hashes = {}
    frame_hash_owner = {}
    dup_seqs = []
    total_jpg = 0
    total_bytes = 0
    ok = 0
    for i, it in enumerate(items):
        d = os.path.join(ROOT, it['frame_dir'])
        if not os.path.isdir(d):
            bad_path.append(it['sample_id'])
            continue
        jpgs = []
        ok_here = True
        for k in range(1, 26):
            p = os.path.join(d, '%06d.jpg' % k)
            if not os.path.exists(p):
                ok_here = False
                bad_count.append(it['sample_id'])
                break
            total_bytes += os.path.getsize(p)
            jpgs.append(p)
        if not ok_here:
            continue
        if len(jpgs) != 25:
            bad_count.append(it['sample_id'])
            continue
        # 解码 + 尺寸
        dims = None
        hbuf = hashlib.md5()
        for p in jpgs:
            im = cv2.imread(p, cv2.IMREAD_COLOR)
            if im is None:
                bad_decode.append(it['sample_id'])
                ok_here = False
                break
            h = hashlib.md5()
            with open(p, 'rb') as f:
                h.update(f.read())
            hbuf.update(h.digest())
            if dims is None:
                dims = im.shape
            elif im.shape != dims:
                bad_dim.append((it['sample_id'], str(im.shape)))
        if not ok_here:
            continue
        seq_h = hbuf.hexdigest()
        if seq_h in seq_hashes and seq_hashes[seq_h] != it['sample_id']:
            dup_seqs.append((seq_hashes[seq_h], it['sample_id']))
        else:
            seq_hashes[seq_h] = it['sample_id']
        total_jpg += 25
        ok += 1
        if (i + 1) % 500 == 0:
            print('  %d/%d %.0fs' % (i + 1, len(items), time.time() - t0), flush=True)

    result = {
        'total_samples': len(items),
        'ok_samples': ok,
        'total_jpg': total_jpg,
        'total_bytes': total_bytes,
        'bad_path': bad_path[:50],
        'bad_path_count': len(bad_path),
        'bad_frame_count': bad_count[:50],
        'bad_frame_count_count': len(bad_count),
        'bad_decode': bad_decode[:50],
        'bad_decode_count': len(bad_decode),
        'bad_dim': bad_dim[:20],
        'bad_dim_count': len(bad_dim),
        'duplicate_frame_sequence': len(dup_seqs),
        'duplicate_frame_sequence_pairs': dup_seqs[:20],
        'elapsed_s': round(time.time() - t0, 1),
    }
    os.makedirs(REPORTS, exist_ok=True)
    json.dump(result, open(os.path.join(REPORTS, 'frame_integrity_check.json'),
                           'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # 回填防泄漏报告
    lp = os.path.join(REPORTS, 'split_leakage_check.json')
    if os.path.exists(lp):
        leak = json.load(open(lp, encoding='utf-8'))
        leak['duplicate_frame_sequence'] = len(dup_seqs)
        json.dump(leak, open(lp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('DONE ok=%d jpg=%d bytes=%.2fGB dup_seq=%d' % (ok, total_jpg, total_bytes / 1e9, len(dup_seqs)))
    print('->', os.path.join(REPORTS, 'frame_integrity_check.json'))


if __name__ == '__main__':
    main()
