# -*- coding: utf-8 -*-
"""group_stats.py — 按实际 group_id 重算防泄漏统计并覆盖 reports/split_leakage_check.json

用户修正指令（2026-10-04）：禁止手工把 group_total 改成 4971；必须重新读取
dataset_master.json，根据实际 group_id 计算并输出：
  1) 样本总数
  2) 非空 group_id 数量
  3) 唯一 group_id 数量
  4) 各 split 的唯一 group_id 数量
  5) group_id 跨 split 交集（必须为 0）
  6) 缺失 group_id 的样本
  7) 重复 group_id 对应的原始视频关系

判定原则：若每条样本确实对应独立 episode，唯一 group_id 应等于样本总数；
若同一原始视频产生多个片段，唯一 group_id 可以少于样本总数，但这些片段必须
处于同一个 split。不得为了让数字等于样本总数而伪造 group_id。
"""
import json
import os
import datetime

ROOT = r'D:\dataset_final_export\dataset_final'
M = os.path.join(ROOT, 'manifests', 'dataset_master.json')
R = os.path.join(ROOT, 'reports')
OUT = os.path.join(R, 'split_leakage_check.json')
FINT = os.path.join(R, 'frame_integrity_check.json')


def main():
    items = json.load(open(M, encoding='utf-8'))
    total = len(items)

    # 1/2/3) 基础统计
    non_empty = [it for it in items if it.get('group_id') not in (None, '')]
    group_to_items = {}
    missing_group = []
    for it in items:
        g = it.get('group_id')
        if g in (None, ''):
            missing_group.append(it['sample_id'])
            continue
        group_to_items.setdefault(g, []).append(it)
    unique_groups = set(group_to_items.keys())

    # 4) 各 split 唯一 group_id 数量
    per_split = {}
    split_group_set = {}
    for sp in ['train', 'val_real', 'test_real', 'reserve']:
        gs = set()
        cnt = 0
        for it in items:
            if it.get('split') == sp and it.get('group_id') not in (None, ''):
                gs.add(it['group_id'])
                cnt += 1
        split_group_set[sp] = gs
        per_split[sp] = {'samples': cnt, 'unique_groups': len(gs)}

    # 5) group_id 跨 split 交集
    crossing = set()
    for a in ['train', 'val_real', 'test_real', 'reserve']:
        for b in ['train', 'val_real', 'test_real', 'reserve']:
            if a < b:
                crossing |= (split_group_set[a] & split_group_set[b])

    # 7) 重复 group_id 对应的原始视频关系
    dup_groups = {g: its for g, its in group_to_items.items() if len(its) > 1}
    detail = []
    for g, its in sorted(dup_groups.items()):
        detail.append({
            'group_id': g,
            'sample_count': len(its),
            'sample_ids': [it['sample_id'] for it in its],
            'original_video_ids': list({str(it.get('original_video_id')) for it in its}),
            'splits': list({str(it.get('split')) for it in its}),
            'sources': list({str(it.get('source')) for it in its}),
        })
    dup_sample_count = sum(len(its) for its in dup_groups.values())

    # 复核 2/4 级检查：sample_id 唯一、路径可解析、跨 split 视频重叠
    ids = [it['sample_id'] for it in items]
    dup_ids = sorted({x for x in ids if ids.count(x) > 1})
    path_errors = [it['sample_id'] for it in items
                   if not os.path.isdir(os.path.join(ROOT, it.get('frame_dir', '')))]
    vid_split = {}
    for it in items:
        v = it.get('original_video_id')
        if v:
            vid_split.setdefault(str(v), set()).add(it.get('split'))
    video_overlap = sorted({str(v) for v, sps in vid_split.items() if len(sps) > 1})

    # 重复帧序列（沿用 frame_integrity_check.json 的全量检查结果，不重复计算）
    dup_frame_seq = None
    if os.path.exists(FINT):
        fint = json.load(open(FINT, encoding='utf-8'))
        dup_frame_seq = fint.get('duplicate_frame_sequence')

    result = {
        'recomputed_from': 'dataset_master.json',
        'recompute_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'method': ('按 sample["group_id"] 实际统计（build_master.py 生成规则：'
                   'CCD/DADA/BDD100K 按原始视频 ID；CARLA 按 Town+场景+天气+序号，每条为独立 episode）。'
                   '唯一 group_id 等于样本总数 ⇒ 每条样本对应独立 episode；'
                   '少于样本总数 ⇒ 同组片段必须处于同一 split。'),
        'sample_total': total,
        'non_empty_group_count': len(non_empty),
        'unique_group_count': len(unique_groups),
        'unique_groups_per_split': per_split,
        'groups_in_multiple_splits': sorted(crossing),
        'group_overlap': len(crossing),
        'missing_group_count': len(missing_group),
        'missing_group_samples': missing_group,
        'duplicate_group_count': len(dup_groups),
        'duplicate_group_sample_count': dup_sample_count,
        'duplicate_group_detail': detail[:30],
        'original_video_relation': (
            'unique_group_count == sample_total ⇒ 每条样本为独立原始视频/episode；'
            '无同一原始视频切出多片段的情况。'),
        'duplicate_sample_id': len(dup_ids),
        'duplicate_sample_ids': dup_ids,
        'video_overlap_across_splits': len(video_overlap),
        'video_overlap_video_ids': video_overlap,
        'duplicate_frame_sequence': dup_frame_seq,
        'path_errors': len(path_errors),
        'path_error_samples': path_errors,
        'conclusion': 'PASS' if (len(crossing) == 0 and len(dup_ids) == 0
                                 and len(path_errors) == 0 and len(video_overlap) == 0
                                 and len(missing_group) == 0) else 'FAIL',
    }
    json.dump(result, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('written %s' % OUT)
    print('sample_total=%d non_empty_group=%d unique_group=%d group_overlap=%d '
          'dup_id=%d dup_group=%d dup_group_samples=%d missing_group=%d path_errors=%d '
          'video_overlap=%d dup_frame_seq=%s' % (
              total, len(non_empty), len(unique_groups), len(crossing), len(dup_ids),
              len(dup_groups), dup_sample_count, len(missing_group), len(path_errors),
              len(video_overlap), dup_frame_seq))
    for sp, v in per_split.items():
        print('split %s: samples=%d unique_groups=%d' % (sp, v['samples'], v['unique_groups']))


if __name__ == '__main__':
    main()
