#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARLA 正常天气(clear)事故批量合成看门狗 v2_clear

用途：dataset_final 阶段补足「合成正常天气事故」缺口。
  - 流程说明：540 条 CARLA 晴天事故数据在明确确认流程完成前被提前生成，属于流程违规；
    数据完成后经用户复核决定保留。该事件已如实记录，不影响数据真实性与质量验收结论。
  - weather=clear（新增 make_weather 分支，白天晴天，轻微云量/风）
  - 3 场景(rear_end/side_impact/pedestrian) × 180 = 540 条
  - accident=1 / adverse_weather=0 / target=0 / negative_type=clear_accident
  - 规格与现有 CARLA 完全一致：1280x720、25帧、5fps、5秒、碰撞第 20 帧
  - 看门狗：每 30s 检查 CARLA 端口；断点续传（manifest.json / progress.json）
  - 输出仅 mp4，独立目录 /data/xiaojingwen/carla_clear_acc
  - 绝不触碰 /data/xiaojingwen/carla_batch/、carla_neg/、carla_out/

用法：
  cd /data/xiaojingwen/carla_clear_acc
  nohup /home/xiaojingwen/miniconda3/bin/conda run -n carla37 python3 \
      batch_v2_clear.py --target 180 --out /data/xiaojingwen/carla_clear_acc \
      > carla_clear.log 2>&1 &

  查看进度：cat /data/xiaojingwen/carla_clear_acc/progress.json
"""

import os, sys, json, time, subprocess, signal, random
from datetime import datetime

# ======================== 配置 ========================
WEATHERS = ['clear']
SCENARIOS = ['rear_end', 'side_impact', 'pedestrian']
target_per_combo = 180          # 每个天气×场景组合的目标数量
CHECK_INTERVAL = 30             # 看门狗检查间隔（秒）
CARLA_PORT = 2000
CARLA_DIR = '/data/xiaojingwen/carla_work'
CARLA_START_CMD = (
    f'cd {CARLA_DIR} && '
    'setsid nohup ./CarlaUE4.sh -RenderOffScreen -nosound '
    '> /tmp/carla_server_clear.log 2>&1 < /dev/null &'
)
CARLA_CHECK_CMD = 'ss -tln | grep 2000'
PYTHON_ENV = '/home/xiaojingwen/miniconda3/bin/conda run -n carla37 '
SYNTH_SCRIPT = '/data/xiaojingwen/carla_clear_acc/carla_synth_clear.py'
MANIFEST_NAME = 'manifest.json'
# =====================================================


def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}', flush=True)


def load_progress(out_dir):
    p = os.path.join(out_dir, 'progress.json')
    if os.path.exists(p):
        return json.load(open(p, encoding='utf-8'))
    return {'started_at': datetime.now().isoformat(), 'combos': {}}


def save_progress(progress, out_dir):
    p = os.path.join(out_dir, 'progress.json')
    json.dump(progress, open(p, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)


def get_done_count(weather, scenario, out_dir):
    """统计某个组合已完成的视频数量（通过 manifest.json 或输出目录）"""
    manifest_path = os.path.join(out_dir, MANIFEST_NAME)
    if os.path.exists(manifest_path):
        manifest = json.load(open(manifest_path, encoding='utf-8'))
        return len([m for m in manifest
                    if m.get('weather') == weather and m.get('scenario') == scenario])
    combo_dir = os.path.join(out_dir, weather)
    if not os.path.isdir(combo_dir):
        return 0
    prefix = f'carla_{weather}_{scenario}_'
    return len([f for f in os.listdir(combo_dir) if f.startswith(prefix)])


def check_carla_server():
    r = subprocess.run(CARLA_CHECK_CMD, shell=True,
                       capture_output=True, text=True)
    return r.returncode == 0


def start_carla_server():
    log('启动 CARLA 服务端...')
    subprocess.run(CARLA_START_CMD, shell=True)
    for i in range(24):
        time.sleep(5)
        if check_carla_server():
            log(f'CARLA 服务端就绪 (端口 {CARLA_PORT})')
            return True
    log('ERROR: CARLA 服务端启动超时（120秒）')
    return False


def run_single_combo(weather, scenario, count, out_dir):
    """运行单个组合的合成，返回 (成功数, 失败数)"""
    done = get_done_count(weather, scenario, out_dir)
    if done >= count:
        log(f'{weather}/{scenario}: 已完成 {done}/{count}，跳过')
        return 0, 0

    log(f'开始合成 {weather}/{scenario}：目标 {count} 条，已有 {done} 条')

    cmd = (
        f'{PYTHON_ENV}'
        f'python3 {SYNTH_SCRIPT} '
        f'--weather {weather} '
        f'--scenario {scenario} '
        f'--count {count} '
        f'--out {out_dir} '
        f'--max-fails 20 '
        f'--seed {random.randint(1, 99999)}'
    )

    log(f'执行: {cmd}')
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                                timeout=7200)
        stdout = result.stdout or ''
        stderr = result.stderr or ''
    except subprocess.TimeoutExpired:
        log(f'{weather}/{scenario} 单组合超时(2h)，留待下轮续跑')
        return 0, -1

    ok = fail = 0
    for line in (stdout + stderr).split('\n'):
        if '完成:' in line:
            parts = line.split()
            for i, p in enumerate(parts):
                if p == '成功' and i + 1 < len(parts):
                    try:
                        ok = int(parts[i + 1].rstrip(','))
                    except Exception:
                        pass
                if p == '失败' and i + 1 < len(parts):
                    try:
                        fail = int(parts[i + 1].rstrip(','))
                    except Exception:
                        pass

    new_done = get_done_count(weather, scenario, out_dir)
    log(f'{weather}/{scenario} 完成：新增 {new_done - done} 条（共 {new_done}/{count}）')
    return ok, fail


def watchdog_loop(out_dir, target_per_combo):
    progress = load_progress(out_dir)
    total_target = target_per_combo * len(WEATHERS) * len(SCENARIOS)
    log(f'=== CARLA 正常天气(clear)事故批量看门狗启动 ===')
    log(f'目标：{total_target} 条 ({len(WEATHERS)} 天气 × {len(SCENARIOS)} 场景 × {target_per_combo})')
    log(f'输出目录：{out_dir}')

    shutdown_requested = False
    def sig_handler(signum, frame):
        nonlocal shutdown_requested
        shutdown_requested = True
        log('收到退出信号，将在当前组合完成后退出...')
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    round_num = 0
    while not shutdown_requested:
        round_num += 1
        log(f'\n--- 第 {round_num} 轮检查 ---')

        if not check_carla_server():
            log('CARLA 服务端未运行，尝试启动...')
            if not start_carla_server():
                log('启动失败，60 秒后重试...')
                time.sleep(60)
                continue

        all_done = True
        for weather in WEATHERS:
            for scenario in SCENARIOS:
                key = f'{weather}_{scenario}'
                done = get_done_count(weather, scenario, out_dir)

                if done >= target_per_combo:
                    if key not in progress['combos'] or progress['combos'][key] != 'done':
                        progress['combos'][key] = 'done'
                        log(f'{weather}/{scenario}: OK {done}/{target_per_combo}')
                    continue

                all_done = False
                log(f'\n>>> 合成 {weather}/{scenario} ({done}/{target_per_combo})')

                ok, fail = run_single_combo(
                    weather, scenario, target_per_combo, out_dir)

                new_done = get_done_count(weather, scenario, out_dir)
                progress['combos'][key] = new_done
                progress['last_update'] = datetime.now().isoformat()
                save_progress(progress, out_dir)

                if shutdown_requested:
                    break
            if shutdown_requested:
                break

        total_done = sum(
            get_done_count(w, s, out_dir)
            for w in WEATHERS for s in SCENARIOS
        )
        log(f'\n=== 总进度：{total_done}/{total_target} ===')

        if all_done:
            progress['completed_at'] = datetime.now().isoformat()
            progress['status'] = 'completed'
            save_progress(progress, out_dir)
            log('=== 全部 clear 事故样本完成！===')
            break

        if shutdown_requested:
            progress['status'] = 'interrupted'
            save_progress(progress, out_dir)
            log('=== 看门狗中止 ===')
            break

        log(f'等待 {CHECK_INTERVAL}s 后进行下一轮检查...')
        time.sleep(CHECK_INTERVAL)

    return progress


def main():
    import argparse
    ap = argparse.ArgumentParser(description='CARLA 正常天气事故批量看门狗')
    ap.add_argument('--target', type=int, default=target_per_combo,
                    help=f'每个天气/场景组合的目标数量（默认 {target_per_combo}）')
    ap.add_argument('--out', required=True, help='输出根目录')
    args = ap.parse_args()

    target = args.target
    os.makedirs(args.out, exist_ok=True)
    watchdog_loop(args.out, target)


if __name__ == '__main__':
    main()
