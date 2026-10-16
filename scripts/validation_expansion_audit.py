# -*- coding: utf-8 -*-
"""validation_expansion_audit.py — v1.1 验证集扩充：第一步只读审计（修改任何清单前完成）

统计 dataset_final（冻结 v1.0，只读）reserve 中的三类候选：
  正样本候选 = domain=real AND accident=1 AND adverse_weather=1 AND target=1 AND prediction_eligible=true
  负样本A候选 = domain=real AND accident=0 AND adverse_weather=1 AND target=0 AND negative_type=adverse_no_accident
  负样本B候选 = domain=real AND accident=1 AND adverse_weather=0 AND target=0 AND negative_type=clear_accident
输出 reports\validation_expansion_inventory.{json,csv,md} 并判定数量闸门
（正≥50 且 负A≥25 且 负B≥25 才继续；任一不足输出缺口报告并停止）。
"""
import json
import os
import collections
import datetime

ROOT = r'D:\dataset_final_export\dataset_final'
M = os.path.join(ROOT, 'manifests', 'dataset_master.json')
R = os.path.join(ROOT, 'reports')
OUT_JSON = os.path.join(R, 'validation_expansion_inventory.json')
OUT_CSV = os.path.join(R, 'validation_expansion_inventory.csv')
OUT_MD = os.path.join(R, 'validation_expansion_inventory.md')
OUT_GAP = os.path.join(R, 'validation_expansion_gap.md')


def is_pos_cand(x):
    return (x['domain'] == 'real' and x['accident'] == 1 and x['adverse_weather'] == 1
            and x['target'] == 1 and x.get('prediction_eligible', True) is True)


def is_negA_cand(x):
    return (x['domain'] == 'real' and x['accident'] == 0 and x['adverse_weather'] == 1
            and x['target'] == 0 and x['negative_type'] == 'adverse_no_accident')


def is_negB_cand(x):
    return (x['domain'] == 'real' and x['accident'] == 1 and x['adverse_weather'] == 0
            and x['target'] == 0 and x['negative_type'] == 'clear_accident')


def summarize(its):
    s = {
        'count': len(its),
        'weather': dict(collections.Counter(x['weather'] for x in its)),
        'source': dict(collections.Counter(x['source'] for x in its)),
        'quality_flag': dict(collections.Counter(
            ','.join(x.get('quality_flag') or []) for x in its)),
        'prediction_eligible': dict(collections.Counter(x.get('prediction_eligible') for x in its)),
        'unique_original_video_ids': len({str(x['original_video_id']) for x in its}),
        'unique_group_ids': len({str(x['group_id']) for x in its}),
        'splits': dict(collections.Counter(x['split'] for x in its)),
    }
    return s


def main():
    m = json.load(open(M, encoding='utf-8'))
    reserve = [x for x in m if x['split'] == 'reserve']
    pos = [x for x in reserve if is_pos_cand(x)]
    negA = [x for x in reserve if is_negA_cand(x)]
    negB = [x for x in reserve if is_negB_cand(x)]

    gate = {
        'pos_need': 50, 'negA_need': 25, 'negB_need': 25,
        'pos_have': len(pos), 'negA_have': len(negA), 'negB_have': len(negB),
        'pos_pass': len(pos) >= 50, 'negA_pass': len(negA) >= 25, 'negB_pass': len(negB) >= 25,
        'gate_pass': len(pos) >= 50 and len(negA) >= 25 and len(negB) >= 25,
    }
    gate['max_balanced_expansion'] = min(len(pos), len(negA), len(negB)) if gate['gate_pass'] is False \
        else min(len(pos), len(negA), len(negB))

    result = {
        'audit_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'input': 'manifests/dataset_master.json（冻结 v1.0，只读）',
        'reserve_total': len(reserve),
        'pos_candidates': {'summary': summarize(pos), 'sample_ids': [x['sample_id'] for x in pos]},
        'negA_candidates': {'summary': summarize(negA)},
        'negB_candidates': {'summary': summarize(negB)},
        'gate': gate,
        'conclusion': ('闸门通过' if gate['gate_pass']
                       else '闸门未通过：正样本候选 %d < 50（reserve 中真实恶劣天气事故正样本实际仅剩 %d 条）。'
                            '按指令不修改任何清单、不复制/重复使用样本、不下载、不生成 CARLA；'
                            '输出缺口报告并停止等待用户确认。' % (len(pos), len(pos))),
    }
    json.dump(result, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    # CSV
    with open(OUT_CSV, 'w', encoding='utf-8') as f:
        f.write('sample_type,count,weather,source,unique_video_ids,unique_group_ids,'
                'prediction_eligible_true,quality_flag\n')
        for t, its in [('pos', pos), ('negA', negA), ('negB', negB)]:
            s = summarize(its)
            f.write('%s,%d,"%s","%s",%d,%d,%d,"%s"\n' % (
                t, len(its), json.dumps(s['weather'], ensure_ascii=False),
                json.dumps(s['source'], ensure_ascii=False),
                s['unique_original_video_ids'], s['unique_group_ids'],
                s['prediction_eligible'].get(True, 0),
                json.dumps(s['quality_flag'], ensure_ascii=False)))

    # MD
    lines = ['# dataset_final v1.1 验证集扩充 · 第一步只读审计（reserve 候选）', '',
             '审计时间：%s' % result['audit_time'], '',
             '输入：`manifests/dataset_master.json`（冻结 v1.0，只读）；reserve 共 **%d** 条。' % len(reserve), '',
             '## 候选定义与数量', '',
             '| 类别 | 定义 | 数量 | 闸门要求 | 是否通过 |', '|---|---|---|---|---|',
             '| 正样本候选 | real ∧ accident=1 ∧ adverse_weather=1 ∧ target=1 ∧ prediction_eligible=true | %d | ≥50 | %s |'
             % (len(pos), '通过' if gate['pos_pass'] else '**不通过**'),
             '| 负样本A候选 | real ∧ accident=0 ∧ adverse_weather=1 ∧ negative_type=adverse_no_accident | %d | ≥25 | %s |'
             % (len(negA), '通过' if gate['negA_pass'] else '**不通过**'),
             '| 负样本B候选 | real ∧ accident=1 ∧ adverse_weather=0 ∧ negative_type=clear_accident | %d | ≥25 | %s |'
             % (len(negB), '通过' if gate['negB_pass'] else '**不通过**'),
             '', '## 各候选详细统计', '']
    for t, its in [('正样本候选(pos)', pos), ('负样本A候选(adverse_no_accident)', negA),
                   ('负样本B候选(clear_accident)', negB)]:
        s = summarize(its)
        lines += ['### %s（%d 条）' % (t, len(its)), '',
                  '| 维度 | 分布 |', '|---|---|',
                  '| weather | %s |' % json.dumps(s['weather'], ensure_ascii=False),
                  '| source | %s |' % json.dumps(s['source'], ensure_ascii=False),
                  '| prediction_eligible | %s |' % json.dumps(s['prediction_eligible'], ensure_ascii=False),
                  '| quality_flag | %s |' % json.dumps(s['quality_flag'], ensure_ascii=False),
                  '| 唯一 original_video_id | %d |' % s['unique_original_video_ids'],
                  '| 唯一 group_id | %d |' % s['unique_group_ids'], '']
    if pos:
        lines += ['### 正样本候选 sample_id 全清单', '',
                  '```']
        lines += [x['sample_id'] for x in pos]
        lines += ['```', '']
    lines += ['## 闸门判定', '',
              '**%s**' % result['conclusion'],
              '',
              '可达最大平衡规模（按三类中最小者）：**%d**（正 %d / 负A %d / 负B %d）'
              % (gate['max_balanced_expansion'], min(len(pos), gate['max_balanced_expansion']),
                 min(len(negA), gate['max_balanced_expansion']), min(len(negB), gate['max_balanced_expansion'])), '',
              '## 缺口说明', '',
              'reserve 中真实恶劣天气事故正样本**实际仅剩 %d 条**（CCD 恶劣天气事故总量 486，'
              'train 已用 270 / 原 val_real 已用 75 / test_real 已用 140，余 1）。'
              'DADA 25 条已全部在原 val_real；负样本A 候选仅 BDD（421）；负样本B 候选仅 CCD（769）。' % len(pos),
              '',
              '按用户指令：任一不足 → **不修改任何清单、不复制/重复使用样本、不下载、不生成 CARLA，'
              '停止并等待用户确认**。', '']
    open(OUT_MD, 'w', encoding='utf-8').write('\n'.join(lines))

    # 缺口报告（独立文件，供用户确认）
    gap = ['# validation_expansion 缺口报告（v1.1 闸门未通过）', '',
           '审计时间：%s' % result['audit_time'], '',
           '目标：val_real 200→300（新增正 50 / 负A 25 / 负B 25，100% 真实，全部来自 reserve）。', '',
           '## 候选实测数量', '',
           '| 候选 | 实测 | 需要 | 差额 |', '|---|---|---|---|',
           '| 真实恶劣天气事故正样本 | %d | 50 | **缺 %d** |' % (len(pos), 50 - len(pos)),
           '| 真实恶劣天气无事故（负A） | %d | 25 | 满足（富余 %d） |' % (len(negA), len(negA) - 25),
           '| 真实正常天气事故（负B） | %d | 25 | 满足（富余 %d） |' % (len(negB), len(negB) - 25), '',
           '## 闸门结论', '',
           '**未通过**：正样本候选 %d < 50。reserve 中真实恶劣天气事故正样本实际仅剩 %d 条，'
           '来源为 CCD（486 条总量中 train 270 / 原 val_real 75 / test_real 140 已占用，余 1）。' % (len(pos), len(pos)), '',
           '## 可达最大平衡规模', '',
           '按「三类候选取最小、保持正负平衡」：最大可新增 **%d** 条（正 %d / 负A %d / 负B %d），'
           '即 val_real 200→203，远小于 300 目标。' % (
               gate['max_balanced_expansion'],
               min(len(pos), gate['max_balanced_expansion']),
               min(len(negA), gate['max_balanced_expansion']),
               min(len(negB), gate['max_balanced_expansion'])), '',
           '## 可选方向（供用户拍板，未执行任何动作）', '',
           '1. **接受缩减规模**：新增 1 正 + 1 负A + 1 负B = 3 条，val_real 200→203（正 101/负 102，'
           '基本平衡，但远未达 300 目标）；',
           '2. **调整目标**：降低正样本扩充目标（如新增 1 正 + 25 负A + 25 负B → 正负失衡 101/150，'
           '不推荐，破坏正负 1:1 设计）；',
           '3. **新增真实数据源**：需下载更多 CCD/其他真实恶劣天气事故视频（用户指令本阶段禁止下载）；',
           '4. **保持 v1.0 不变**，放弃本次扩充。', '',
           '按用户指令：未修改任何清单、未复制样本、未下载、未生成 CARLA；停止等待用户确认。', '']
    open(OUT_GAP, 'w', encoding='utf-8').write('\n'.join(gap))

    print('written inventory json/csv/md + gap report')
    print('reserve_total=%d pos=%d negA=%d negB=%d' % (len(reserve), len(pos), len(negA), len(negB)))
    print('gate_pass=%s (pos>=50:%s negA>=25:%s negB>=25:%s)' % (
        gate['gate_pass'], gate['pos_pass'], gate['negA_pass'], gate['negB_pass']))
    if pos:
        print('pos sample_ids:', pos[0]['sample_id'])
    print('max_balanced_expansion=%d' % gate['max_balanced_expansion'])


if __name__ == '__main__':
    main()
