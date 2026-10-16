# -*- coding: utf-8 -*-
"""spot_check_prep.py — v1.0 最终验收审计：标注质量抽检 contact sheet 生成（只读，不改标签）

抽检策略（>=10% = >=500 条：prediction_eligible=true 重点 / 正样本优先 /
稀有类别尽量全检 / test 集重点 / 恶劣天气事故重点）：
  1) test_real 全部 340
  2) early_motion_peak 全部 175（复核 prediction_eligible=false 自洽性）
  3) 真实恶劣天气事故正样本全检（real+target=1，511，去重）
  4) 其余随机补足至 >=500 唯一
渲染：每条 4 帧（事故: 起始/碰撞前/碰撞帧/末尾；无事故: 0,7,13,24），96x54 缩略图
      -> reports/spot_check/sheets/sheet_XXX.png（每张 25 条 x 4 帧，行首元数据标签）
输出：reports/spot_check/selection.json + selection.csv + sheets/
"""
import json
import os
import random
import csv
import datetime


def main():
    import numpy as np
    from PIL import Image, ImageDraw
    import cv2

    ROOT = r'D:\dataset_final_export\dataset_final'
    M = os.path.join(ROOT, 'manifests', 'dataset_master.json')
    R = os.path.join(ROOT, 'reports')
    SC = os.path.join(R, 'spot_check')
    SH = os.path.join(SC, 'sheets')
    OUT_SEL = os.path.join(SC, 'selection.json')
    OUT_CSV = os.path.join(SC, 'selection.csv')
    SHEET_SIZE = 25

    random.seed(42)
    os.makedirs(SH, exist_ok=True)
    m = json.load(open(M, encoding='utf-8'))
    by_id = {it['sample_id']: it for it in m}

    sel = []
    sel_ids = set()

    def add(sid):
        if sid not in sel_ids:
            sel_ids.add(sid)
            sel.append(by_id[sid])

    # 1) test_real 全部
    for it in m:
        if it['split'] == 'test_real':
            add(it['sample_id'])
    # 2) early 全部
    for it in m:
        if (it.get('quality_flag') or []) == ['early_motion_peak']:
            add(it['sample_id'])
    # 3) 真实恶劣天气事故正样本全检
    for it in m:
        if it['domain'] == 'real' and it['target'] == 1:
            add(it['sample_id'])
    # 4) 补足：其余随机，直到 >=600 上限
    candidates = [it for it in m if it['sample_id'] not in sel_ids]
    random.shuffle(candidates)
    for it in candidates:
        if len(sel) >= 600:
            break
        add(it['sample_id'])
    print('selected unique=%d' % len(sel))

    FRAME_SETS = {
        'pos': [0, 15, 20, 24],
        'neg': [0, 7, 13, 24],
    }
    meta = []
    canvas = None
    sheet_no = 0
    row = 0
    for si, it in enumerate(sel):
        sid = it['sample_id']
        d = os.path.join(ROOT, it['frame_dir'])
        jpgs = sorted(f for f in os.listdir(d) if f.lower().endswith('.jpg'))
        idxs = FRAME_SETS['pos' if it['accident'] == 1 else 'neg']
        thumbs = []
        for j in idxs:
            j = min(j, len(jpgs) - 1)
            img = cv2.imread(os.path.join(d, jpgs[j]), cv2.IMREAD_COLOR)
            if img is None:
                img = 255 * np.ones((54, 96, 3), dtype=np.uint8)
            img = cv2.resize(img, (96, 54))
            thumbs.append(img)
        if row == 0:
            canvas = Image.new('RGB', (96 * 4 + 250, 54 * SHEET_SIZE), (40, 40, 40))
            sheet_path = os.path.join(SH, 'sheet_%03d.png' % sheet_no)
        y0 = row * 54
        for k, t in enumerate(thumbs):
            canvas.paste(Image.fromarray(t[:, :, ::-1]), (250 + k * 96, y0))
        draw = ImageDraw.Draw(canvas)
        label = ('%s w=%s acc=%d tgt=%d pe=%s cf=%s sp=%s\nqf=%s src=%s' % (
            sid, it['weather'], it['accident'], it['target'],
            it['prediction_eligible'], it['collision_frame'], it['split'],
            ','.join(it.get('quality_flag') or ['-']), it['source']))
        draw.text((4, y0 + 1), label, fill=(255, 255, 255))
        meta.append({'sample_id': sid, 'sheet': os.path.basename(sheet_path), 'row': row,
                     'split': it['split'], 'source': it['source'], 'domain': it['domain'],
                     'weather': it['weather'], 'accident': it['accident'], 'target': it['target'],
                     'negative_type': it['negative_type'], 'prediction_eligible': it['prediction_eligible'],
                     'collision_frame': it['collision_frame'], 'quality_flag': it.get('quality_flag'),
                     'frames_shown': idxs})
        row += 1
        if row == SHEET_SIZE or si == len(sel) - 1:
            canvas.save(sheet_path)
            print('sheet %03d saved rows=%d' % (sheet_no, row), flush=True)
            sheet_no += 1
            row = 0
        if (si + 1) % 100 == 0:
            print('render progress %d/%d' % (si + 1, len(sel)), flush=True)

    json.dump({'audit_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
               'total_selected': len(sel), 'items': meta},
              open(OUT_SEL, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    with open(OUT_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(meta[0].keys()))
        w.writeheader()
        for r in meta:
            w.writerow(r)
    print('DONE spot_check_prep: selected=%d sheets=%d' % (
        len(sel), (len(sel) + SHEET_SIZE - 1) // SHEET_SIZE))


if __name__ == '__main__':
    main()
