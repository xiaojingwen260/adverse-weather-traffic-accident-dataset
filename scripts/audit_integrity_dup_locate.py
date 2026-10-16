# -*- coding: utf-8 -*-
"""audit_integrity_dup_locate.py — 定位 audit_integrity 发现的 2 组重复帧 MD5 的样本归属

全量重扫 MD5（只记录重复 md5 的文件路径与所属样本/帧名/split），
输出 reports/audit_integrity_dup_locate.json + .md
"""
import json
import os
import hashlib
import collections
import datetime

ROOT = r'D:\dataset_final_export\dataset_final'
M = os.path.join(ROOT, 'manifests', 'dataset_master.json')
R = os.path.join(ROOT, 'reports')


def md5file(p, bufsize=1 << 20):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        while True:
            b = f.read(bufsize)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main():
    m = json.load(open(M, encoding='utf-8'))
    seen = collections.defaultdict(list)
    t0 = datetime.datetime.now()
    for i, it in enumerate(m):
        d = os.path.join(ROOT, it['frame_dir'])
        for f in sorted(x for x in os.listdir(d) if x.lower().endswith('.jpg')):
            fp = os.path.join(d, f)
            h = md5file(fp)
            seen[h].append({'sample_id': it['sample_id'], 'split': it['split'],
                            'frame_dir': it['frame_dir'], 'frame': f, 'abs': fp})
        if (i + 1) % 1000 == 0:
            print('progress %d/%d (%.0fs)' % (i + 1, len(m),
                  (datetime.datetime.now() - t0).total_seconds()), flush=True)
    dups = {h: v for h, v in seen.items() if len(v) > 1}
    res = {
        'audit_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'elapsed_sec': (datetime.datetime.now() - t0).total_seconds(),
        'duplicate_md5_groups': len(dups),
        'details': dups,
    }
    json.dump(res, open(os.path.join(R, 'audit_integrity_dup_locate.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)
    print('DONE dup_locate: groups=%d' % len(dups))
    for h, v in dups.items():
        print(h, v)


if __name__ == '__main__':
    main()
