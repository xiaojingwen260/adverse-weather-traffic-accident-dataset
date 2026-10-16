# -*- coding: utf-8 -*-
"""test_loader_delivery.py — 加载器全量遍历验收

对 dataset_master.json 全量（含 540 clear）逐条经加载器读取：
  - 相对路径可解析
  - 25 帧全部可读（失败计入）
输出：reports/loader_delivery_result.json
"""
import json, os, time, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'loaders'))
from dataset_loader import DatasetFinal

ROOT = r'D:\dataset_final_export\dataset_final'
REPORTS = os.path.join(ROOT, 'reports')


def main():
    ds = DatasetFinal(ROOT)
    items = ds.master
    print('master items:', len(items))
    t0 = time.time()
    errors = []
    ok = 0
    for i, it in enumerate(items):
        frames, rec = ds.load_sample(it)
        if frames is None or len(frames) != rec['frame_count']:
            errors.append({'sample_id': it['sample_id'], 'issue': 'frames=%s' % (len(frames) if frames else 0)})
        else:
            ok += 1
        if (i + 1) % 1000 == 0:
            print('  %d/%d %.0fs' % (i + 1, len(items), time.time() - t0), flush=True)
    result = {
        'total': len(items),
        'iterated': ok,
        'errors': len(errors),
        'error_items': errors[:50],
        'elapsed_s': round(time.time() - t0, 1),
    }
    os.makedirs(REPORTS, exist_ok=True)
    json.dump(result, open(os.path.join(REPORTS, 'loader_delivery_result.json'),
                           'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('DONE iterated=%d/%d errors=%d %.0fs' % (ok, len(items), len(errors), time.time() - t0))
    print('->', os.path.join(REPORTS, 'loader_delivery_result.json'))


if __name__ == '__main__':
    main()
