# -*- coding: utf-8 -*-
"""make_freeze_v1.0.py — v1.0 正式冻结产物生成（用户选择 a：文档化口径直接冻结）

只读 master/四清单，生成到 freeze_v1.0/ 下：
  version_v1.0.json        —— 版本元数据（dataset_version、冻结日期、判定、TTA 可评估范围）
  frozen_manifest_hashes.json —— master + 四 split json 的 sha256/条数（快照指针，不改原文件）
  split_hashes.json        —— 各 split sample_id 集合 sha256
  final_distribution_frozen.json —— 冻结口径统计快照
  audit_references.json    —— 既有审计产物归档引用（路径 + 可选哈希）
  tta_eval_scope.json      —— TTA 可评估范围实测（CARLA 事故 / DADA / pe=true / CCD 排除）
"""
import json
import os
import hashlib
import datetime

ROOT = r'D:\dataset_final_export\dataset_final'
M_DIR = os.path.join(ROOT, 'manifests')
R_DIR = os.path.join(ROOT, 'reports')
FZ = os.path.join(ROOT, 'freeze_v1.0')
os.makedirs(FZ, exist_ok=True)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def sha256_text(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def main():
    master = json.load(open(os.path.join(M_DIR, 'dataset_master.json'), encoding='utf-8'))
    splits = {}
    for sp in ['train', 'val_real', 'test_real', 'reserve']:
        splits[sp] = json.load(open(os.path.join(M_DIR, sp + '.json'), encoding='utf-8'))

    # 1) version
    # TTA 评价范围（用户口径）：collision_frame 有真实标注的事故正样本 = CARLA 事故正 1080 + DADA 25
    carla_acc = [x for x in master if x['source'] == 'CARLA' and x['target'] == 1]
    carla_clear = [x for x in master if x['source'] == 'CARLA' and x['negative_type'] == 'clear_accident']
    dada = [x for x in master if x['source'] == 'DADA']
    tta_base = carla_acc + dada
    tta_pe = [x for x in tta_base if x['prediction_eligible'] is True]
    ccd_pos = [x for x in master if x['source'] == 'CCD' and x['target'] == 1]
    ccd_pos_cf_null = [x for x in ccd_pos if x['collision_frame'] is None]
    version = {
        'dataset_version': '1.0',
        'freeze_date': '2026-10-05',
        'freeze_decision': 'v1.0 正式冻结，可进入 baseline 训练（2026-10-05 用户选择方案 a：B1 文档化后直接冻结）',
        'audit_verdict': 'C CONDITIONAL PASS -> 经用户决策 B1 文档化后转为正式冻结',
        'total_samples': len(master),
        'split_counts': {sp: len(v) for sp, v in splits.items()},
        'tta_eval_scope': {
            'note': 'TTA/time-to-accident/collision lead time 仅在 collision_frame 有真实标注的事故正样本上计算，'
                    '不对 CCD 做自动估算并当作真值',
            'carla_accident_pos_samples': len(carla_acc),
            'dada_samples': len(dada),
            'tta_total': len(tta_base),
            'tta_prediction_eligible_true': len(tta_pe),
            'carla_clear_accident_neg_cf20_note': (
                '另有 CARLA clear_accident 负样本 %d 条 collision_frame=20（生成真值），'
                '属负样本，不计入 TTA 正样本评价' % len(carla_clear)),
            'ccd_real_pos_excluded': len(ccd_pos),
            'ccd_real_pos_cf_null': len(ccd_pos_cf_null),
            'exclusion_note': '486 条 CCD 真实恶劣天气事故正样本（collision_frame=null）不在 TTA 评价范围，'
                              '仅用于事故检测/分类等不依赖 collision_frame 的实验',
        },
        'generated_by': 'scripts/make_freeze_v1.0.py',
    }
    json.dump(version, open(os.path.join(FZ, 'version_v1.0.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)

    # 2) frozen manifest hashes（快照指针，不改原文件）
    manifest_files = {
        'dataset_master.json': (len(master), sha256_file(os.path.join(M_DIR, 'dataset_master.json'))),
    }
    for sp, items in splits.items():
        manifest_files[sp + '.json'] = (len(items), sha256_file(os.path.join(M_DIR, sp + '.json')))
    fz_manifest = {
        'note': '冻结快照/哈希指针；原文件未改写，以现有 v1.0 清单为准',
        'files': {k: {'count': c, 'sha256': h} for k, (c, h) in manifest_files.items()},
    }
    json.dump(fz_manifest, open(os.path.join(FZ, 'frozen_manifest_hashes.json'), 'w',
                                encoding='utf-8'), ensure_ascii=False, indent=2)

    # 3) split sample_id 集合哈希
    split_hashes = {}
    for sp, items in splits.items():
        ids = sorted(x['sample_id'] for x in items)
        split_hashes[sp] = {'count': len(ids), 'sample_id_set_sha256': sha256_text('\n'.join(ids))}
    split_hashes['_master'] = {'count': len(master),
                               'sample_id_set_sha256': sha256_text('\n'.join(sorted(x['sample_id'] for x in master)))}
    json.dump(split_hashes, open(os.path.join(FZ, 'split_hashes.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)

    # 4) final_distribution 冻结口径快照
    import collections
    dist = {
        'total': len(master),
        'frames_total': len(master) * 25,
        'split': dict(collections.Counter(x['split'] for x in master)),
        'target': dict(collections.Counter(x['target'] for x in master)),
        'domain': dict(collections.Counter(x['domain'] for x in master)),
        'weather': dict(collections.Counter(x['weather'] for x in master)),
        'source': dict(collections.Counter(x['source'] for x in master)),
        'accident': dict(collections.Counter(x['accident'] for x in master)),
        'negative_type': dict(collections.Counter(str(x['negative_type']) for x in master)),
        'prediction_eligible': dict(collections.Counter(x['prediction_eligible'] for x in master)),
        'train': {
            'total': 2700, 'syn': sum(1 for x in master if x['split'] == 'train' and x['domain'] == 'synthetic'),
            'real': sum(1 for x in master if x['split'] == 'train' and x['domain'] == 'real'),
            'pos': sum(1 for x in master if x['split'] == 'train' and x['target'] == 1),
            'neg': sum(1 for x in master if x['split'] == 'train' and x['target'] == 0),
            'adverse_noaccident': sum(1 for x in master if x['split'] == 'train' and x['negative_type'] == 'adverse_no_accident'),
            'clear_accident': sum(1 for x in master if x['split'] == 'train' and x['negative_type'] == 'clear_accident'),
        },
    }
    json.dump(dist, open(os.path.join(FZ, 'final_distribution_frozen.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)

    # 5) audit references
    refs = []
    for f in sorted(os.listdir(R_DIR)):
        if f.startswith(('audit_', 'final_acceptance', 'spot_')):
            p = os.path.join(R_DIR, f)
            if os.path.isfile(p):
                refs.append({'file': 'reports/' + f, 'sha256': sha256_file(p)})
    refs.append({'file': 'reports/spot_check/sheets/（36 张目检图）', 'sha256': '-'})
    json.dump({'note': '既有审计产物归档引用（哈希供核对，未移动原文件）', 'references': refs},
              open(os.path.join(FZ, 'audit_references.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)

    print('DONE freeze: master=%d tta_total=%d tta_pe=%d carla_acc=%d dada=%d ccd_pos_excluded=%d ccd_pos_cf_null=%d' % (
        len(master), len(tta_base), len(tta_pe), len(carla_acc), len(dada), len(ccd_pos), len(ccd_pos_cf_null)))


if __name__ == '__main__':
    main()
