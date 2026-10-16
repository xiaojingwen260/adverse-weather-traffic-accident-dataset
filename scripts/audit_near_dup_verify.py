# -*- coding: utf-8 -*-
"""audit_near_dup_verify.py — 对疑似对做 25 帧逐帧 dHash 精确复核 + 渲染对比图

方法：疑似对（near_dup le4 全部 + le8 中 train-val/test 对）逐帧 25 帧 dHash，
      输出：帧级平均汉明距离、时间对齐最近距离（容忍偏移）、并渲染
      首帧/碰撞帧对比图到 reports/spot_check/pairs/（供目检）
判定参考：合成同域同类平均距离通常在 <5；跨域真实-合成高（>10 常见）；
          帧级平均 <=4 且画面目检一致 → 近重复成立
输出：reports/audit_near_dup_verify.json + pairs/*.png
"""
import json
import os
import collections
import datetime


def main():
    import numpy as np
    import cv2
    from PIL import Image, ImageDraw

    ROOT = r'D:\dataset_final_export\dataset_final'
    R = os.path.join(ROOT, 'reports')
    P = os.path.join(R, 'spot_check', 'pairs')
    os.makedirs(P, exist_ok=True)
    m = json.load(open(os.path.join(ROOT, 'manifests', 'dataset_master.json'), encoding='utf-8'))
    by_id = {it['sample_id']: it for it in m}
    nd = json.load(open(os.path.join(R, 'audit_near_dup.json'), encoding='utf-8'))

    def frames(sid):
        d = os.path.join(ROOT, by_id[sid]['frame_dir'])
        return sorted(f for f in os.listdir(d) if f.lower().endswith('.jpg'))

    def dhash(img, size=8):
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        g = cv2.resize(g, (size + 1, size))
        bits = 0
        for rr in range(size):
            for c in range(size):
                bits = (bits << 1) | (1 if g[rr, c] > g[rr, c + 1] else 0)
        return bits

    def seq_hash(sid):
        jpgs = frames(sid)
        return [dhash(cv2.imread(os.path.join(ROOT, by_id[sid]['frame_dir'], jpgs[i]),
                                cv2.IMREAD_COLOR)) for i in range(len(jpgs))]

    pairs = []
    for s in nd['strict_le4_list']:
        pairs.append((s['a'], s['b'], s['hamming'], s['pair'], s['domains'], 'le4'))
    for s in nd['suspicious_le8_list']:
        if s['pair'] in ('train-val_real', 'train-test_real', 'val_real-test_real'):
            pairs.append((s['a'], s['b'], s['hamming'], s['pair'], s['domains'], 'le8'))

    results = []
    rendered = 0
    seen = set()
    for a, b, h, pair, domains, level in pairs:
        if (a, b) in seen or (b, a) in seen:
            continue
        seen.add((a, b))
        ha = seq_hash(a)
        hb = seq_hash(b)
        n = min(len(ha), len(hb))
        # 逐帧对齐平均
        aligned = [bin(x ^ y).count('1') for x, y in zip(ha[:n], hb[:n])]
        mean_align = sum(aligned) / n
        # 时间容忍 ±2 帧：滑动最近
        best = None
        for off in range(-2, 3):
            d = 0
            cnt = 0
            for i in range(n):
                j = i + off
                if 0 <= j < len(hb):
                    d += bin(ha[i] ^ hb[j]).count('1')
                    cnt += 1
            if cnt:
                mm = d / cnt
                if best is None or mm < best:
                    best = mm
        results.append({'a': a, 'b': b, 'majority_hamming': h, 'pair': pair,
                        'domains': domains, 'level': level,
                        'mean_frame_hamming_align': round(mean_align, 3),
                        'best_frame_hamming_offset': round(best, 3)})
        # 渲染对比图（首帧并排 + 标签）
        if rendered < 60:
            fa = frames(a)
            fb = frames(b)
            ia = cv2.imread(os.path.join(ROOT, by_id[a]['frame_dir'], fa[0]), cv2.IMREAD_COLOR)
            ib = cv2.imread(os.path.join(ROOT, by_id[b]['frame_dir'], fb[0]), cv2.IMREAD_COLOR)
            ia = cv2.resize(ia, (320, 180))
            ib = cv2.resize(ib, (320, 180))
            img = np.concatenate([ia, ib], axis=1)
            cv2.imwrite(os.path.join(P, '%s__%s.png' % (a, b)), img)
            rendered += 1

    json.dump({'audit_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
               'method': ('疑似对逐帧 25 帧 dHash：对齐平均 + 时间容忍±2 帧最近平均；'
                          '帧级平均<=4 视为近重复候选'),
               'pairs': results,
               'conclusion': 'NEAR_DUP_VERIFY_DONE'}, open(os.path.join(R, 'audit_near_dup_verify.json'),
                                                           'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)
    print('DONE verify pairs=%d rendered=%d' % (len(results), rendered))
    # 汇总: 平均<=4 的对
    for r in results:
        flag = ' <<< NEAR' if r['mean_frame_hamming_align'] <= 4 else ''
        print('%s %s | %s %s | align=%.2f best=%.2f%s' % (
            r['a'], r['b'], r['pair'], r['domains'], r['mean_frame_hamming_align'],
            r['best_frame_hamming_offset'], flag))


if __name__ == '__main__':
    main()
