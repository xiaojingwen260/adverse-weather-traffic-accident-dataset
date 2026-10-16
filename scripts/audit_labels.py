# -*- coding: utf-8 -*-
"""audit_labels.py — v1.0 最终验收审计：标签一致性 / prediction_eligible 规则 / 划分 / 类别分布 / 元数据

独立复核（不沿用旧结论）。只读 master，只报告不修改。
输出：reports/audit_labels.json + reports/audit_labels.md
"""
import json
import os
import collections
import datetime

ROOT = r'D:\dataset_final_export\dataset_final'
M = os.path.join(ROOT, 'manifests', 'dataset_master.json')
R = os.path.join(ROOT, 'reports')
OUT_JSON = os.path.join(R, 'audit_labels.json')
OUT_MD = os.path.join(R, 'audit_labels.md')

WEATHERS = ['rainy', 'snowy', 'night', 'clear']
ADVERSE = {'rainy', 'snowy', 'night'}
CARLA_TOWNS = {'Town01', 'Town02', 'Town04', 'Town05', 'Town10HD_Opt'}
SPLITS = ['train', 'val_real', 'test_real', 'reserve']


def main():
    m = json.load(open(M, encoding='utf-8'))
    problems = []  # {sample_id, field, value, problem, severity}

    def add(sid, field, value, problem, sev):
        problems.append({'sample_id': sid, 'field': field, 'value': str(value),
                         'problem': problem, 'severity': sev})

    # ---------- A. 字段合法性 / 标签一致性 ----------
    for it in m:
        sid = it['sample_id']
        w = it['weather']
        if w not in WEATHERS:
            add(sid, 'weather', w, 'weather 不在枚举 {rainy,snowy,night,clear}', 'B')
        adv = it['adverse_weather']
        if adv != (1 if w in ADVERSE else 0):
            add(sid, 'adverse_weather', adv, 'adverse_weather 与 weather 不一致', 'A')
        if it['target'] != (1 if (it['accident'] == 1 and adv == 1) else 0):
            add(sid, 'target', it['target'], 'target != accident AND adverse_weather', 'A')
        nt = it['negative_type']
        if nt == 'adverse_no_accident':
            if not (it['accident'] == 0 and adv == 1 and it['target'] == 0):
                add(sid, 'negative_type', nt, 'adverse_no_accident 字段矛盾', 'A')
        elif nt == 'clear_accident':
            if not (it['accident'] == 1 and adv == 0 and it['target'] == 0):
                add(sid, 'negative_type', nt, 'clear_accident 字段矛盾（accident 必须=1）', 'A')
        elif nt is None:
            if it['target'] != 1:
                add(sid, 'negative_type', nt, 'negative_type=null 但 target!=1', 'A')
        else:
            add(sid, 'negative_type', nt, 'negative_type 非法值', 'B')
        dom = it['domain']
        src = it['source']
        if src == 'CARLA':
            if dom != 'synthetic':
                add(sid, 'domain', dom, 'CARLA 应为 synthetic', 'A')
        else:
            if dom != 'real':
                add(sid, 'domain', dom, '%s 应为 real' % src, 'A')
        if it['scenario'] not in {'rear_end', 'side_impact', 'pedestrian', 'unknown'}:
            add(sid, 'scenario', it['scenario'], 'scenario 非法', 'B')
        if it['split'] not in SPLITS:
            add(sid, 'split', it['split'], 'split 非法', 'A')
        if it['frame_count'] != 25:
            add(sid, 'frame_count', it['frame_count'], 'frame_count!=25', 'A')
        if it['fps'] != 5:
            add(sid, 'fps', it['fps'], 'fps!=5', 'A')
        if it['town'] is not None and src == 'CARLA':
            if it['town'] not in CARLA_TOWNS:
                add(sid, 'town', it['town'], 'CARLA town 不在枚举', 'B')
        if it['town'] is not None and src != 'CARLA':
            add(sid, 'town', it['town'], '真实数据 town 应 null', 'C')
        # collision_frame 一致性
        cf = it['collision_frame']
        if it['accident'] == 1:
            if cf is None:
                add(sid, 'collision_frame', cf, 'accident=1 但 collision_frame=null', 'B')
            else:
                if not (1 <= cf <= 25):
                    add(sid, 'collision_frame', cf, 'collision_frame 超出 1..25', 'B')
        # width/height 合法性
        if not (isinstance(it['width'], int) and isinstance(it['height'], int) and
                it['width'] > 0 and it['height'] > 0):
            add(sid, 'width/height', '%sx%s' % (it['width'], it['height']), '尺寸非法', 'B')
        # quality_flag / prediction_eligible 结构
        qf = it.get('quality_flag') or []
        if qf not in ([], ['early_motion_peak']):
            add(sid, 'quality_flag', qf, 'quality_flag 非法值', 'B')
        if not isinstance(it['prediction_eligible'], bool):
            add(sid, 'prediction_eligible', it['prediction_eligible'], 'prediction_eligible 非布尔', 'A')
        # original_video_id 非空
        if not it.get('original_video_id'):
            add(sid, 'original_video_id', it.get('original_video_id'), 'original_video_id 为空', 'B')

    # ---------- B. prediction_eligible 规则复核 ----------
    early = [it for it in m if (it.get('quality_flag') or []) == ['early_motion_peak']]
    early_false = [it for it in early if it['prediction_eligible'] is False]
    false_nonearly = [it for it in m if it['prediction_eligible'] is False and
                      (it.get('quality_flag') or []) != ['early_motion_peak']]
    early_by_src = collections.Counter(it['source'] for it in early)
    early_by_split = collections.Counter(it['split'] for it in early)

    # 早峰样本 peak_frame_mad 复核（仅合成正样本有 peak 字段）
    early_peak_lt18 = 0
    early_peak_ge18 = []
    early_no_peak = 0
    for it in early:
        pk = it.get('peak_frame_mad')
        if pk is None:
            early_no_peak += 1
        elif pk < 18:
            early_peak_lt18 += 1
        else:
            early_peak_ge18.append({'sample_id': it['sample_id'], 'peak': pk})

    # 正样本 prediction_eligible=true 的碰撞帧分布（规则：碰撞位于 18~22 才可预测）
    pos_true = [it for it in m if it['target'] == 1 and it['prediction_eligible'] is True]
    cf_dist = collections.Counter(it['collision_frame'] for it in pos_true)
    pos_true_cf_bad = [it for it in pos_true if not (isinstance(it['collision_frame'], int)
                                                     and 18 <= it['collision_frame'] <= 22)]
    # 真实正样本碰撞帧
    real_pos = [it for it in m if it['target'] == 1 and it['domain'] == 'real']
    real_pos_cf = collections.Counter(it['collision_frame'] for it in real_pos)

    # 负样本 prediction_eligible=true 数量与语义说明
    neg_true = [it for it in m if it['target'] == 0 and it['prediction_eligible'] is True]

    # ---------- C. 划分互斥 ----------
    by_split = {sp: [it for it in m if it['split'] == sp] for sp in SPLITS}
    id_sets = {sp: {it['sample_id'] for it in by_split[sp]} for sp in SPLITS}
    group_sets = {sp: {it['group_id'] for it in by_split[sp]} for sp in SPLITS}
    vid_sets = {sp: {(it['source'], str(it['original_video_id'])) for it in by_split[sp]} for sp in SPLITS}
    split_id_overlap = {}
    split_group_overlap = {}
    split_vid_overlap = {}
    for a in SPLITS:
        for b in SPLITS:
            if a < b:
                split_id_overlap['%s/%s' % (a, b)] = len(id_sets[a] & id_sets[b])
                split_group_overlap['%s/%s' % (a, b)] = len(group_sets[a] & group_sets[b])
                split_vid_overlap['%s/%s' % (a, b)] = len(vid_sets[a] & vid_sets[b])

    # ---------- D. 类别分布（全量 + 关键组合） ----------
    def c(keyfn):
        return dict(collections.Counter(keyfn(it) for it in m))

    dist = {
        'total': len(m),
        'split': c(lambda x: x['split']),
        'target': c(lambda x: 'pos' if x['target'] == 1 else 'neg'),
        'domain': c(lambda x: x['domain']),
        'weather': c(lambda x: x['weather']),
        'source': c(lambda x: x['source']),
        'accident': c(lambda x: x['accident']),
        'negative_type': c(lambda x: str(x['negative_type'])),
        'prediction_eligible': c(lambda x: x['prediction_eligible']),
        'scenario': c(lambda x: x['scenario']),
        'camera_type': {'missing_field': len(m)},  # 字段不存在 → 元数据缺口
        'combos': {
            'real_accident': sum(1 for x in m if x['domain'] == 'real' and x['accident'] == 1),
            'real_nonaccident': sum(1 for x in m if x['domain'] == 'real' and x['accident'] == 0),
            'syn_accident': sum(1 for x in m if x['domain'] == 'synthetic' and x['accident'] == 1),
            'syn_nonaccident': sum(1 for x in m if x['domain'] == 'synthetic' and x['accident'] == 0),
            'rainy_accident': sum(1 for x in m if x['weather'] == 'rainy' and x['accident'] == 1),
            'snowy_accident': sum(1 for x in m if x['weather'] == 'snowy' and x['accident'] == 1),
            'night_accident': sum(1 for x in m if x['weather'] == 'night' and x['accident'] == 1),
            'rainy_night_accident': sum(1 for x in m if x['weather'] == 'rainy' and x['adverse_weather'] == 1 and x['accident'] == 1),
            'adverse_accident': sum(1 for x in m if x['adverse_weather'] == 1 and x['accident'] == 1),
            'adverse_nonaccident': sum(1 for x in m if x['adverse_weather'] == 1 and x['accident'] == 0),
            'pe_true_real_accident': sum(1 for x in m if x['prediction_eligible'] and x['domain'] == 'real' and x['accident'] == 1),
            'pe_true_adverse_accident': sum(1 for x in m if x['prediction_eligible'] and x['adverse_weather'] == 1 and x['accident'] == 1),
            'clear_accident_total': sum(1 for x in m if x['negative_type'] == 'clear_accident'),
        },
    }
    # 每 split 的详细统计（正负/accident rate/day-night/天气/域/pe）
    per_split = {}
    for sp in SPLITS:
        its = by_split[sp]
        n = len(its)
        day_night = {'night': sum(1 for x in its if x['weather'] == 'night'),
                     'day': sum(1 for x in its if x['weather'] != 'night')}
        per_split[sp] = {
            'total': n,
            'pos': sum(1 for x in its if x['target'] == 1),
            'neg': sum(1 for x in its if x['target'] == 0),
            'accident_rate': round(sum(1 for x in its if x['accident'] == 1) / n, 4) if n else None,
            'day_night': day_night,
            'weather': dict(collections.Counter(x['weather'] for x in its)),
            'domain': dict(collections.Counter(x['domain'] for x in its)),
            'prediction_eligible': dict(collections.Counter(x['prediction_eligible'] for x in its)),
            'negative_type': dict(collections.Counter(str(x['negative_type']) for x in its)),
        }

    # ---------- E. 元数据缺口 ----------
    meta_gaps = {
        'camera_type': 'manifest 无 camera 字段（实际来源均为前视行车记录仪视角）→ C 级元数据缺口',
        'day_night': 'manifest 无 day/night 字段；本审计按 weather=night→night、其余→day 映射统计',
        'source_url': 'manifest 无 source URL 字段 → 无法直接验证链接，靠 original_video_id/本地源文件追溯',
        'fog': 'weather 无 fog 类（源数据不含雾天）',
    }

    result = {
        'audit_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'input': 'manifests/dataset_master.json（只读）',
        'problem_count': len(problems),
        'problems': problems,
        'prediction_eligible': {
            'true_total': sum(1 for x in m if x['prediction_eligible'] is True),
            'false_total': sum(1 for x in m if x['prediction_eligible'] is False),
            'by_domain': dict(collections.Counter(('%s/%s' % (x['domain'], x['prediction_eligible'])) for x in m)),
            'by_split': dict(collections.Counter(('%s/%s' % (x['split'], x['prediction_eligible'])) for x in m)),
            'by_negative_type': dict(collections.Counter(('%s/%s' % (str(x['negative_type']), x['prediction_eligible'])) for x in m)),
            'early_motion_peak': {
                'total': len(early),
                'by_source': dict(early_by_src),
                'by_split': dict(early_by_split),
                'early_and_false': len(early_false),
                'false_but_not_early': [x['sample_id'] for x in false_nonearly],
                'peak_lt18': early_peak_lt18,
                'peak_ge18': early_peak_ge18,
                'no_peak_field': early_no_peak,
            },
            'pos_true_collision_frame_dist': dict(cf_dist),
            'pos_true_cf_outside_18_22': pos_true_cf_bad,
            'real_pos_collision_frame_dist': dict(real_pos_cf),
            'neg_true_count': len(neg_true),
            'neg_true_note': ('负样本 prediction_eligible=true 语义：作为预测任务的无事故窗口（负类），'
                              '与正样本预测资格不冲突；其 eligibility 仅表示可参与预测任务训练/评估。'),
        },
        'split_exclusion': {
            'id_overlap': split_id_overlap,
            'group_overlap': split_group_overlap,
            'video_overlap': split_vid_overlap,
        },
        'distribution': dist,
        'per_split': per_split,
        'metadata_gaps': meta_gaps,
        'conclusion': 'PASS' if not any(p['severity'] in ('A', 'B') for p in problems) else 'ISSUES_FOUND',
    }
    json.dump(result, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    lines = ['# v1.0 最终验收审计 · 标签一致性 / 预测资格 / 划分 / 分布 / 元数据', '',
             '审计时间：%s' % result['audit_time'], '',
             '## 1. 字段合法性与标签一致性', '',
             '发现问题：**%d** 条' % len(problems), '']
    if problems:
        sev_c = collections.Counter(p['severity'] for p in problems)
        lines += ['按严重程度：%s' % dict(sev_c), '',
                  '| sample_id | 字段 | 值 | 问题 | 严重程度 |', '|---|---|---|---|---|']
        for p in problems:
            lines.append('| %s | %s | %s | %s | %s |' % (p['sample_id'], p['field'],
                                                         p['value'], p['problem'], p['severity']))
        lines += ['']
    lines += ['## 2. prediction_eligible 规则复核', '',
              '- prediction_eligible=true：**%d**；false：**%d**' % (
                  result['prediction_eligible']['true_total'],
                  result['prediction_eligible']['false_total']),
              '- early_motion_peak 标记：**%d**（source 分布 %s；split 分布 %s）' % (
                  len(early), dict(early_by_src), dict(early_by_split)),
              '- early 且 prediction_eligible=false：%d；false 但非 early：%d 条 %s' % (
                  len(early_false), len(false_nonearly), [x['sample_id'] for x in false_nonearly]),
              '- early 样本 peak_frame_mad<18：%d；>=18：%d 条 %s；无 peak 字段：%d（真实样本无 MAD 字段）' % (
                  early_peak_lt18, len(early_peak_ge18), early_peak_ge18[:10], early_no_peak),
              '- 正样本 true 的碰撞帧分布：%s' % dict(cf_dist),
              '- 正样本 true 中碰撞帧在 [18,22] 之外：%d 条 %s' % (
                  len(pos_true_cf_bad), [x['sample_id'] for x in pos_true_cf_bad]),
              '- 真实正样本碰撞帧分布：%s' % dict(real_pos_cf),
              '- 负样本 true：%d（语义说明见 json）' % len(neg_true), '',
              '## 3. 划分互斥', '',
              '| 集合对 | ID 重叠 | group 重叠 | 视频重叠 |', '|---|---|---|---|']
    for k in sorted(split_id_overlap):
        lines.append('| %s | %d | %d | %d |' % (k, split_id_overlap[k],
                                                split_group_overlap[k], split_vid_overlap[k]))
    lines += ['', '## 4. 类别分布（全库）', '',
              '| 维度 | 分布 |', '|---|---|']
    for k, v in dist.items():
        if k in ('combos', 'camera_type'):
            continue
        lines.append('| %s | %s |' % (k, json.dumps(v, ensure_ascii=False)))
    lines += ['', '### 关键组合', '', '| 组合 | 数量 |', '|---|---|']
    for k, v in dist['combos'].items():
        lines.append('| %s | %d |' % (k, v))
    lines += ['', '## 5. 每 split 统计', '']
    for sp in SPLITS:
        lines += ['### %s' % sp, '', '```', json.dumps(per_split[sp], ensure_ascii=False, indent=2), '```', '']
    lines += ['## 6. 元数据缺口', '']
    for k, v in meta_gaps.items():
        lines.append('- **%s**：%s' % (k, v))
    lines += ['', '## 7. 结论', '',
              '**%s**' % result['conclusion'], '']
    open(OUT_MD, 'w', encoding='utf-8').write('\n'.join(lines))
    print('DONE labels: problems=%d sev=%s' % (len(problems),
          dict(collections.Counter(p['severity'] for p in problems))))
    print('pe true=%d false=%d early=%d early_false=%d false_nonearly=%d' % (
        result['prediction_eligible']['true_total'],
        result['prediction_eligible']['false_total'], len(early),
        len(early_false), len(false_nonearly)))
    print('pos_true_cf_outside_18_22=%d real_pos_cf=%s' % (len(pos_true_cf_bad), dict(real_pos_cf)))
    print('split overlaps:', split_id_overlap, split_group_overlap, split_vid_overlap)


if __name__ == '__main__':
    main()
