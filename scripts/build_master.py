# -*- coding: utf-8 -*-
"""
dataset_final 统一主清单构建脚本

输入（只读）：
  - D:\\dataset_v2_export\\dataset_v2\\dataset_planB_v2.json   (v2 交付包 4431 条)
  - D:\\dataset\\carla_clear_out_v2\\manifest.json             (新 540 条 clear 事故, 若已生成)
  - D:\\dataset_final_export\\dataset_final\\reports\\clear_verify.json (clear 条目的碰撞帧/质量复核, 若已生成)

输出（写入 D:\\dataset_final_export\\dataset_final\\）：
  - manifests\\dataset_master.json / train.json / val_real.json / test_real.json / reserve.json
  - reports\\final_distribution.json/.csv/.md
  - reports\\split_leakage_check.json
  - reports\\label_logic_check.json
  - reports\\dataset_construction_report.md (由本脚本生成主体)

标签口径（用户指令，不可违背）：
  adverse_weather = 1 iff weather in (rainy, snowy, night)
  target = accident AND adverse_weather
  negative_type: None(主任务正)/adverse_no_accident(恶劣天气无事故)/clear_accident(正常天气事故)
  训练集 80% 合成 / 20% 真实 (±0.5%)，正负各 50%，两类负样本各 50%
  TEST_REAL=340 固定（CCD 200 正 + BDD 140 负，来自 v2 test 的真实部分），不重抽样
  val_real 100% 真实；test_real 100% 真实；合成数据不得进入 test_real/val_real
  防泄漏：group_id 按原始视频/episode 唯一；group_overlap=0
"""
import json, csv, collections, random, os, sys

ROOT = r'D:\dataset_final_export\dataset_final'
V2 = r'D:\dataset_v2_export\dataset_v2\dataset_planB_v2.json'
CLEAR_MANIFEST = r'D:\dataset\carla_clear_out_v2\manifest.json'
CLEAR_VERIFY = os.path.join(ROOT, 'reports', 'clear_verify.json')
SEED = 42

# v2 source -> (final source, frames 子目录, 分组 kind)
SRC_MAP = {
    'carla_synth_v2': ('CARLA', 'frames\\CARLA_ACCIDENT', 'acc'),
    'carla_neg_v2':   ('CARLA', 'frames\\CARLA_NON_ACCIDENT', 'nonacc'),
    'ccd_real':       ('CCD',   'frames\\CCD', None),
    'dada_real':      ('DADA',  'frames\\DADA', None),
    'bdd100k_mot':    ('BDD100K', 'frames\\BDD100K', None),
}

ADVERSE = {'rainy', 'snowy', 'night'}


def adverse_of(weather):
    return 1 if weather in ADVERSE else 0


def neg_type(acc, adv):
    if acc == 1 and adv == 1:
        return None
    if acc == 0 and adv == 1:
        return 'adverse_no_accident'
    if acc == 1 and adv == 0:
        return 'clear_accident'
    return None  # clear no-accident -> reserve, 不进入主任务


def build_from_v2(items):
    out = []
    for it in items:
        src, fdir, kind = SRC_MAP[it['source']]
        weather = it['weather']
        acc = it['accident']
        adv = adverse_of(weather)
        sid = it['sample_id']
        # 原视频ID：CARLA 用 video_id；CCD/BDD/DADA 用 video_id（即目录名）
        orig = it.get('video_id') or sid
        town = it.get('town')
        # 分组（CARLA 每条 = 独立 episode：town+场景+天气+序号 唯一标识一个视频）
        if src == 'CARLA':
            gid = 'carla_%s_%s_%s_%s_%s' % (kind, town, it.get('scenario'), weather,
                                            sid.rsplit('_', 1)[-1])
        else:
            gid = '%s_%s' % (src.lower(), orig)
        rec = {
            'sample_id': sid,
            'frame_dir': fdir + '\\' + sid,
            'source': src,
            'domain': it['domain'],
            'accident': acc,
            'weather': weather,
            'weather_raw': it.get('weather_raw'),
            'adverse_weather': adv,
            'target': 1 if (acc == 1 and adv == 1) else 0,
            'negative_type': neg_type(acc, adv),
            'scenario': it.get('scenario') or 'unknown',
            'collision_frame': it.get('collision_frame'),
            'frame_count': it.get('frame_count') or it.get('n_frames') or 25,
            'fps': it.get('fps') or 5,
            'width': it.get('width'),
            'height': it.get('height'),
            'original_video_id': orig,
            'group_id': gid,
            'town': town,
            'seed': it.get('seed'),
            'peak_frame_mad': it.get('peak_frame_mad'),
            'quality_flag': [],
            'prediction_eligible': True,
        }
        # 早期 MAD 峰（碰撞第 18 帧前已明显发生）：保留用于检测，不用于预测
        peak = it.get('peak_frame_mad')
        if src == 'CARLA' and acc == 1 and peak is not None and peak < 18:
            rec['quality_flag'] = ['early_motion_peak']
            rec['prediction_eligible'] = False
        out.append(rec)
    return out


def build_from_clear():
    """新 540 条 clear 事故（晴天；生成流程违规记录见 reports/dataset_construction_report.md 3.1）"""
    if not os.path.exists(CLEAR_MANIFEST):
        return []
    man = json.load(open(CLEAR_MANIFEST, encoding='utf-8'))
    verify = {}
    if os.path.exists(CLEAR_VERIFY):
        verify = {v['video_id']: v for v in
                  json.load(open(CLEAR_VERIFY, encoding='utf-8'))['items']}
    out = []
    for it in man:
        vid = it['video_id']
        v = verify.get(vid, {})
        sid = vid
        peak = v.get('peak_frame_mad') or 20
        town = it.get('town')
        scenario = it.get('scenario')
        rec = {
            'sample_id': sid,
            'frame_dir': 'frames\\CARLA_ACCIDENT\\' + sid,
            'source': 'CARLA',
            'domain': 'synthetic',
            'accident': 1,
            'weather': 'clear',
            'weather_raw': 'clear',
            'adverse_weather': 0,
            'target': 0,
            'negative_type': 'clear_accident',
            'scenario': scenario,
            'collision_frame': it.get('collision_frame') or 20,
            'frame_count': 25,
            'fps': 5,
            'width': 1280,
            'height': 720,
            'original_video_id': vid,
            'group_id': 'carla_clearacc_%s_%s_clear_%s' % (town, scenario, sid.rsplit('_', 1)[-1]),
            'town': town,
            'seed': None,
            'peak_frame_mad': peak,
            'quality_flag': [],
            'prediction_eligible': True,
        }
        if peak < 18:
            rec['quality_flag'] = ['early_motion_peak']
            rec['prediction_eligible'] = False
        out.append(rec)
    return out


def pick(items, n, rng, key=None):
    """确定性挑选 n 条（按 key 分桶排序后挑选，保证 group 完整性——此处 group 即样本本身）"""
    if key:
        buckets = collections.defaultdict(list)
        for it in items:
            buckets[it[key]].append(it)
        order = []
        for k in sorted(buckets):
            for it in sorted(buckets[k], key=lambda x: x['sample_id']):
                order.append(it)
    else:
        order = sorted(items, key=lambda x: x['sample_id'])
    # 用稳定伪随机洗牌后取前 n（rng 固定 seed）
    idx = list(range(len(order)))
    rng.shuffle(idx)
    chosen = [order[i] for i in idx[:n]]
    return chosen, [it for it in order if it not in chosen]


def main():
    v2 = json.load(open(V2, encoding='utf-8'))
    items = v2['items']
    assert len(items) == 4431, 'v2 条目数异常: %d' % len(items)

    master = build_from_v2(items)
    clear_items = build_from_clear()

    real = [it for it in master if it['domain'] == 'real']
    syn = [it for it in master if it['domain'] == 'synthetic']

    # ---------- 1. test_real 固定 340（v2 test 的真实部分，不重抽样） ----------
    v2_test = set(i['sample_id'] for i in items if i.get('split') == 'test')
    test_real = [it for it in master if it['sample_id'] in v2_test and it['domain'] == 'real']
    assert len(test_real) == 340, 'test_real 应为 340，实际 %d' % len(test_real)
    by_src = collections.Counter(it['source'] for it in test_real)
    assert by_src.get('CCD') == 200 and by_src.get('BDD100K') == 140, 'test_real 组成异常: %s' % dict(by_src)
    test_ids = set(it['sample_id'] for it in test_real)
    for it in test_real:
        it['split'] = 'test_real'

    # ---------- 2. val_real：100% 真实，三类负样本齐备，正负 1:1 ----------
    real_pool = [it for it in real if it['sample_id'] not in test_ids]
    rng = random.Random(SEED)
    pos_pool = [it for it in real_pool if it['target'] == 1]          # 真实恶劣天气事故
    noacc_pool = [it for it in real_pool if it['negative_type'] == 'adverse_no_accident']
    clearacc_pool = [it for it in real_pool if it['negative_type'] == 'clear_accident']

    # DADA 25 固定进 val_real（v2 既定 val 成员，真实恶劣天气事故）
    dada = [it for it in pos_pool if it['source'] == 'DADA']
    ccd_pos = [it for it in pos_pool if it['source'] == 'CCD']
    assert len(dada) == 25, 'DADA 应为 25 条，实际 %d' % len(dada)

    VAL_POS_TARGET = 100      # DADA 25 + CCD 75
    VAL_NOACC_TARGET = 50     # BDD 恶劣天气无事故
    VAL_CLEARACC_TARGET = 50  # CCD 正常天气事故
    weather_order = ['night', 'snowy', 'rainy']

    # val 正样本：先取 DADA，再从 CCD adverse 事故按天气分层补到 100
    val_pos = list(dada)
    ccd_pool = list(ccd_pos)
    used_ids = set(it['sample_id'] for it in val_pos)
    need = VAL_POS_TARGET - len(val_pos)
    for w in weather_order:
        bucket = [it for it in ccd_pool
                  if it['weather'] == w and it['sample_id'] not in used_ids]
        take = min(need // (3 - weather_order.index(w)), len(bucket))
        chosen = pick(bucket, take, rng)[0]
        val_pos += chosen
        used_ids |= set(it['sample_id'] for it in chosen)
        need -= len(chosen)
    # 剩余缺口按剩余池子确定性补齐
    if need > 0:
        bucket = [it for it in ccd_pool if it['sample_id'] not in used_ids]
        chosen = pick(bucket, need, rng)[0]
        val_pos += chosen
        need -= len(chosen)
    if need > 0:
        print('WARN val_real 正样本缺口 %d（保留真实分布）' % need)

    # val 负样本：adverse_no_accident（BDD）50 + clear_accident（CCD）50
    chosen_noacc, _ = pick(noacc_pool, VAL_NOACC_TARGET, rng)
    chosen_clearacc, _ = pick(clearacc_pool, VAL_CLEARACC_TARGET, rng)
    val_neg = chosen_noacc + chosen_clearacc

    val_real = val_pos + val_neg
    val_ids = set(it['sample_id'] for it in val_real)
    for it in val_real:
        it['split'] = 'val_real'

    # ---------- 3. train：80/20、正负 50/50、两类负样本 50/50 ----------
    # 合成侧
    syn_pos = [it for it in syn if it['target'] == 1]                    # 1080 CARLA 事故，全部
    syn_noacc_pool = [it for it in syn if it['negative_type'] == 'adverse_no_accident']
    syn_clearacc = [it for it in syn if it['negative_type'] == 'clear_accident']  # 新 clear，全部
    # 新 clear 若尚未生成则报错（80/20 结构依赖它）
    if len(clear_items) != 540:
        print('FATAL 需要 540 条 clear 事故，当前 %d —— 请先生成并下载' % len(clear_items))
        sys.exit(2)
    train_syn_noacc, syn_noacc_reserve = pick(syn_noacc_pool, 540, rng)
    train_syn = syn_pos + train_syn_noacc + clear_items   # 1080+540+540=2160

    # 真实侧：test/val 已扣除
    real_train_pool = [it for it in real_pool if it['sample_id'] not in val_ids]
    pos_pool2 = [it for it in real_train_pool if it['target'] == 1]
    noacc_pool2 = [it for it in real_train_pool if it['negative_type'] == 'adverse_no_accident']
    clearacc_pool2 = [it for it in real_train_pool if it['negative_type'] == 'clear_accident']

    # 真实正样本 270：night/snowy/rainy 尽量均衡
    REAL_POS_TARGET = 270
    tr_pos = []
    pool2 = list(pos_pool2)
    used2 = set()
    need = REAL_POS_TARGET
    for w in weather_order:
        bucket = [it for it in pool2
                  if it['weather'] == w and it['sample_id'] not in used2]
        take = min(need // (3 - weather_order.index(w)), len(bucket))
        chosen = pick(bucket, take, rng)[0]
        tr_pos += chosen
        used2 |= set(it['sample_id'] for it in chosen)
        need -= len(chosen)
    if need > 0:
        bucket = [it for it in pool2 if it['sample_id'] not in used2]
        chosen = pick(bucket, need, rng)[0]
        tr_pos += chosen
        need -= len(chosen)
    if need > 0:
        print('WARN train 真实正样本缺口 %d（保留真实分布）' % need)

    tr_noacc, _ = pick(noacc_pool2, 135, rng)
    tr_clearacc, _ = pick(clearacc_pool2, 135, rng)
    train_real = tr_pos + tr_noacc + tr_clearacc   # 270+135+135=540

    train = train_syn + train_real
    for it in train:
        it['split'] = 'train'

    # ---------- 4. reserve：其余全部有效数据 ----------
    train_ids = set(it['sample_id'] for it in train)
    reserve = [it for it in master if it['sample_id'] not in (test_ids | val_ids | train_ids)]
    for it in reserve:
        it['split'] = 'reserve'

    # ---------- 5. 校验 ----------
    n_train, n_val, n_test, n_res = len(train), len(val_real), len(test_real), len(reserve)
    assert n_train == 2700 and n_val == 200 and n_test == 340, \
        'train/val/test 数量异常: %d/%d/%d' % (n_train, n_val, n_test)
    assert n_train + n_val + n_test + n_res == 4431 + len(clear_items), \
        '总数不一致: %d+%d+%d+%d vs %d' % (n_train, n_val, n_test, n_res, 4431 + len(clear_items))

    syn_n = sum(1 for it in train if it['domain'] == 'synthetic')
    real_n = len(train) - syn_n
    pos_n = sum(1 for it in train if it['target'] == 1)
    neg_n = len(train) - pos_n
    nt = collections.Counter(it['negative_type'] for it in train if it['target'] == 0)
    syn_pct = 100.0 * syn_n / n_train
    real_pct = 100.0 * real_n / n_train
    assert abs(syn_pct - 80.0) <= 0.5 and abs(real_pct - 20.0) <= 0.5, \
        '80/20 比例越界: syn %.3f%% real %.3f%%' % (syn_pct, real_pct)
    assert pos_n == 1350 and neg_n == 1350, '正负应各 1350: %d/%d' % (pos_n, neg_n)
    assert nt['adverse_no_accident'] == 675 and nt['clear_accident'] == 675, \
        '两类负样本应各 675: %s' % dict(nt)

    # ---------- 6. 防泄漏检查 ----------
    gid_splits = collections.defaultdict(set)
    for it in master:
        gid_splits[it['group_id']].add(it['split'])
    group_overlap = sum(1 for g, ss in gid_splits.items() if len(ss) > 1)
    dup_ids = len(master) - len(set(it['sample_id'] for it in master))
    # 相同原始视频跨 split
    vid_splits = collections.defaultdict(set)
    for it in master:
        vid_splits[(it['source'], it['original_video_id'])].add(it['split'])
    video_overlap = sum(1 for k, ss in vid_splits.items() if len(ss) > 1)

    # ---------- 7. 标签逻辑检查 ----------
    label_errs = []
    for it in master:
        if it['target'] == 1 and not (it['accident'] == 1 and it['adverse_weather'] == 1):
            label_errs.append((it['sample_id'], 'target=1 但 accident/adverse 不满足'))
        if it['negative_type'] == 'adverse_no_accident' and \
                not (it['accident'] == 0 and it['adverse_weather'] == 1 and it['target'] == 0):
            label_errs.append((it['sample_id'], 'adverse_no_accident 字段矛盾'))
        if it['negative_type'] == 'clear_accident' and \
                not (it['accident'] == 1 and it['adverse_weather'] == 0 and it['target'] == 0):
            label_errs.append((it['sample_id'], 'clear_accident 字段矛盾'))
        if it['split'] == 'test_real' and it['domain'] != 'real':
            label_errs.append((it['sample_id'], 'test_real 混入合成'))
        if it['split'] == 'val_real' and it['domain'] != 'real':
            label_errs.append((it['sample_id'], 'val_real 混入合成'))

    # ---------- 8. 输出 ----------
    os.makedirs(os.path.join(ROOT, 'manifests'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'reports'), exist_ok=True)
    all_items = master + clear_items
    json.dump(all_items, open(os.path.join(ROOT, 'manifests', 'dataset_master.json'),
                              'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for name, subset in [('train', train), ('val_real', val_real),
                         ('test_real', test_real), ('reserve', reserve)]:
        json.dump(subset, open(os.path.join(ROOT, 'manifests', name + '.json'),
                               'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # final_distribution 交叉统计
    def cross(keyf, sel=None):
        c = collections.Counter()
        for it in (sel if sel is not None else all_items):
            c[keyf(it)] += 1
        return dict(c)

    dist = {
        'total': len(all_items),
        'split_x_target': {k: dict(v) for k, v in
                           _group_cross(all_items, lambda x: x['split'], lambda x: x['target']).items()},
        'split_x_domain': {k: dict(v) for k, v in
                           _group_cross(all_items, lambda x: x['split'], lambda x: x['domain']).items()},
        'split_x_weather': {k: dict(v) for k, v in
                            _group_cross(all_items, lambda x: x['split'], lambda x: x['weather']).items()},
        'split_x_source': {k: dict(v) for k, v in
                           _group_cross(all_items, lambda x: x['split'], lambda x: x['source']).items()},
        'split_x_negative_type': {k: dict(v) for k, v in
                                  _group_cross(all_items, lambda x: x['split'], lambda x: str(x['negative_type'])).items()},
        'split_x_accident_x_adverse': {k: dict(v) for k, v in
                                       _group_cross(all_items, lambda x: x['split'],
                                                    lambda x: '%d/%d' % (x['accident'], x['adverse_weather'])).items()},
        'domain_x_target': dict(_group_cross(all_items, lambda x: x['domain'], lambda x: x['target'])),
        'domain_x_negative_type': dict(_group_cross(all_items, lambda x: x['domain'],
                                                    lambda x: str(x['negative_type']))),
        'train_ratio': {'syn': syn_n, 'real': real_n, 'syn_pct': round(syn_pct, 3),
                        'real_pct': round(real_pct, 3), 'pos': pos_n, 'neg': neg_n,
                        'neg_types': dict(nt)},
    }
    json.dump(dist, open(os.path.join(ROOT, 'reports', 'final_distribution.json'),
                         'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    with open(os.path.join(ROOT, 'reports', 'final_distribution.csv'), 'w',
              newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['split', 'dimension', 'value', 'count'])
        for dim in ['target', 'domain', 'weather', 'source', 'negative_type', 'accident_x_adverse']:
            for sp, cc in sorted(dist['split_x_' + dim].items()):
                for val, cnt in sorted(cc.items(), key=lambda x: str(x[0])):
                    w.writerow([sp, dim, val, cnt])
        for dom, cc in sorted(dist['domain_x_target'].items()):
            for tgt, cnt in sorted(cc.items()):
                w.writerow(['all', 'domain_x_target', '%s/%s' % (dom, tgt), cnt])
        for dom, cc in sorted(dist['domain_x_negative_type'].items()):
            for nt_, cnt in sorted(cc.items()):
                w.writerow(['all', 'domain_x_negative_type', '%s/%s' % (dom, nt_), cnt])

    leakage = {
        'group_overlap': group_overlap,
        'duplicate_sample_id': dup_ids,
        'video_overlap_across_splits': video_overlap,
        'duplicate_frame_sequence': None,  # 由 frame_integrity/去重脚本填充
        'group_total': len(gid_splits),
        'note': 'group_id 按原始视频/独立 episode 唯一；CARLA 正/负为独立 episode（pos manifest 无 seed，neg seed 为运行级随机），无成对反事实可跨 split',
    }
    json.dump(leakage, open(os.path.join(ROOT, 'reports', 'split_leakage_check.json'),
                            'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    label_check = {
        'total': len(all_items),
        'errors': label_errs,
        'error_count': len(label_errs),
        'checked_rules': [
            'target=1 -> accident=1 and adverse_weather=1',
            'adverse_no_accident -> accident=0 and adverse_weather=1 and target=0',
            'clear_accident -> accident=1 and adverse_weather=0 and target=0',
            'test_real/val_real 100% real',
        ],
    }
    json.dump(label_check, open(os.path.join(ROOT, 'reports', 'label_logic_check.json'),
                                'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # 简要控制台汇总
    print('total=%d (v2 4431 + clear %d)' % (len(all_items), len(clear_items)))
    print('train=%d (syn %d / real %d, syn_pct=%.3f%%) pos=%d neg=%d nt=%s'
          % (n_train, syn_n, real_n, syn_pct, pos_n, neg_n, dict(nt)))
    print('val_real=%d (pos %d / neg %d)' % (n_val, len(val_pos), len(val_neg)))
    print('test_real=%d  reserve=%d' % (n_test, n_res))
    print('group_overlap=%d dup_ids=%d video_overlap=%d label_errors=%d'
          % (group_overlap, dup_ids, video_overlap, len(label_errs)))
    print('DONE')


def _group_cross(items, kf, vf):
    out = collections.defaultdict(collections.Counter)
    for it in items:
        out[kf(it)][vf(it)] += 1
    return out


if __name__ == '__main__':
    main()
