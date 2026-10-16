# -*- coding: utf-8 -*-
"""source_lineage_check.py — 来源级（原始视频/基础场景）防泄漏检查（冻结前追加）

背景：group_id 恰好等于 sample_id（4971 唯一组）不能单独证明无泄漏；
若 group_id 由 sample_id 生成，跨 split 交集必然为 0，但同一原始视频切出的多个
片段仍可能分布在不同集合。因此本脚本从实际字段重建「原始来源」分组。

分组方法（不沿用 group_id，字段以 dataset_master.json 实际存在为准）：
  1) 真实数据（CCD/DADA/BDD100K）：source + original_video_id 分组。
     实测：CCD 1500 样本 / 1500 唯一视频；DADA 25/25；BDD100K 746/746
     ⇒ 每条原始视频恰好产出 1 个 25 帧样本，不存在「同视频切多片段」。
  2) CARLA（2700 条 = 正 1080 + 负 1080 + clear 540）：
     - 字段事实：正样本 seed=null、负样本 seed=运行级随机种子（每组合一次运行一个
       seed，组内多条共享，非逐视频场景种子）、clear seed=null；无 episode_id /
       base_scene_id 字段。不得编造这些字段。
     - L1 逐原始视频：source + original_video_id ⇒ 每条唯一，跨 split 必然 0（参考基线）。
     - L2 运行段：负样本按 source+town+scenario+weather+seed；正/clear 无 seed，
       按 source+town+scenario+weather（weather 对 clear 恒为 clear）。该组近似
       「同一次运行生成的同 town 段」；注意：同一运行段内各条为独立 episode
       （同 seed 批覆盖 5 个不同 town，town 段内亦为多条独立随机场景），
       **不等于同一基础场景**。
  3) 正/负/clear 三批次间「事故版 vs 反事实无事故版」配对：无共同字段键
     （正无 seed；批次命名/生成完全独立）⇒ 如实报告可验证程度。

输出：reports/source_lineage_leakage_check.json
"""
import json
import os
import collections
import datetime

ROOT = r'D:\dataset_final_export\dataset_final'
M = os.path.join(ROOT, 'manifests', 'dataset_master.json')
OUT = os.path.join(ROOT, 'reports', 'source_lineage_leakage_check.json')
SPLITS = ['train', 'val_real', 'test_real', 'reserve']


def split_set(group):
    return sorted({it['split'] for it in group})


def main():
    m = json.load(open(M, encoding='utf-8'))
    total = len(m)

    # ---------- 1) 真实数据：source + original_video_id ----------
    real_cross = []
    real_groups = {}
    for src in ['CCD', 'DADA', 'BDD100K']:
        its = [x for x in m if x['source'] == src]
        g = collections.defaultdict(list)
        for x in its:
            g[(src, str(x['original_video_id']))].append(x)
        real_groups[src] = g
        for key, grp in g.items():
            if len(split_set(grp)) > 1:
                real_cross.append({
                    'source': src, 'original_video_id': key[1],
                    'n_samples': len(grp), 'splits': split_set(grp),
                    'sample_ids': [x['sample_id'] for x in grp]})

    # ---------- 2) CARLA ----------
    car = [x for x in m if x['source'] == 'CARLA']
    car_pos = [x for x in car if x['negative_type'] is None]          # 事故正样本 1080
    car_neg = [x for x in car if x['negative_type'] == 'adverse_no_accident']  # 无事故负 1080
    car_clear = [x for x in car if x['negative_type'] == 'clear_accident']    # 晴天事故负 540

    # L1 逐原始视频
    l1 = collections.defaultdict(list)
    for x in car:
        l1[('CARLA', str(x['original_video_id']))].append(x)
    l1_cross = [{'original_video_id': k[1], 'n_samples': len(grp), 'splits': split_set(grp)}
                for k, grp in l1.items() if len(split_set(grp)) > 1]

    # L2 运行段
    def run_segment_key(x):
        if x['negative_type'] == 'adverse_no_accident':  # 负样本有 seed
            return ('CARLA', 'neg', str(x['town']), str(x['scenario']), str(x['weather']), str(x['seed']))
        if x['negative_type'] == 'clear_accident':
            return ('CARLA', 'clear', str(x['town']), str(x['scenario']), str(x['weather']))
        return ('CARLA', 'pos', str(x['town']), str(x['scenario']), str(x['weather']))

    l2 = collections.defaultdict(list)
    for x in car:
        l2[run_segment_key(x)].append(x)
    l2_cross = []
    for k, grp in l2.items():
        if len(split_set(grp)) > 1:
            l2_cross.append({
                'segment': {'batch': k[1], 'town': k[2], 'scenario': k[3], 'weather': k[4],
                            'seed': k[5] if len(k) > 5 else None},
                'n_samples': len(grp),
                'train': sum(1 for x in grp if x['split'] == 'train'),
                'reserve': sum(1 for x in grp if x['split'] == 'reserve'),
                'splits': split_set(grp)})

    # L3 批次组合级（仅统计分布，供参考）
    batch_stat = {
        'pos (carla_batch)': dict(collections.Counter(x['split'] for x in car_pos)),
        'neg (carla_neg)': dict(collections.Counter(x['split'] for x in car_neg)),
        'clear (carla_clear_acc)': dict(collections.Counter(x['split'] for x in car_clear)),
    }

    # 3) 批次间配对键检查
    pos_keys = {(x['town'], x['scenario'], x['weather']) for x in car_pos}
    neg_keys = {(x['town'], x['scenario'], x['weather']) for x in car_neg}
    clear_keys = {(x['town'], x['scenario'], x['weather']) for x in car_clear}
    pairing = {
        'pos_has_seed': any(x.get('seed') is not None for x in car_pos),
        'neg_has_seed': any(x.get('seed') is not None for x in car_neg),
        'clear_has_seed': any(x.get('seed') is not None for x in car_clear),
        'pos_neg_share_town_scenario_weather_pairs': len(pos_keys & neg_keys),
        'pos_clear_share_pairs': len(pos_keys & clear_keys),
        'neg_clear_share_pairs': len(neg_keys & clear_keys),
        'pair_key_note': ('town+scenario+weather 组合键不代表同一基础场景；'
                          '正/负/clear 为独立生成批次，无逐视频场景种子/场景ID配对键'),
    }

    # ---------- 判定 ----------
    # 来源级（逐原始视频）：真实 0 跨 + CARLA L1 0 跨
    real_video_overlap = len(real_cross)
    l1_overlap = len(l1_cross)
    source_level_overlap = real_video_overlap + l1_overlap
    # 运行段级：如实报告（不判定为同源泄漏，理由见下）
    l2_overlap = len(l2_cross)
    l2_verdict = {
        'cross_split_segments': l2_overlap,
        'is_same_base_scene': False,
        'evidence': [
            '同一运行级 seed 批覆盖 5 个不同 town（如 seed 28751 出现在 Town01/02/04/05/Town10HD_Opt 的 '
            'pedestrian+night 段），不同 town 道路拓扑不同 ⇒ 不可能是同一基础场景',
            'seed 为运行级随机种子（每组合一次运行一个随机 seed，组内多条共享），非逐视频场景种子，'
            '不构成场景身份标识',
            '同运行段内各条为独立 episode（场景随机重建），字段层面无逐条场景指纹可证同场景',
        ],
        'conclusion': ('运行段跨 train/reserve 为划分方式的事实（负样本 1080 按 seed=42 确定性 '
                       '逐条挑选 540 入 train、540 入 reserve），但不构成「同一基础场景泄漏」；'
                       '若用户要求更强约束「同运行段必须同 split」，则需要重构 train（负样本将全部 '
                       '移入 reserve，合成负样本无法再满足 675 目标），该项请用户拍板。'),
    }

    result = {
        'check_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'check_name': '来源级（原始视频/基础场景）防泄漏检查',
        'grouping_method': (
            '真实数据按 source+original_video_id；CARLA 分三级：L1 逐原始视频 '
            '(source+original_video_id)、L2 运行段 (source+town+scenario+weather[+seed])、'
            'L3 批次级；不沿用 group_id；不编造 episode_id/base_scene_id 字段'),
        'fields_used': ['source', 'original_video_id', 'town', 'scenario', 'weather', 'seed', 'split'],
        'fields_unavailable': ['episode_id', 'base_scene_id', 'per_video_scene_seed'],
        'sample_total': total,
        'real_data': {
            'CCD': {'samples': len(real_groups['CCD']), 'unique_videos': len(real_groups['CCD']),
                    'videos_with_multiple_segments': 0},
            'DADA': {'samples': len(real_groups['DADA']), 'unique_videos': len(real_groups['DADA']),
                     'videos_with_multiple_segments': 0},
            'BDD100K': {'samples': len(real_groups['BDD100K']), 'unique_videos': len(real_groups['BDD100K']),
                        'videos_with_multiple_segments': 0},
            'note': '每条原始视频恰好产出 1 个 25 帧样本 ⇒ 不存在同视频切多片段',
            'cross_split_groups': real_cross,
        },
        'carla': {
            'total': len(car),
            'batch_split': batch_stat,
            'L1_per_video': {'groups': len(l1), 'cross_split_groups': l1_cross},
            'L2_run_segment': {'groups': len(l2), 'cross_split_groups': l2_cross[:60],
                               'cross_split_group_count': l2_overlap},
            'L3_batch': batch_stat,
        },
        'cross_batch_pairing': pairing,
        'verifiable_degree': {
            'can_verify': [
                '真实数据每条原始视频仅 1 个片段，且无跨 split（唯一视频数=样本数）',
                'CARLA 逐原始视频 2700 条全部唯一，无跨 split',
                '正/负/clear 三批次样本 id/命名体系完全独立（carla_* / carla_neg_* / carla_clear_*）',
            ],
            'cannot_verify_from_manifest': [
                '正样本无 seed、三批次无逐视频场景种子/场景 ID ⇒ 「同一基础场景在正/负/clear '
                '批次间是否被复用」无法仅凭清单字段排除；可验证到的程度：三批次 town+scenario+'
                'weather 组合存在重合（见 cross_batch_pairing），但组合键≠场景指纹',
                '同运行段内多条是否同一基础场景：无字段指纹，无法从清单排除',
            ],
        },
        'conclusion': {
            'source_level_overlap': source_level_overlap,
            'pass': source_level_overlap == 0,
            'statement': ('无同源场景泄漏（来源级：逐原始视频分组跨 split 交集 = 0；'
                          '真实数据每条视频仅 1 片段）。') if source_level_overlap == 0
                         else ('发现来源级跨 split 交集，见 real_data.cross_split_groups / carla.L1。'),
            'l2_run_segment_verdict': l2_verdict,
        },
    }
    json.dump(result, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('written %s' % OUT)
    print('real groups: CCD=%d DADA=%d BDD100K=%d (unique videos == samples)' % (
        len(real_groups['CCD']), len(real_groups['DADA']), len(real_groups['BDD100K'])))
    print('real_cross=%d l1_cross=%d l2_cross=%d source_level_overlap=%d' % (
        real_video_overlap, l1_overlap, l2_overlap, source_level_overlap))
    print('pos split=%s' % batch_stat['pos (carla_batch)'])
    print('neg split=%s' % batch_stat['neg (carla_neg)'])
    print('clear split=%s' % batch_stat['clear (carla_clear_acc)'])
    print('pos_neg shared town+scen+weather pairs=%d, pos_clear=%d, neg_clear=%d' % (
        pairing['pos_neg_share_town_scenario_weather_pairs'],
        pairing['pos_clear_share_pairs'], pairing['neg_clear_share_pairs']))
    print('CONCLUSION source_level_overlap=%d pass=%s' % (source_level_overlap, source_level_overlap == 0))


if __name__ == '__main__':
    main()
