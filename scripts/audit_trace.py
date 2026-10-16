# -*- coding: utf-8 -*-
"""audit_trace.py — v1.0 最终验收审计：数据来源与可追溯性（只读，只报告）

按 source 检查 master 样本能否追溯到本地原始数据：
  CARLA 正：D:\dataset\carla_out_v2\{weather}\{sample_id}.mp4
  CARLA 负：D:\dataset\carla_neg_out_v2\{weather}\{sample_id}.mp4
  CARLA clear：D:\dataset\carla_clear_out_v2\clear\{sample_id}.mp4
  CCD：D:\dataset\CCD\ccd_adverse_v2\videos\{weather_raw_dir}\{original_video_id}.mp4
       （weather_raw=Normal→crash_day_normal；Rainy→crash_day_rainy；Snowy→crash_day_snowy；其余按实际目录探测）
  DADA：D:\dataset\DADA\frames_10fps\images_10_{X}\（dada_X_YYY → 视频 X）
  BDD100K：D:\dataset\BDD100K\BDD100K\mot_adverse\{train|val}\{original_video_id}\
输出：reports/audit_trace.json + reports/audit_trace.md
"""
import json
import os
import collections
import datetime

ROOT = r'D:\dataset_final_export\dataset_final'
M = os.path.join(ROOT, 'manifests', 'dataset_master.json')
R = os.path.join(ROOT, 'reports')
OUT_JSON = os.path.join(R, 'audit_trace.json')
OUT_MD = os.path.join(R, 'audit_trace.md')

CARLA_POS = r'D:\dataset\carla_out_v2'
CARLA_NEG = r'D:\dataset\carla_neg_out_v2'
CARLA_CLR = r'D:\dataset\carla_clear_out_v2'
CCD_VID = r'D:\dataset\CCD\ccd_adverse_v2\videos'
DADA_FR = r'D:\dataset\DADA\frames_10fps'
BDD_MOT = r'D:\dataset\BDD100K\BDD100K\mot_adverse'

CCD_DIRMAP = {'Normal': 'crash_day_normal', 'Rainy': 'crash_day_rainy', 'Snowy': 'crash_day_snowy'}


def main():
    m = json.load(open(M, encoding='utf-8'))
    ok = []
    fail = []
    per_src = collections.defaultdict(lambda: {'ok': 0, 'fail': 0})

    def check(sid, path):
        exists = os.path.exists(path)
        (ok if exists else fail).append({'sample_id': sid, 'path': path})
        return exists

    for it in m:
        sid = it['sample_id']
        src = it['source']
        if src == 'CARLA':
            if it['negative_type'] == 'adverse_no_accident':
                p = os.path.join(CARLA_NEG, it['weather'], sid + '.mp4')
            elif it['negative_type'] == 'clear_accident':
                p = os.path.join(CARLA_CLR, 'clear', sid + '.mp4')
            else:
                p = os.path.join(CARLA_POS, it['weather'], sid + '.mp4')
            check(sid, p)
        elif src == 'CCD':
            wd = CCD_DIRMAP.get(it.get('weather_raw'))
            if wd is None:
                # 探测
                wd = None
                for d in os.listdir(CCD_VID):
                    if os.path.isdir(os.path.join(CCD_VID, d)):
                        if os.path.exists(os.path.join(CCD_VID, d, it['original_video_id'] + '.mp4')):
                            wd = d
                            break
            if wd:
                p = os.path.join(CCD_VID, wd, it['original_video_id'] + '.mp4')
            else:
                p = os.path.join(CCD_VID, 'CRASH_DIR_NOT_FOUND_' + str(it['original_video_id']))
            check(sid, p)
        elif src == 'DADA':
            vid = str(it['original_video_id'])
            # dada_X_YYY → X（目录 images_10_XXX 三位补零）
            x = vid.split('_')[1] if len(vid.split('_')) >= 2 else vid
            candidates = [os.path.join(DADA_FR, d) for d in os.listdir(DADA_FR)
                          if d.startswith('images_10_') and d[10:].lstrip('0') == str(int(x))
                          or d == 'images_10_%s' % x.zfill(3)]
            p = candidates[0] if candidates else os.path.join(DADA_FR, 'NOT_FOUND_' + vid)
            check(sid, p)
        elif src == 'BDD100K':
            found = False
            for sub in ('train', 'val'):
                p = os.path.join(BDD_MOT, sub, str(it['original_video_id']))
                if os.path.isdir(p):
                    found = True
                    per_src['BDD100K']['ok'] += 1
                    ok.append({'sample_id': sid, 'path': p})
                    break
            if not found:
                per_src['BDD100K']['fail'] += 1
                fail.append({'sample_id': sid, 'path': 'NOT_FOUND'})

    # per-source 统计（按 sample_id 前缀/来源精确重算）
    for k, cond in [('CARLA', lambda s: s.startswith('carla_')),
                    ('CCD', lambda s: s.startswith('crash_')),
                    ('DADA', lambda s: s.startswith('dada_'))]:
        per_src[k] = {'ok': sum(1 for x in ok if cond(x['sample_id'])),
                      'fail': sum(1 for x in fail if cond(x['sample_id']))}
    per_src['BDD100K'] = {'ok': sum(1 for x in ok if not x['sample_id'].startswith(('carla_', 'crash_', 'dada_'))),
                          'fail': sum(1 for x in fail if not x['sample_id'].startswith(('carla_', 'crash_', 'dada_')))}
    trace_total = sum(v['ok'] for v in per_src.values())
    fail_total = sum(v['fail'] for v in per_src.values())

    result = {
        'audit_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'input': 'manifests/dataset_master.json（只读）',
        'per_source': {k: dict(v) for k, v in per_src.items()},
        'traceable': trace_total,
        'untraceable': fail_total,
        'fail_list': fail[:200],
        'source_url_note': ('manifest 无 source URL 字段（元数据缺口，C 级）；可追溯性基于本地原始文件/'
                            'original_video_id 建立。'),
        'conclusion': 'PASS' if fail_total == 0 else 'UNTRACEABLE_FOUND',
    }
    json.dump(result, open(OUT_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    lines = ['# v1.0 最终验收审计 · 数据来源与可追溯性', '',
             '审计时间：%s' % result['audit_time'], '',
             '| 来源 | 可追溯 | 不可追溯 |', '|---|---|---|']
    for k in ['CARLA', 'CCD', 'DADA', 'BDD100K']:
        lines.append('| %s | %d | %d |' % (k, per_src[k]['ok'], per_src[k]['fail']))
    lines += ['', '合计：可追溯 %d / 不可追溯 %d' % (trace_total, fail_total), '',
              '说明：%s' % result['source_url_note'], '']
    if fail:
        lines += ['## 不可追溯样本（前 200）', '', '```']
        lines += ['%s  %s' % (x['sample_id'], x['path']) for x in fail[:200]]
        lines += ['```', '']
    open(OUT_MD, 'w', encoding='utf-8').write('\n'.join(lines))
    print('DONE trace: traceable=%d untraceable=%d per_source=%s' % (
        trace_total, fail_total, {k: dict(v) for k, v in per_src.items()}))


if __name__ == '__main__':
    main()
