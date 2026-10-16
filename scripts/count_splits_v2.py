# -*- coding: utf-8 -*-
"""只读统计 v2 主清单的 split x source x domain x weather 分布"""
import json, collections

P = r'D:\dataset_v2_export\dataset_v2\dataset_planB_v2.json'
data = json.load(open(P, encoding='utf-8'))
items = data['items']
print('total', len(items))

split_counts = collections.Counter(i.get('split') for i in items)
print('split:', dict(split_counts))

for sp in sorted(split_counts):
    sub = [i for i in items if i.get('split') == sp]
    by_src = collections.Counter(i['source'] for i in sub)
    by_dom = collections.Counter(i['domain'] for i in sub)
    by_wea = collections.Counter(i['weather'] for i in sub)
    by_acc = collections.Counter(i['accident'] for i in sub)
    print(sp, 'n=%d' % len(sub))
    print('  source:', dict(by_src))
    print('  domain:', dict(by_dom))
    print('  weather:', dict(by_wea))
    print('  accident:', dict(by_acc))

# 未知 split / null
null_sp = [i['sample_id'] for i in items if i.get('split') is None]
print('split=None:', len(null_sp), null_sp[:10])

# CCD 目录名唯一性检查（group 基础）
ccd_ids = [i['sample_id'] for i in items if i['source'] == 'ccd_real']
print('ccd n=%d uniq=%d' % (len(ccd_ids), len(set(ccd_ids))))
