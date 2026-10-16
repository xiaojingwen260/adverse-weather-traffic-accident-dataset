# -*- coding: utf-8 -*-
"""
CARLA 事故视频合成（方案 B 正样本）v3

规格（与 CARLA合成规格.md 一致）：
  25 帧 @ 5 fps = 5 秒 / 1280x720 / 行车记录仪视角
  碰撞落在第 20±2 帧，前 3.4 秒为正常行驶

v3 关键设计（针对 v2 失败教训）：
  - 物理 20Hz，每 4 tick 抽 1 帧（0.2s 大步长会让载具物理失效）
  - 追尾 = ego 撞静止前车：碰撞由几何保证，不赌速度差
  - 侧撞/行人 = 按 ego 距离触发（不再按固定帧号赌 timing）
  - ego 车道保持转向：弯道上不会偏离车道绕过目标
  - 先跑长 episode 记录碰撞帧，回看裁 25 帧窗口

用法：
  python carla_synth.py --weather rainy --scenario rear_end --count 30 --out /path
"""
import os, sys, json, math, random, argparse, queue, re
from datetime import datetime

import numpy as np

try:
    import carla
except ImportError:
    sys.exit('未找到 carla 模块')

try:
    import cv2
except ImportError:
    cv2 = None


# ---------------- 规格常量 ----------------
OUT_FRAMES = 25
FPS = 5
DT = 0.05
TICKS_PER_FRAME = int(round((1.0 / FPS) / DT))   # 4
IMG_W, IMG_H = 1280, 720
COLLISION_AT = 20
CAPTURE_MAX = 56   # 留 6 帧余量：碰撞最晚可落在第 50 帧仍能裁出窗口
MIN_LEAD_FRAMES = 17

# Town03 加载时会把服务端搞死（实测两次均在加载途中进程消失），拉黑
TOWNS = ['Town01', 'Town02', 'Town04', 'Town05', 'Town10HD_Opt']

# 场景几何参数
REAR_GAP = 40.0        # 追尾：静止前车距离（碰撞约在 4 秒后）
SIDE_AHEAD = 40.0      # 侧撞：碰撞点在 ego 前方距离（与追尾同距离，
                       # 否则预热后 ego 只剩 ~14m，碰撞落在第 8 帧被判太早）
SIDE_OFFSET = 11.0     # 侧撞：侧车横向距离
SIDE_TRIGGER = 26.0    # 侧撞：ego 距碰撞点多远时侧车起步
PED_AHEAD = 40.0       # 行人：横穿点在 ego 前方距离（同 SIDE_AHEAD 的教训）
PED_OFFSET = 5.5       # 行人：起始横向距离
PED_TRIGGER = 16.0     # 行人：ego 距横穿点多远时开始走
PED_SPEED = 1.8        # 行人步行速度 m/s：2.6 太快（2.1s 冲过 5.5m），
                       # 碰撞时行人才进画面 1~2 帧且贴右边缘，样本不可用；
                       # 1.8m/s 走 5.5m 约 3s，与 ego(5~7m/s) 到点同步，
                       # 且行人在车道内暴露 ~2s（约 10 帧可见），利于预判学习


# ---------------- 天气 ----------------
def make_weather(name, rng):
    W = carla.WeatherParameters
    if name == 'clear':
        return W(cloudiness=rng.uniform(5, 20),
                 precipitation=0.0,
                 precipitation_deposits=0.0,
                 wind_intensity=rng.uniform(5, 25),
                 fog_density=rng.uniform(0, 2),
                 fog_distance=rng.uniform(40, 60),
                 wetness=0.0,
                 sun_altitude_angle=rng.uniform(35, 60))
    if name == 'rainy':
        return W(cloudiness=rng.uniform(70, 90),
                 precipitation=rng.uniform(80, 100),
                 precipitation_deposits=rng.uniform(70, 90),
                 wind_intensity=rng.uniform(30, 50),
                 fog_density=rng.uniform(3, 8),
                 fog_distance=rng.uniform(25, 35),
                 wetness=rng.uniform(75, 95),
                 sun_altitude_angle=rng.uniform(25, 40))
    if name == 'snowy':
        return W(cloudiness=rng.uniform(85, 95),
                 precipitation=rng.uniform(60, 80),
                 precipitation_deposits=rng.uniform(85, 100),
                 wind_intensity=rng.uniform(20, 40),
                 fog_density=rng.uniform(6, 14),
                 fog_distance=rng.uniform(15, 25),
                 wetness=rng.uniform(10, 30),
                 sun_altitude_angle=rng.uniform(10, 20))
    return W(cloudiness=rng.uniform(20, 45),
             precipitation=0.0,
             precipitation_deposits=0.0,
             wind_intensity=rng.uniform(5, 20),
             fog_density=rng.uniform(1, 4),
             wetness=0.0,
             sun_altitude_angle=rng.uniform(-40, -20))


class FrameGrabber:
    def __init__(self):
        self.q = queue.Queue()
        self.enabled = True

    def __call__(self, image):
        if self.enabled:
            self.q.put(image)

    def get(self, timeout=10.0):
        return self.q.get(timeout=timeout)

    def clear(self):
        while not self.q.empty():
            try:
                self.q.get_nowait()
            except queue.Empty:
                break

    def reset(self):
        self.clear()
        self.enabled = True

    def close(self):
        self.enabled = False
        self.clear()


def to_bgr(image):
    arr = np.frombuffer(image.raw_data, dtype=np.uint8)
    arr = arr.reshape((image.height, image.width, 4))
    return arr[:, :, :3].copy()


def build_camera(world, ego, grabber):
    grabber.reset()
    bp = world.get_blueprint_library().find('sensor.camera.rgb')
    bp.set_attribute('image_size_x', str(IMG_W))
    bp.set_attribute('image_size_y', str(IMG_H))
    bp.set_attribute('fov', '100')
    tf = carla.Transform(carla.Location(x=1.0, z=1.25))
    cam = world.spawn_actor(bp, tf, attach_to=ego)
    cam.listen(grabber)
    return cam


def spawn_vehicle(world, bp_lib, tf, rng):
    cars = [b for b in bp_lib.filter('vehicle.*')
            if int(b.get_attribute('number_of_wheels')) == 4]
    bp = rng.choice(cars)
    if bp.has_attribute('color'):
        bp.set_attribute('color', rng.choice(bp.get_attribute('color').recommended_values))
    return world.try_spawn_actor(bp, tf)


def lane_ahead_tf(world, ref_loc, dist, step=2.0):
    """ref_loc 所在车道前进 dist 米处的 Transform。

    v4 修复：一次 next(40) 在路口会随机跳分支（实测误差 190m）。
    改为 2m 步长链式推进，每步选与当前朝向最一致的延续，
    并做直线距离合理性校验。
    """
    amap = world.get_map()
    wp = amap.get_waypoint(ref_loc, project_to_road=True,
                           lane_type=carla.LaneType.Driving)
    if wp is None:
        return None
    cur = wp
    travelled = 0.0
    while travelled < dist:
        nxt = cur.next(step)
        if not nxt:
            return None
        fwd = cur.transform.get_forward_vector()
        best, best_dot = None, 0.5      # 夹角 >60° 的分支直接拒绝
        for w in nxt:
            f2 = w.transform.get_forward_vector()
            d = fwd.x * f2.x + fwd.y * f2.y
            if d > best_dot:
                best, best_dot = w, d
        if best is None:
            return None
        cur = best
        travelled += step
    tf = cur.transform
    straight = dist2d(tf.location, ref_loc)
    if straight < dist * 0.5 or straight > dist * 1.2:
        return None
    tf.location.z += 0.3
    return tf


def clear_world(world):
    """清掉残留 actor（同图连续 attempt 时会累积）"""
    n = 0
    for a in world.get_actors():
        if (a.type_id.startswith('vehicle.') or
                a.type_id.startswith('walker.') or
                a.type_id.startswith('sensor.') or
                a.type_id.startswith('controller.ai.walker')):
            try:
                a.destroy()
                n += 1
            except Exception:
                pass
    return n


def follow_steer(world, ego, lookahead=6.0):
    """车道保持转向：让 ego 沿车道走（弯道上不偏离）"""
    amap = world.get_map()
    wp = amap.get_waypoint(ego.get_location(), project_to_road=True,
                           lane_type=carla.LaneType.Driving)
    nxt = wp.next(lookahead)
    target = nxt[0].transform.location if nxt else wp.transform.location
    return steer_toward(ego, target)


def steer_toward(ego, target):
    """追踪转向：瞄准目标点开（追尾场景用它替代车道保持，
    否则多车道/弯道上 ego 会绕过静止前车，实测 68% 撞不上）"""
    tf = ego.get_transform()
    fwd = tf.get_forward_vector()
    dx = target.x - tf.location.x
    dy = target.y - tf.location.y
    n = math.hypot(dx, dy) or 1.0
    dx, dy = dx / n, dy / n
    ang = math.atan2(fwd.x * dy - fwd.y * dx, fwd.x * dx + fwd.y * dy)
    return max(-1.0, min(1.0, ang / 0.45))


def cruise(ego, steer, target=7.0):
    """定速巡航控制：固定油门实测车速 2~14m/s 飘忽，
    碰撞帧在 11~35 之间乱飞（太早判废、太晚拖时长）。
    锁住 ~7m/s 后 40m 碰撞点 ≈ 第 21 帧，稳定落在窗口内"""
    v = ego.get_velocity()
    sp = math.sqrt(v.x * v.x + v.y * v.y)
    if sp > target + 1.0:
        return carla.VehicleControl(throttle=0.0, brake=0.4, steer=steer)
    # P 增益 0.25：卡车等重载蓝图在 0.12 下提速太慢（实测碰撞拖到第 48 帧）
    thr = min(0.9, max(0.05, 0.25 * (target - sp)))
    return carla.VehicleControl(throttle=thr, steer=steer)


def dist2d(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def setup_hazard(world, bp_lib, ego, scenario, rng):
    """布设危险物，返回 (hazard, trigger_point, walk_dir or None)"""
    ego_loc = ego.get_location()
    if scenario == 'rear_end':
        for d in [REAR_GAP, REAR_GAP - 5, REAR_GAP + 5, REAR_GAP - 10]:
            tf = lane_ahead_tf(world, ego_loc, d)
            if tf is None:
                print('    [dbg] d=%.0f 车道推进失败' % d, flush=True)
                continue
            v = spawn_vehicle(world, bp_lib, tf, rng)
            if v is None:
                print('    [dbg] d=%.0f 生成点被占' % d, flush=True)
                continue
            world.tick()   # 同步模式下新 actor 须 tick 后坐标才生效
            real_d = dist2d(v.get_location(), ego_loc)
            if real_d < 15.0 or real_d > 60.0:   # 位置不合理，毁掉重试
                print('    [dbg] d=%.0f 实距%.1f 不合理' % (d, real_d), flush=True)
                v.destroy()
                continue
            # 朝向校验：车道方向的"前方"可能在 ego 背后（生成点朝向与车道
            # 相反时），那时追踪转向会原地打转（实测车速 0.1 m/s）
            ef = ego.get_transform().get_forward_vector()
            hl = v.get_location()
            hx, hy = hl.x - ego_loc.x, hl.y - ego_loc.y
            hn = math.hypot(hx, hy) or 1.0
            facing = (ef.x * hx + ef.y * hy) / hn
            if facing < 0.5:
                print('    [dbg] d=%.0f 目标在身后(cos%.2f)，放弃' % (d, facing),
                      flush=True)
                v.destroy()
                continue
            return v, None, None
        return None, None, None

    if scenario == 'side_impact':
        cross_tf = lane_ahead_tf(world, ego_loc, SIDE_AHEAD)
        if cross_tf is None:
            return None, None, None
        cp = cross_tf.location           # 碰撞点（ego 车道上）
        right = cross_tf.get_right_vector()
        # 固定 11m 单侧常落在人行道/建筑里导致生成失败（实测占失败一半），
        # 改为左右两侧 × 多个横向距离逐个尝试，并校验实落点没被挤偏
        for sign in (1, -1):
            for off in [8.0, 10.0, SIDE_OFFSET, 13.0, 15.0]:
                side_loc = carla.Location(x=cp.x + right.x * off * sign,
                                          y=cp.y + right.y * off * sign,
                                          z=cp.z + 0.5)
                yaw = math.degrees(math.atan2(cp.y - side_loc.y,
                                              cp.x - side_loc.x))
                v = spawn_vehicle(world, bp_lib,
                                  carla.Transform(side_loc,
                                                  carla.Rotation(yaw=yaw)), rng)
                if v is None:
                    continue
                world.tick()
                if dist2d(v.get_location(), side_loc) > 2.5:
                    v.destroy()
                    continue
                return v, cp, None
        return None, None, None

    # pedestrian
    cross_tf = lane_ahead_tf(world, ego_loc, PED_AHEAD)
    if cross_tf is None:
        return None, None, None
    cp = cross_tf.location
    right = cross_tf.get_right_vector()
    wbp = bp_lib.filter('walker.pedestrian.*')
    w_loc = carla.Location(x=cp.x + right.x * PED_OFFSET,
                           y=cp.y + right.y * PED_OFFSET,
                           z=cp.z + 0.5)
    w = world.try_spawn_actor(rng.choice(wbp),
                              carla.Transform(w_loc, cross_tf.rotation))
    if w is None:
        return None, None, None
    # 行走方向直接由 行人生成点→横穿点 计算：用 -right 向量在部分 Town
    # 朝向约定下会走反（实测行人 4 秒走出 10m 远离横穿点，hz距cp 15.5m）
    wx, wy = cp.x - w_loc.x, cp.y - w_loc.y
    wn = math.hypot(wx, wy) or 1.0
    walk_dir = carla.Vector3D(x=wx / wn, y=wy / wn, z=0)
    return w, cp, walk_dir


def run_episode(world, ego, hazard, trigger_pt, walk_dir, scenario, grabber):
    """跑长 episode，返回 (帧列表, 碰撞帧号 or None)"""
    frames = []
    collision_frame = None
    min_cp = float('inf')   # ego 与碰撞点的历史最近距离（用于越过未撞提前放弃）

    bp = world.get_blueprint_library().find('sensor.other.collision')
    col_q = queue.Queue()
    col_sensor = world.spawn_actor(bp, carla.Transform(), attach_to=ego)
    col_sensor.listen(lambda e: col_q.put(e))

    try:
        # 预热 2.5 秒：ego 加速到巡航速度（不计入画面）
        # 追尾场景预热阶段也瞄准目标，先解决朝向问题再提速
        for _ in range(int(2.5 / DT)):
            if scenario == 'rear_end' and hazard is not None:
                steer = steer_toward(ego, hazard.get_location())
                hazard.apply_control(carla.VehicleControl(hand_brake=True))
                ego.apply_control(cruise(ego, steer))
                world.tick()
                grabber.clear()
                continue
            elif trigger_pt is not None:
                steer = steer_toward(ego, trigger_pt)
                ego.apply_control(cruise(ego, steer))
                world.tick()
                grabber.clear()
                continue
            else:
                steer = follow_steer(world, ego)
            ego.apply_control(carla.VehicleControl(throttle=0.42, steer=steer))
            world.tick()
            grabber.clear()

        for f in range(CAPTURE_MAX):
            ego_loc = ego.get_location()

            if scenario == 'rear_end':
                if hazard is not None:
                    steer = steer_toward(ego, hazard.get_location())
                    hazard.apply_control(carla.VehicleControl(hand_brake=True))
                else:
                    steer = follow_steer(world, ego)
                # 固定 0.40 油门在 Town05 陡坡爬不动（实测 1.6m/s 原地磨蹭），
                # 统一定速巡航
                ego.apply_control(cruise(ego, steer))
            elif scenario == 'side_impact':
                # ego 直接瞄准碰撞点开（车道保持版实测会游荡/卡死，
                # 整个 episode 车速 ~1m/s 根本到不了碰撞点）
                # 逼近碰撞点 5m 内锁定直行：贴脸时目标点横向微偏会
                # 被 steer_toward 放大成满舵甩尾，绕过堵路车（实测 hz距cp1.1m 仍 miss）
                if trigger_pt is not None:
                    steer = 0.0 if dist2d(ego_loc, trigger_pt) < 5.0 \
                        else steer_toward(ego, trigger_pt)
                else:
                    steer = follow_steer(world, ego)
                ego.apply_control(cruise(ego, steer))
                if hazard is not None and trigger_pt is not None:
                    d_h = dist2d(hazard.get_location(), trigger_pt)
                    if d_h <= 2.5:
                        # 侧车抢占碰撞点后刹停堵住路口——碰撞由几何保证，
                        # 不再赌"同时到达"的时间窗（实测两者总差 0.3~0.7s 必 miss）
                        hazard.apply_control(carla.VehicleControl(
                            brake=1.0, hand_brake=True))
                    elif dist2d(ego_loc, trigger_pt) < SIDE_TRIGGER:
                        hsteer = steer_toward(hazard, trigger_pt)
                        hazard.apply_control(carla.VehicleControl(
                            throttle=0.8, steer=hsteer))
            else:  # pedestrian
                if trigger_pt is not None:
                    steer = 0.0 if dist2d(ego_loc, trigger_pt) < 5.0 \
                        else steer_toward(ego, trigger_pt)
                else:
                    steer = follow_steer(world, ego)
                ego.apply_control(cruise(ego, steer))
                if hazard is not None and trigger_pt is not None:
                    if dist2d(ego_loc, trigger_pt) < PED_TRIGGER:
                        hazard.apply_control(carla.WalkerControl(
                            direction=walk_dir, speed=PED_SPEED))

            img = None
            for _ in range(TICKS_PER_FRAME):
                world.tick()
                img = grabber.get(timeout=15.0)
            frames.append(to_bgr(img))

            if not col_q.empty() and collision_frame is None:
                col_q.get()
                collision_frame = f

            if collision_frame is not None and f >= collision_frame + 6:
                break

            # 已越过碰撞点仍没撞上（侧撞/行人场景常见），提前结束省时间
            if collision_frame is None and trigger_pt is not None:
                d_cp = dist2d(ego_loc, trigger_pt)
                if d_cp < min_cp:
                    min_cp = d_cp
                elif min_cp < 4.0 and d_cp > 12.0:
                    break
    finally:
        try:
            col_sensor.stop()
        except Exception:
            pass
        try:
            col_sensor.destroy()
        except Exception:
            pass

    return frames, collision_frame, min_cp


def cut_window(frames, collision_frame):
    start = collision_frame - COLLISION_AT
    pad = 0
    if start < 0:
        # 碰撞落在第 17~19 帧：开头用首帧补齐，碰撞仍固定在输出第 20 帧
        pad = -start
        start = 0
    end = start + OUT_FRAMES - pad
    if end > len(frames):
        return None
    return [frames[0]] * pad + frames[start:end]


def quality_check(frames, weather):
    """废片检测：相机卡进车体/全黑/画面卡死。
    实测区分度：正常片 帧间差分~6.4 顶部亮度~113；废片 ~2.3 / ~50。
    """
    import cv2
    small = [cv2.cvtColor(cv2.resize(f, (320, 180)), cv2.COLOR_BGR2GRAY)
             .astype(np.float32) for f in frames]
    motion = float(np.mean([np.abs(small[i + 1] - small[i]).mean()
                            for i in range(len(small) - 1)]))
    if motion < 3.5:
        return '画面卡死(差分%.1f)' % motion
    top = float(np.mean([f[:60].mean() for f in small]))
    gstd = float(np.mean([f.std() for f in small]))
    if weather == 'night':
        if gstd < 15:
            return '夜间画面过平(std%.1f)' % gstd
    elif top < 70:
        return '顶部过暗(%.0f)，相机可能卡进车体' % top
    return None


def save_mp4(frames, path, fps=FPS):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp_path = path + '.part.mp4'
    w = cv2.VideoWriter(tmp_path, cv2.VideoWriter_fourcc(*'mp4v'), fps,
                        (IMG_W, IMG_H))
    if not w.isOpened():
        raise RuntimeError('VideoWriter open failed: ' + tmp_path)
    try:
        for f in frames:
            w.write(f)
    finally:
        w.release()
    if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
        raise RuntimeError('empty mp4: ' + tmp_path)
    os.replace(tmp_path, path)


def save_manifest(manifest, path):
    tmp_path = path + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)


def existing_combo_files(out_dir, weather, scenario):
    folder = os.path.join(out_dir, weather)
    prefix = 'carla_%s_%s_' % (weather, scenario)
    if not os.path.isdir(folder):
        return []
    return sorted(f for f in os.listdir(folder)
                  if f.startswith(prefix) and f.endswith('.mp4'))


def next_video_index(files):
    values = []
    for name in files:
        m = re.search(r'_(\d+)\.mp4$', name)
        if m:
            values.append(int(m.group(1)))
    return max(values) + 1 if values else 0


def configure_sync(world):
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = DT
    settings.max_substep_delta_time = 0.01
    settings.max_substeps = 10
    world.apply_settings(settings)
    return settings


def connection_failed(exc):
    msg = str(exc).lower()
    markers = ('time-out', 'timeout', 'connection refused', 'connection reset',
               'failed to connect', 'end of file', 'session')
    return any(x in msg for x in markers)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--port', type=int, default=2000)
    ap.add_argument('--weather', required=True, choices=['rainy', 'snowy', 'night', 'clear'])
    ap.add_argument('--scenario', required=True,
                    choices=['rear_end', 'side_impact', 'pedestrian'])
    ap.add_argument('--count', type=int, required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--max-fails', type=int, default=15)
    ap.add_argument('--max-new', type=int, default=0,
                    help='stop after this many new videos; 0 means no limit')
    args = ap.parse_args()

    rng = random.Random(args.seed)
    np.random.seed(args.seed)

    os.makedirs(args.out, exist_ok=True)
    manifest_path = os.path.join(args.out, 'manifest.json')
    manifest = []
    if os.path.exists(manifest_path):
        manifest = json.load(open(manifest_path, encoding='utf-8'))
    files = existing_combo_files(args.out, args.weather, args.scenario)
    done = len(files)
    first_index = next_video_index(files)
    print('已完成 %d / %d，继续' % (done, args.count), flush=True)

    client = carla.Client(args.host, args.port)
    # 正常 RPC 不应等待十分钟。服务端崩溃时要尽快交给外层看门狗重启。
    client.set_timeout(60.0)

    world = client.get_world()
    settings = configure_sync(world)

    bp_lib = world.get_blueprint_library()
    grabber = FrameGrabber()

    try:
        ok, fail, world = synth_loop(client, world, settings, bp_lib, grabber,
                                     args, rng, manifest, manifest_path, done,
                                     first_index)
    finally:
        # 关键：退出必须恢复异步模式，否则服务端永远停在同步态等新客户端 tick，
        # 后续所有客户端 get_world() 都会超时（本次踩过的坑）
        try:
            s = world.get_settings()
            s.synchronous_mode = False
            s.fixed_delta_seconds = None
            world.apply_settings(s)
            print('已恢复异步模式', flush=True)
        except Exception:
            pass

    print('完成: 成功 %d  失败 %d  清单 %s' % (ok, fail, manifest_path), flush=True)


def synth_loop(client, world, settings, bp_lib, grabber,
               args, rng, manifest, manifest_path, done, first_index):
    ok = fail = consecutive_fail = 0
    goal = args.count
    if args.max_new > 0:
        goal = min(goal, done + args.max_new)
    while done + ok < goal:
        # 同一地图连续生成 20 条，避免每条视频 load_world 造成流会话泄漏。
        town = TOWNS[((done + ok) // 20) % len(TOWNS)]
        try:
            if world.get_map().name.split('/')[-1] != town:
                client.set_timeout(90.0)
                world = client.load_world(town)
                settings = configure_sync(world)
                bp_lib = world.get_blueprint_library()
                grabber.clear()
                client.set_timeout(60.0)
        except Exception as e:
            print('  切图失败 %s: %s' % (town, e), flush=True)
            raise

        world.set_weather(make_weather(args.weather, rng))

        n_clr = clear_world(world)
        if n_clr:
            print('  清场: 移除 %d 个残留 actor' % n_clr, flush=True)
            world.tick()

        actors = []
        cam = None
        try:
            pts = list(world.get_map().get_spawn_points())
            rng.shuffle(pts)
            ego = None
            for p in pts[:20]:
                ego = spawn_vehicle(world, bp_lib, p, rng)
                if ego is not None:
                    break
            if ego is None:
                raise RuntimeError('ego 生成失败')
            actors.append(ego)
            world.tick()   # 同步模式：tick 后 ego 坐标才生效
            ego.set_light_state(carla.VehicleLightState(
                carla.VehicleLightState.LowBeam | carla.VehicleLightState.Position))

            hazard, trigger_pt, walk_dir = setup_hazard(
                world, bp_lib, ego, args.scenario, rng)
            if hazard is None:
                raise RuntimeError('危险物生成失败')
            actors.append(hazard)

            cam = build_camera(world, ego, grabber)

            frames, cframe, min_cp = run_episode(
                world, ego, hazard, trigger_pt, walk_dir, args.scenario, grabber)
            if cframe is None:
                d_miss = dist2d(ego.get_location(), hazard.get_location()) \
                    if hazard is not None else -1
                vel = ego.get_velocity()
                spd = math.sqrt(vel.x ** 2 + vel.y ** 2)
                el = ego.get_location()
                hl = hazard.get_location() if hazard is not None else None
                hz_cp = dist2d(hl, trigger_pt) \
                    if (hl is not None and trigger_pt is not None) else -1
                raise RuntimeError(
                    '未发生碰撞 (min_cp%.1f 距目标%.1fm 车速%.1fm/s hz距cp%.1fm ego[%.0f,%.0f] hz[%s])'
                    % (min_cp, d_miss, spd, hz_cp, el.x, el.y,
                       '%.0f,%.0f' % (hl.x, hl.y) if hl else 'None'))
            if cframe < MIN_LEAD_FRAMES:
                raise RuntimeError('碰撞太早(第%d帧)' % cframe)

            window = cut_window(frames, cframe)
            if window is None:
                raise RuntimeError('无法裁出 25 帧窗口(碰撞第%d帧 共%d帧)'
                                   % (cframe, len(frames)))
            bad = quality_check(window, args.weather)
            if bad:
                raise RuntimeError('废片: ' + bad)

            vid = 'carla_%s_%s_%03d' % (
                args.weather, args.scenario, first_index + ok)
            path = os.path.join(args.out, args.weather, vid + '.mp4')
            save_mp4(window, path)
            manifest.append(dict(
                video_id=vid, weather=args.weather, scenario=args.scenario,
                path=path, frames=len(window), collision_frame=COLLISION_AT,
                town=world.get_map().name.split('/')[-1],
                time=datetime.now().isoformat()))
            save_manifest(manifest, manifest_path)
            ok += 1
            consecutive_fail = 0
            print('  成功 %s（碰撞第%d帧）[%d/%d]' % (vid, cframe, done + ok, args.count),
                  flush=True)
        except RuntimeError as e:
            if connection_failed(e):
                raise
            fail += 1
            consecutive_fail += 1
            print('  失败(%d): %s' % (fail, e), flush=True)
        except Exception as e:
            if connection_failed(e):
                raise
            fail += 1
            consecutive_fail += 1
            print('  异常(%d): %s' % (fail, e), flush=True)
        finally:
            if cam is not None:
                grabber.close()
                try:
                    cam.stop()
                except Exception:
                    pass
                try:
                    cam.destroy()
                except Exception:
                    pass
            for a in reversed(actors):
                try:
                    a.destroy()
                except Exception:
                    pass
            # 同步模式中，销毁命令需要一个 tick 才会在服务端彻底落地。
            try:
                world.tick()
            except Exception:
                pass
            grabber.clear()

        if consecutive_fail >= args.max_fails:
            print('连续失败过多，中止', flush=True)
            break

    return ok, fail, world


if __name__ == '__main__':
    main()
