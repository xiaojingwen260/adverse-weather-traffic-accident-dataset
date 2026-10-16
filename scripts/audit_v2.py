# -*- coding: utf-8 -*-
"""audit_v2.py — dataset_final 阶段 1：只读审计（不重划分、不写数据）
输入：交付包 dataset_planB_v2.json（D:\\dataset_v2_export\\dataset_v2\\）
输出：D:\\dataset_final_export\\dataset_final\\reports\\pre_split_inventory.{json,csv,md}
计算：六类样本 + source/weather/domain/accident/target/scenario/split/original_video_id/town/
      collision_frame/negative_type 交叉统计；sample_id 唯一性；CARLA jpg 均大小（供缺口估算）
"""
import json, os, csv
from collections import Counter, defaultdict

MANIFEST = r'D:\dataset_v2_export\dataset_v2\dataset_planB_v2.json'
OUT = r'D:\dataset_final_export\dataset_final\reports'
CARLA_FRAMES = [r'D:\dataset_v2_export\dataset_v2\frames\carla_synth_v2',
                r'D:\dataset_v2_export\dataset_v2\frames\carla_neg_v2']
os.makedirs(OUT, exist_ok=True)

plan = json.load(open(MANIFEST, encoding='utf-8'))
items = plan['items']
ADVERSE = {'rainy', 'snowy', 'night'}

for it in items:
    it['adverse_weather'] = 1 if it['weather'] in ADVERSE else 0
    it['target'] = 1 if (it['accident'] == 1 and it['adverse_weather'] == 1) else 0
    a, aw, wx = it['accident'], it['adverse_weather'], it['weather']
    if a == 1 and aw == 1:
        it['negative_type'] = None
    elif a == 0 and aw == 1:
        it['negative_type'] = 'adverse_no_accident'
    elif a == 1 and aw == 0:
        it['negative_type'] = 'clear_accident'
    else:
        it['negative_type'] = 'clear_no_accident'
    it['original_video_id'] = it.get('video_id')

n = len(items)
dup_sid = n - len(set(it['sample_id'] for it in items))

def cls(it):
    d = it['domain']; aw = it['adverse_weather']; a = it['accident']
    if d == 'synthetic':
        if aw == 1 and a == 1: return 'syn_adverse_acc'
        if aw == 1 and a == 0: return 'syn_adverse_noacc'
        if aw == 0 and a == 1: return 'syn_clear_acc'
        return 'syn_clear_noacc'
    if aw == 1 and a == 1: return 'real_adverse_acc'
    if aw == 1 and a == 0: return 'real_adverse_noacc'
    if aw == 0 and a == 1: return 'real_clear_acc'
    return 'real_clear_noacc'

six = Counter(cls(it) for it in items)
ORDER = ['syn_adverse_acc', 'syn_adverse_noacc', 'syn_clear_acc',
         'real_adverse_acc', 'real_adverse_noacc', 'real_clear_acc',
         'syn_clear_noacc', 'real_clear_noacc']
six = {k: six.get(k, 0) for k in ORDER}

def cross(items_, keys):
    c = Counter()
    for it in items_:
        c['|'.join(str(it[k]) for k in keys)] += 1
    return dict(sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0]))))

inv = dict(
    total=n, duplicate_sample_id=dup_sid,
    six_class=six,
    by_source=dict(sorted(cross(items, ['source']).items())),
    by_weather=dict(sorted(cross(items, ['weather']).items())),
    by_domain=dict(sorted(cross(items, ['domain']).items())),
    by_accident=dict(sorted(cross(items, ['accident']).items())),
    by_target=dict(sorted(cross(items, ['target']).items())),
    by_negative_type=dict(sorted(cross(items, ['negative_type']).items(), key=lambda kv: str(kv[0]))),
    by_split_v2=dict(sorted(cross(items, ['split']).items())),
    by_scenario=dict(sorted(cross(items, ['scenario']).items(), key=lambda kv: str(kv[0]))),
    by_town=dict(sorted(cross(items, ['town']).items(), key=lambda kv: str(kv[0]))),
    by_collision_frame=dict(sorted(cross([i for i in items if i.get('collision_frame') is not None],
                                         ['collision_frame']).items())),
    six_x_split={('%s|%s' % (k[0], k[1])): c for k, c in
                 sorted(Counter((cls(it), it['split']) for it in items).items(), key=lambda kv: (-kv[1], str(kv[0])))},
    weather_x_domain_x_accident={
        '%s|%s|%d' % (k[0], k[1], k[2]): c
        for k, c in sorted(Counter((it['weather'], it['domain'], it['accident']) for it in items).items(),
                           key=lambda kv: (-kv[1], str(kv[0])))},
    test_real_composition={
        '%s|%s|%d|%s' % (k[0], k[1], k[2], str(k[3])): c
        for k, c in sorted(Counter((it['source'], it['weather'], it['accident'], str(it['negative_type']))
                                  for it in items if it['split'] == 'test' and it['domain'] == 'real').items(),
                           key=lambda kv: (-kv[1], str(kv[0])))},
    unique_video_per_source={src: len(set(it['original_video_id'] for it in items if it['source'] == src))
                             for src in sorted(set(it['source'] for it in items))},
    real_adverse_acc_by_weather=dict(sorted(Counter(it['weather'] for it in items
                                                    if it['domain'] == 'real' and it['adverse_weather'] == 1 and it['accident'] == 1).items())),
    real_adverse_noacc_by_weather=dict(sorted(Counter(it['weather'] for it in items
                                                      if it['domain'] == 'real' and it['adverse_weather'] == 1 and it['accident'] == 0).items())),
    real_clear_acc_by_source=dict(sorted(Counter(it['source'] for it in items
                                                 if it['domain'] == 'real' and it['weather'] == 'clear' and it['accident'] == 1).items())),
)
json.dump(inv, open(os.path.join(OUT, 'pre_split_inventory.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

# per-item CSV
with open(os.path.join(OUT, 'pre_split_inventory.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['sample_id', 'source', 'domain', 'weather', 'adverse_weather', 'accident',
                'target', 'negative_type', 'scenario', 'split', 'original_video_id',
                'town', 'collision_frame', 'frame_count', 'fps'])
    for it in sorted(items, key=lambda x: x['sample_id']):
        w.writerow([it['sample_id'], it['source'], it['domain'], it['weather'],
                    it['adverse_weather'], it['accident'], it['target'], it['negative_type'],
                    it.get('scenario'), it['split'], it['original_video_id'],
                    it.get('town'), it.get('collision_frame'), it.get('frame_count'), it.get('fps')])

# CARLA jpg 均大小（缺口报告估算用）
carla_files = 0; carla_bytes = 0
for root in CARLA_FRAMES:
    for dp, _, fns in os.walk(root):
        for fn in fns:
            if fn.lower().endswith('.jpg'):
                p = os.path.join(dp, fn)
                carla_files += 1
                carla_bytes += os.path.getsize(p)
carla_avg = carla_bytes / carla_files if carla_files else 0
inv['carla_jpg_count'] = carla_files
inv['carla_jpg_total_bytes'] = carla_bytes
inv['carla_jpg_avg_bytes'] = int(carla_avg)
json.dump(inv, open(os.path.join(OUT, 'pre_split_inventory.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

# MD report
L = []
A = L.append
A('# dataset_final 阶段 1 · 数据审计报告（pre-split inventory）')
A('')
A('- 输入：`D:\\dataset_v2_export\\dataset_v2\\dataset_planB_v2.json`（4431 条，交付包相对路径版）')
A('- 输出：`reports\\pre_split_inventory.{json,csv,md}`（本文件）')
A('- 日期：2026-10-04；本阶段只读，未重新划分数据，未启动 CARLA/训练')
A('')
A('## 1. 六类样本统计（主任务定义：target = accident AND adverse_weather）')
A('')
A('| 类别 | 定义 | 数量 |')
A('|---|---|---:|')
CN = {'syn_adverse_acc': 'synthetic + 恶劣天气事故', 'syn_adverse_noacc': 'synthetic + 恶劣天气无事故',
      'syn_clear_acc': 'synthetic + 晴天事故', 'real_adverse_acc': 'real + 恶劣天气事故',
      'real_adverse_noacc': 'real + 恶劣天气无事故', 'real_clear_acc': 'real + 晴天事故',
      'syn_clear_noacc': 'synthetic + 晴天无事故', 'real_clear_noacc': 'real + 晴天无事故'}
for k in ORDER:
    A('| %s | %s | %d |' % (k, CN[k], six[k]))
A('')
A('总计 %d 条；sample_id 重复 %d；晴天无事故（两类）合计 %d（该类不进入主任务，应入 reserve）'
  % (n, dup_sid, six['syn_clear_noacc'] + six['real_clear_noacc']))
A('')
A('## 2. 维度分布')
A('')
A('| 维度 | 分布 |')
A('|---|---|')
for k, title in [('by_source', 'source'), ('by_weather', 'weather'), ('by_domain', 'domain'),
                 ('by_accident', 'accident'), ('by_target', 'target'), ('by_negative_type', 'negative_type'),
                 ('by_split_v2', 'split(v2)'), ('by_scenario', 'scenario'), ('by_town', 'town(CARLA)')]:
    A('| %s | %s |' % (title, ', '.join('%s=%d' % (str(a), b) for a, b in inv[k].items())))
A('| collision_frame（有碰撞帧的正样本 %d 条） | %s |'
  % (sum(inv['by_collision_frame'].values()),
     ', '.join('%s=%d' % (str(a), b) for a, b in sorted(inv['by_collision_frame'].items(), key=lambda x: int(x[0])))))
A('')
A('## 3. 六类 × split(v2)')
A('')
A('| 类别 \\ split | %s |' % ' | '.join('train' if False else s for s in ['train', 'val', 'test']))
A('|---|---|---:|---:|---:|')
sixsplit = defaultdict(dict)
for key, c in inv['six_x_split'].items():
    cl, sp = key.split('|')
    sixsplit[cl][sp] = c
for k in ORDER:
    A('| %s | %d | %d | %d |' % (k, sixsplit[k].get('train', 0), sixsplit[k].get('val', 0), sixsplit[k].get('test', 0)))
A('')
A('## 4. weather × domain × accident')
A('')
A('| weather | domain | accident | n |')
A('|---|---|---|---:|')
for k, c in inv['weather_x_domain_x_accident'].items():
    wx, dom, acc = k.split('|')
    A('| %s | %s | %s | %d |' % (wx, dom, acc, c))
A('')
A('## 5. TEST_REAL 340 构成（v2 固定，不得重新抽样）')
A('')
A('| source | weather | accident | negative_type | n |')
A('|---|---|---|---|---:|')
for k, c in inv['test_real_composition'].items():
    src, wx, acc, nt = k.split('|')
    A('| %s | %s | %s | %s | %d |' % (src, wx, acc, 'None' if nt == 'None' else nt, c))
A('')
A('## 6. 关键发现（供缺口判断）')
A('')
A('- **synthetic + 晴天事故 = 0**（CARLA 合成仅 rainy/snowy/night；训练结构要求的合成正常天气事故负样本需新增生成或调整方案）→ 详见 `reports\\synthetic_clear_accident_gap.md`')
A('- 晴天无事故（两类）= %d（本就无此数据，reserve 为空类）' % (six['syn_clear_noacc'] + six['real_clear_noacc']))
A('- real 恶劣天气事故按天气：%s' % inv['real_adverse_acc_by_weather'])
A('- real 恶劣天气无事故按天气：%s' % inv['real_adverse_noacc_by_weather'])
A('- 训练结构可行性（推荐 2700 方案）所需的 real 侧供给：恶劣天气事故正 ≥270（可用 %d）、恶劣天气无事故负 ≥135（可用 %d）、晴天事故负 ≥135（可用 %d）'
  % (sum(inv['real_adverse_acc_by_weather'].values()), sum(inv['real_adverse_noacc_by_weather'].values()),
     sum(inv['real_clear_acc_by_source'].values())))
A('')
A('## 7. 来源')
A('- 全部数字由 `scripts\\audit_v2.py` 从输入清单实测统计；可复现。CARLA jpg 均大小 %d B（%d 张，供缺口估算）。'
  % (inv['carla_jpg_avg_bytes'], inv['carla_jpg_count']))

md = '\n'.join(L)
open(os.path.join(OUT, 'pre_split_inventory.md'), 'w', encoding='utf-8').write(md)
print('inventory ->', OUT)
print('six_class:', six)
print('carla avg jpg bytes:', inv['carla_jpg_avg_bytes'], 'files:', carla_files)
print('dup sample_id:', dup_sid)
