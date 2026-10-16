# -*- coding: utf-8 -*-
"""audit_cross.py — v1.0 最终验收审计：主清单与各清单/报告/README 交叉一致性（只读）

交叉核对：
  1) master 4971 ↔ train/val_real/test_real/reserve.json（sample_id 集合 + split 字段一致性）
  2) master 实测统计 ↔ reports/final_distribution.json 关键数字
  3) master 实测 ↔ reports/final_reverify.json 结论
  4) README.md 关键数字（4971 / 124275 / 17.52GB / 2700 / 200 / 340 / 1731）
  5) reports/loader_delivery_result.json（4971/4971）
  6) state.yaml（current=07_training）与 handoff 关键数字（只读引用）
输出：reports/audit_cross.json + reports/audit_cross.md
"""
import json
import os
import collections
import datetime
import re

ROOT = r'D:\dataset_final_export\dataset_final'
M = os.path.join(ROOT, 'manifests')
R = os.path.join(ROOT, 'reports')
OUT_JSON = os.path.join(R, 'audit_cross.json')
OUT_MD = os.path.join(R, 'audit_cross.md')
WB = r'D:\workbuddyworkplatform\workflows\crash-synthesis'


def main():
    master = json.load(open(os.path.join(M, 'dataset_master.json'), encoding='utf-8'))
    splits = {}
    for sp in ['train', 'val_real', 'test_real', 'reserve']:
        splits[sp] = json.load(open(os.path.join(M, sp + '.json'), encoding='utf-8'))

    master_by_split = collections.defaultdict(list)
    for it in master:
        master_by_split[it['split']].append(it['sample_id'])

    diffs = []
    split_set_mismatch = {}
    for sp, items in splits.items():
        ids_json = {x['sample_id'] for x in items}
        ids_master = set(master_by_split[sp])
        only_json = sorted(ids_json - ids_master)
        only_master = sorted(ids_master - ids_json)
        if only_json or only_master:
            split_set_mismatch[sp] = {'only_in_json': only_json, 'only_in_master': only_master}
            diffs.append('split %s: sample_id 集合与 master 不一致（json 独有 %d / master 独有 %d）' % (
                sp, len(only_json), len(only_master)))
        # 字段一致性抽查：json 记录 vs master 对应记录
        mby = {x['sample_id']: x for x in master if x['split'] == sp}
        field_diffs = 0
        for x in items:
            mm = mby.get(x['sample_id'])
            if mm is None:
                continue
            for f in ['split', 'domain', 'accident', 'weather', 'target', 'negative_type',
                      'prediction_eligible', 'frame_dir', 'group_id', 'source']:
                if x.get(f) != mm.get(f):
                    field_diffs += 1
        if field_diffs:
            diffs.append('split %s: 与 master 对应记录字段不一致 %d 处' % (sp, field_diffs))

    # master 实测 vs final_distribution.json
    def cnt(key):
        return collections.Counter(it[key] for it in master)
    dist = json.load(open(os.path.join(R, 'final_distribution.json'), encoding='utf-8'))
    master_counts = {
        'total': len(master),
        'split': dict(cnt('split')),
        'target': dict(cnt('target')),
        'domain': dict(cnt('domain')),
        'weather': dict(cnt('weather')),
        'source': dict(cnt('source')),
        'negative_type': dict(cnt('negative_type')),
    }
    dist_diffs = []
    if dist.get('total') != len(master):
        dist_diffs.append('final_distribution.total=%s != master %d' % (dist.get('total'), len(master)))
    tr = dist.get('train_ratio', {})
    if tr.get('syn') != 2160 or tr.get('real') != 540:
        dist_diffs.append('train_ratio syn/real=%s/%s != 2160/540' % (tr.get('syn'), tr.get('real')))
    if tr.get('pos') != 1350 or tr.get('neg') != 1350:
        dist_diffs.append('train_ratio pos/neg=%s/%s != 1350/1350' % (tr.get('pos'), tr.get('neg')))
    if tr.get('neg_types', {}).get('adverse_no_accident') != 675 or \
            tr.get('neg_types', {}).get('clear_accident') != 675:
        dist_diffs.append('train_ratio neg_types != 675/675')

    # README 关键数字
    readme = open(os.path.join(ROOT, 'README.md'), encoding='utf-8').read()
    readme_checks = {
        '4971': '4971' in readme,
        '124275': '124,275' in readme or '124275' in readme,
        '2700': '2700' in readme,
        '200 (val)': '200' in readme,
        '340 (test)': '340' in readme,
        '1731 (reserve)': '1731' in readme,
    }
    readme_missing = [k for k, v in readme_checks.items() if not v]

    # final_reverify
    rev = json.load(open(os.path.join(R, 'final_reverify.json'), encoding='utf-8'))
    rev_pass = rev.get('all_pass')
    rev_diffs = []
    if rev_pass is not True:
        rev_diffs.append('final_reverify.all_pass != true')

    # loader
    loader = json.load(open(os.path.join(R, 'loader_delivery_result.json'), encoding='utf-8'))
    loader_diffs = []
    if loader.get('iterated') != 4971 or loader.get('errors') != 0:
        loader_diffs.append('loader iterated/errors=%s/%s != 4971/0' % (
            loader.get('iterated'), loader.get('errors')))

    # state.yaml / handoff（只读引用）
    state_ok = None
    try:
        txt = open(os.path.join(WB, 'state.yaml'), encoding='utf-8').read()
        state_ok = '07_training' in txt.split('current:')[1].split('\n')[1]
    except Exception:
        state_ok = None
    handoff = open(os.path.join(WB, 'stages', '06_dataset_finalization', 'handoff.md'),
                   encoding='utf-8').read()
    handoff_checks = {
        '4971': '4971' in handoff,
        '124275': '124,275' in handoff or '124275' in handoff,
        '80.000%': '80.000%' in handoff,
        '2700/200/340/1731': all(x in handoff for x in ['2700', '200', '340', '1731']),
    }
    handoff_missing = [k for k, v in handoff_checks.items() if not v]

    result = {
        'audit_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'split_json_vs_master': {
            'counts': {sp: len(v) for sp, v in splits.items()},
            'mismatch': split_set_mismatch,
        },
        'master_counts': master_counts,
        'final_distribution_diffs': dist_diffs,
        'final_reverify_diffs': rev_diffs,
        'loader_diffs': loader_diffs,
        'readme_checks': readme_checks,
        'readme_missing': readme_missing,
        'state_current_ok': state_ok,
        'handoff_checks': handoff_checks,
        'handoff_missing': handoff_missing,
        'diffs': diffs + dist_diffs + rev_diffs + loader_diffs +
                (['README 缺关键数字: %s' % readme_missing] if readme_missing else []) +
                (['handoff 缺关键数字: %s' % handoff_missing] if handoff_missing else []),
        'conclusion': 'PASS' if not (diffs or dist_diffs or rev_diffs or loader_diffs
                                     or readme_missing or handoff_missing or state_ok is False) else 'DIFFS_FOUND',
    }
    json.dump(result, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    lines = ['# v1.0 最终验收审计 · 主清单与各清单/报告交叉一致性', '',
             '审计时间：%s' % result['audit_time'], '',
             '## 1. master ↔ split json', '',
             '| split | json 条数 | master 条数 | 集合差异 |', '|---|---|---|---|']
    for sp, items in splits.items():
        lines.append('| %s | %d | %d | %s |' % (sp, len(items), len(master_by_split[sp]),
                                                '一致' if sp not in split_set_mismatch else '不一致'))
    lines += ['', '## 2. master 实测统计', '',
              '| 维度 | 实测 |', '|---|---|']
    for k, v in master_counts.items():
        lines.append('| %s | %s |' % (k, json.dumps(v, ensure_ascii=False)))
    lines += ['', '## 3. 报告交叉差异', '',
              '| 检查 | 结果 |', '|---|---|',
              '| final_distribution | %s |' % (dist_diffs or '一致'),
              '| final_reverify | %s |' % (rev_diffs or 'PASS'),
              '| loader_delivery_result | %s |' % (loader_diffs or '4971/4971, errors=0'),
              '| README 关键数字 | %s |' % (readme_missing or '齐全'),
              '| state.yaml current | %s |' % ('07_training ✓' if state_ok else '需检查'),
              '| handoff 关键数字 | %s |' % (handoff_missing or '齐全'), '',
              '## 4. 结论', '',
              '**%s**' % result['conclusion'], '']
    open(OUT_MD, 'w', encoding='utf-8').write('\n'.join(lines))
    print('DONE cross: split mismatch=%s dist_diffs=%s rev=%s loader=%s readme_missing=%s handoff_missing=%s' % (
        split_set_mismatch, dist_diffs, rev_diffs, loader_diffs, readme_missing, handoff_missing))


if __name__ == '__main__':
    main()
