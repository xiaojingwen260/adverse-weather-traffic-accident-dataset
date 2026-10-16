# -*- coding: utf-8 -*-
"""final_reverify.py — 冻结前最终复验（修正指令第四项，全部以实际文件为准）

逐项读取 manifests/*.json 与 reports/*.json，输出最终核验清单，写入 reports/final_reverify.json。
不做任何修改；若任一项失败，conclusion=FAIL 并列出失败项。
"""
import json
import os
import datetime

ROOT = r'D:\dataset_final_export\dataset_final'
M = os.path.join(ROOT, 'manifests')
R = os.path.join(ROOT, 'reports')


def load(p):
    return json.load(open(p, encoding='utf-8'))


def main():
    master = load(os.path.join(M, 'dataset_master.json'))
    train = load(os.path.join(M, 'train.json'))
    val = load(os.path.join(M, 'val_real.json'))
    test = load(os.path.join(M, 'test_real.json'))
    reserve = load(os.path.join(M, 'reserve.json'))
    leak = load(os.path.join(R, 'split_leakage_check.json'))
    integ = load(os.path.join(R, 'frame_integrity_check.json'))
    loader = load(os.path.join(R, 'loader_delivery_result.json'))
    dist = load(os.path.join(R, 'final_distribution.json'))
    label = load(os.path.join(R, 'label_logic_check.json'))

    rows = []
    def row(name, ok, value, src):
        rows.append({'item': name, 'pass': bool(ok), 'value': value, 'source': src})

    row('dataset_master = 4971', len(master) == 4971, len(master),
        'manifests/dataset_master.json')
    row('train + val_real + test_real + reserve = 4971',
        len(train) + len(val) + len(test) + len(reserve) == len(master) == 4971,
        '%d+%d+%d+%d = %d' % (len(train), len(val), len(test), len(reserve), len(master)),
        'manifests/{train,val_real,test_real,reserve}.json')

    syn = sum(1 for x in train if x['domain'] == 'synthetic')
    real = sum(1 for x in train if x['domain'] == 'real')
    tr = dist['train_ratio']
    row('train 合成 80% / 真实 20%（±0.5%）',
        abs(tr['syn_pct'] - 80.0) <= 0.5 and abs(tr['real_pct'] - 20.0) <= 0.5,
        '合成 %.3f%%（%d） / 真实 %.3f%%（%d）' % (tr['syn_pct'], tr['syn'], tr['real_pct'], tr['real']),
        'final_distribution.json（同 manifests/train.json 域统计 %d/%d）' % (syn, real))
    row('train 正样本 1350 / 负样本 1350',
        tr['pos'] == 1350 and tr['neg'] == 1350,
        '%d / %d' % (tr['pos'], tr['neg']), 'final_distribution.json')
    row('两类负样本各 675',
        tr['neg_types']['adverse_no_accident'] == 675 and tr['neg_types']['clear_accident'] == 675,
        'adverse_no_accident=%d, clear_accident=%d' % (
            tr['neg_types']['adverse_no_accident'], tr['neg_types']['clear_accident']),
        'final_distribution.json')

    val_real_all = all(x['domain'] == 'real' for x in val)
    test_real_all = all(x['domain'] == 'real' for x in test)
    val_pos = sum(1 for x in val if x['target'] == 1)
    val_neg = sum(1 for x in val if x['target'] == 0)
    row('val_real 100% 真实且含正负样本', val_real_all and val_pos > 0 and val_neg > 0,
        'domain=real: %d/200；正 %d / 负 %d' % (sum(1 for x in val if x['domain'] == 'real'), val_pos, val_neg),
        'manifests/val_real.json')
    row('test_real 100% 真实', test_real_all, '%d/340' % sum(1 for x in test if x['domain'] == 'real'),
        'manifests/test_real.json')

    ids = [x['sample_id'] for x in master]
    row('sample_id 重复 = 0', len(set(ids)) == len(ids), '%d 唯一 / %d' % (len(set(ids)), len(ids)),
        'split_leakage_check.json（duplicate_sample_id=%d）' % leak['duplicate_sample_id'])
    row('group 跨 split 重叠 = 0', leak['group_overlap'] == 0, leak['group_overlap'],
        'split_leakage_check.json（唯一组 %d = 样本总数 %d，重复组 %d，缺失组 %d）' % (
            leak['unique_group_count'], leak['sample_total'],
            leak['duplicate_group_count'], leak['missing_group_count']))
    row('路径错误 = 0', leak['path_errors'] == 0, leak['path_errors'],
        'split_leakage_check.json')
    row('4971 × 25 = 124275 JPG',
        integ['total_samples'] == 4971 and integ['total_jpg'] == 124275,
        '%d 条 / %d jpg / %.2f GB（bad_path=%d 缺帧=%d 坏解码=%d 重复帧序列=%d）' % (
            integ['total_samples'], integ['total_jpg'], integ['total_bytes'] / 1e9,
            integ['bad_path_count'], integ['bad_frame_count_count'],
            integ['bad_decode_count'], integ['duplicate_frame_sequence']),
        'frame_integrity_check.json')
    row('加载器全量遍历 4971/4971、0 错误',
        loader['iterated'] == 4971 and loader['total'] == 4971 and loader['errors'] == 0,
        'iterated=%s/%s errors=%d' % (loader['iterated'], loader['total'], loader['errors']),
        'loader_delivery_result.json')
    row('标签逻辑错误 = 0', label['error_count'] == 0, label['error_count'],
        'label_logic_check.json')

    ok_all = all(r['pass'] for r in rows)
    result = {
        'reverify_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'purpose': '冻结前最终复验（2026-10-04 修正指令第四项），全部以实际文件为准，未做任何修改',
        'items': rows,
        'all_pass': ok_all,
        'conclusion': 'PASS' if ok_all else 'FAIL',
    }
    out = os.path.join(R, 'final_reverify.json')
    json.dump(result, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('written %s' % out)
    for r in rows:
        print('[%s] %s = %s (%s)' % ('PASS' if r['pass'] else 'FAIL', r['item'], r['value'], r['source']))
    print('ALL_PASS=%s CONCLUSION=%s' % (ok_all, result['conclusion']))


if __name__ == '__main__':
    main()
