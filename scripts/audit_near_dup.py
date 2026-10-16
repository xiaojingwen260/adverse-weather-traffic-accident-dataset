# -*- coding: utf-8 -*-
"""audit_near_dup.py — v1.0 最终验收审计：重复与深度近重复/泄漏（感知哈希，独立复核）

方法（不只查文件名/MD5）：
  L1 文件级：全量逐帧 MD5（audit_integrity 输出）+ 25 帧序列 MD5（整条重复）
  L2 感知哈希全局：每条抽 5 帧（索引 0,6,12,18,24）计算 64bit dHash，
     取 5 帧按位多数 → 单条指纹；跨 split 任意对两两汉明距离（numpy 分块）：
     距离<=4 视为疑似近重复（严），<=8 视为可疑（宽）
  L3 同源组精确：CARLA 运行段（town+scenario+weather+seed）内两两逐帧 dHash
     序列（5 帧对齐）比较；真实数据按 source+original_video_id（已唯一，无组内对）
  L4 同源跨 split：group_id / original_video_id 跨 split 交集（audit_labels 已输出 0）

输出：reports/audit_near_dup.json + reports/audit_near_dup.md
"""
import json
import os
import collections
import datetime

ROOT = r'D:\dataset_final_export\dataset_final'
M = os.path.join(ROOT, 'manifests', 'dataset_master.json')
R = os.path.join(ROOT, 'reports')
OUT_JSON = os.path.join(R, 'audit_near_dup.json')
OUT_MD = os.path.join(R, 'audit_near_dup.md')


def dhash(img, size=8):
    import cv2
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.resize(g, (size + 1, size))
    bits = 0
    for r in range(size):
        for c in range(size):
            bits = (bits << 1) | (1 if g[r, c] > g[r, c + 1] else 0)
    return bits


def hamming(a, b):
    return bin(a ^ b).count('1')


def main():
    import cv2
    import numpy as np
    m = json.load(open(M, encoding='utf-8'))
    t0 = datetime.datetime.now()
    FRAME_IDX = [0, 6, 12, 18, 24]  # 25 帧 → 000001/000007/000013/000019/000025

    # 每条 5 帧 dHash
    rec = {}  # sample_id -> dict(split, source, domain, group_id, hashes[5], maj)
    for i, it in enumerate(m):
        d = os.path.join(ROOT, it['frame_dir'])
        jpgs = sorted([f for f in os.listdir(d) if f.lower().endswith('.jpg')])
        hashes = []
        for j in FRAME_IDX:
            if j < len(jpgs):
                img = cv2.imread(os.path.join(d, jpgs[j]), cv2.IMREAD_COLOR)
                hashes.append(dhash(img) if img is not None else 0)
            else:
                hashes.append(0)
        # 按位多数
        maj = 0
        for b in range(64):
            cnt = sum(1 for h in hashes if (h >> (63 - b)) & 1)
            maj = (maj << 1) | (1 if cnt >= 3 else 0)
        rec[it['sample_id']] = {
            'split': it['split'], 'source': it['source'], 'domain': it['domain'],
            'group_id': it['group_id'], 'town': it['town'], 'scenario': it['scenario'],
            'weather': it['weather'], 'seed': it['seed'],
            'hashes': hashes, 'maj': maj,
        }
        if (i + 1) % 1000 == 0:
            print('hash progress %d/%d' % (i + 1, len(m)), flush=True)
    print('hash computed %d' % len(rec), flush=True)

    ids = list(rec.keys())
    maj_arr = np.array([rec[s]['maj'] for s in ids], dtype=np.uint64)
    # 位矩阵
    bits = np.zeros((len(ids), 64), dtype=np.uint8)
    for b in range(64):
        bits[:, b] = (maj_arr >> (63 - b)) & 1

    # 跨 split 对：train × (val_real ∪ test_real ∪ reserve)；val × test；val × reserve；test × reserve
    splits = [x['split'] for x in m]
    idx_of = {sp: [i for i, s in enumerate(ids) if splits[i] == sp] for sp in ['train', 'val_real', 'test_real', 'reserve']}

    suspicious = []  # {a, b, dist, split_pair, domain_pair}
    pairs_done = 0
    combos = [('train', 'val_real'), ('train', 'test_real'), ('train', 'reserve'),
              ('val_real', 'test_real'), ('val_real', 'reserve'), ('test_real', 'reserve')]
    for spA, spB in combos:
        ia = idx_of[spA]
        ib = idx_of[spB]
        Ba = bits[ia]
        Bb = bits[ib]
        # 分块
        for st in range(0, len(ia), 400):
            block = Ba[st:st + 400]
            dist = block @ (1 - Bb).T + (1 - block) @ Bb.T  # (k, nB) 汉明距离
            k = dist.shape[0]
            for r in range(k):
                r_abs = ia[st + r]
                for c in range(dist.shape[1]):
                    dd = int(dist[r, c])
                    if dd <= 8:
                        c_abs = ib[c]
                        a, b = ids[r_abs], ids[c_abs]
                        suspicious.append({
                            'a': a, 'b': b, 'hamming': dd,
                            'pair': '%s-%s' % (spA, spB),
                            'domains': '%s-%s' % (rec[a]['domain'], rec[b]['domain']),
                            'sources': '%s-%s' % (rec[a]['source'], rec[b]['source']),
                            'towns': '%s-%s' % (rec[a]['town'], rec[b]['town']),
                            'weathers': '%s-%s' % (rec[a]['weather'], rec[b]['weather']),
                        })
            pairs_done += k * len(ib)
    print('cross pairs computed=%d suspicious<=8=%d' % (pairs_done, len(suspicious)), flush=True)

    strict = [s for s in suspicious if s['hamming'] <= 4]

    # L3 同源组（CARLA 运行段）内精确逐帧比较
    seg = collections.defaultdict(list)
    for sid, info in rec.items():
        if info['source'] == 'CARLA' and info['seed'] is not None:
            seg[(info['town'], info['scenario'], info['weather'], info['seed'])].append(sid)
    seg_near = []
    for key, sids in seg.items():
        for i in range(len(sids)):
            for j in range(i + 1, len(sids)):
                a, b = sids[i], sids[j]
                ha, hb = rec[a]['hashes'], rec[b]['hashes']
                d = min(sum(hamming(ha[f], hb[f]) for f in range(5)),
                        sum(hamming(ha[f], hb[4 - f]) for f in range(5)))  # 正/逆序对齐
                if d <= 20:  # 5 帧平均汉明 <=4
                    seg_near.append({'a': a, 'b': b, 'seq_hamming': d,
                                     'segment': str(key), 'splits': '%s-%s' % (rec[a]['split'], rec[b]['split'])})

    result = {
        'audit_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'elapsed_sec': (datetime.datetime.now() - t0).total_seconds(),
        'method': ('L1 MD5/序列MD5(见 audit_integrity)；L2 5帧dHash按位多数指纹 跨split两两汉明'
                   '(numpy 分块，pair=%d)；L3 CARLA 运行段内 5 帧序列精确比较' % pairs_done),
        'total_samples': len(rec),
        'cross_split_pairs_compared': pairs_done,
        'suspicious_le8': len(suspicious),
        'suspicious_le8_list': suspicious[:200],
        'strict_le4': len(strict),
        'strict_le4_list': strict[:100],
        'segment_near_pairs': len(seg_near),
        'segment_near_list': seg_near[:100],
        'segment_count': len(seg),
        'same_source_cross_split': '见 audit_labels（group/original_video_id 跨 split 交集均 0）',
        'conclusion': 'PASS' if (len(strict) == 0 and len(seg_near) == 0) else 'NEAR_DUP_FOUND',
    }
    json.dump(result, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    lines = ['# v1.0 最终验收审计 · 重复与深度近重复/泄漏', '',
             '审计时间：%s（耗时 %.0fs）' % (result['audit_time'], result['elapsed_sec']), '',
             '方法：%s' % result['method'], '',
             '| 项 | 值 |', '|---|---|',
             '| 参与样本 | %d |' % len(rec),
             '| 跨 split 比对对数 | %d |' % pairs_done,
             '| 疑似（汉明<=8） | %d |' % len(suspicious),
             '| 严格疑似（汉明<=4） | %d |' % len(strict),
             '| CARLA 运行段内近重复（序列汉明<=20） | %d |' % len(seg_near),
             '| 结论 | **%s** |' % result['conclusion'], '']
    if strict:
        lines += ['## 严格疑似对（<=4）', '', '| A | B | 汉明 | 跨集 | 域 | 来源 |', '|---|---|---|---|---|---|']
        for s in strict:
            lines.append('| %s | %s | %d | %s | %s | %s |' % (s['a'], s['b'], s['hamming'],
                                                             s['pair'], s['domains'], s['sources']))
        lines += ['']
    if seg_near:
        lines += ['## CARLA 运行段内近重复（前 100）', '', '| A | B | 序列汉明 | 段 | 跨集 |', '|---|---|---|---|---|']
        for s in seg_near[:100]:
            lines.append('| %s | %s | %d | %s | %s |' % (s['a'], s['b'], s['seq_hamming'],
                                                         s['segment'], s['splits']))
        lines += ['']
    if suspicious and not strict:
        lines += ['## 可疑对（6<汉明<=8，前 100）', '', '| A | B | 汉明 | 跨集 |', '|---|---|---|---|']
        for s in suspicious[:100]:
            lines.append('| %s | %s | %d | %s |' % (s['a'], s['b'], s['hamming'], s['pair']))
        lines += ['']
    open(OUT_MD, 'w', encoding='utf-8').write('\n'.join(lines))
    print('DONE near_dup: pairs=%d le8=%d le4=%d seg_near=%d' % (
        pairs_done, len(suspicious), len(strict), len(seg_near)))


if __name__ == '__main__':
    main()
