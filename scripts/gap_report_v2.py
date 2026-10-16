# -*- coding: utf-8 -*-
"""gap_report_v2.py — 阶段 2：synthetic 晴天事故缺口报告
输入：pre_split_inventory.json（阶段 1 产物）；mp4 均大小实测常量（2026-10-04 PowerShell 实测）
输出：D:\\dataset_final_export\\dataset_final\\reports\\synthetic_clear_accident_gap.md
结论性要求：当前数量；还缺多少；建议生成数量；场景分配；预计新增数据量；是否需要重跑 CARLA。
"""
import json, os

REPORTS = r'D:\dataset_final_export\dataset_final\reports'
inv = json.load(open(os.path.join(REPORTS, 'pre_split_inventory.json'), encoding='utf-8'))

cur = inv['six_class']['syn_clear_acc']
TARGET = 540                      # 用户推荐目标：合成晴天事故 540
ALLOC = {'rear_end': 180, 'side_impact': 180, 'pedestrian': 180}
JPG_AVG = inv['carla_jpg_avg_bytes']       # 145862 B（实测）
MP4_AVG_MB = 1.06                            # 实测：carla 正样本 mp4 均值（1.12GB/1080）
FPS = 25

frames_new = TARGET * FPS
jpg_gb = frames_new * JPG_AVG / 1e9
mp4_gb = TARGET * MP4_AVG_MB / 1024
total_gb = jpg_gb + mp4_gb

# 结构推导（用户推荐 2700 训练方案下的缺口）
# 目标结构：S_pos=1080, S_neg1(adverse_noacc)=540, S_neg2(clear_acc)=540, R=540(270/135/135)
# 需求方程：S/T=0.8±0.5% → X∈[474,609]（S=1620+X, T=2160+X）
x_low = 474; x_high = 609
# 最低可行性：pos=neg=50% 且 80/20 约束 → X≥108（仅满足约束、牺牲两类负样本均衡）
x_min = 108

# 若不生成的最接近方案（X=0）：S=1620, T=2160 → 75.0%，超出 ±0.5% 容差
fallback_ratio = 1620 / 2160 * 100

L = []
A = L.append
A('# 合成晴天事故缺口报告（synthetic_clear_accident_gap）')
A('')
A('- 日期：2026-10-04 · 输入：`pre_split_inventory.json` · 只读审计结论')
A('')
A('## 1. 当前数量')
A('')
A('- **synthetic + accident=1 + weather=clear（adverse_weather=0） = %d 条**（实测，全库 %d 条中仅 %d 条）' % (cur, inv['total'], cur))
A('- 原因：CARLA 合成仅生成 rainy/snowy/night 三套天气（正样本 1080、负样本 1080），从未生成晴天事故。')
A('- 禁止补足手段（按指令）：不得复制样本、不得修改标签、不得把恶劣天气事故伪装成晴天事故。')
A('')
A('## 2. 目标与缺口')
A('')
A('训练集推荐结构（2700 方案）要求两类负样本：恶劣天气无事故 675 = 合成 540 + 真实 135；')
A('正常天气事故 675 = 合成 540 + 真实 135。')
A('')
A('| 项 | 值 |')
A('|---|---|')
A('| 当前合成晴天事故 | **%d** |' % cur)
A('| 结构需要 | **%d**（追尾 %d / 侧撞 %d / 行人 %d） |' % (TARGET, ALLOC['rear_end'], ALLOC['side_impact'], ALLOC['pedestrian']))
A('| 缺口 | **%d** |' % (TARGET - cur))
A('| 80/20±0.5%% 容差内可行区间（固定 S_pos=1080/S_neg1=540/R=540） | 合成晴天事故 X∈[%d, %d] |' % (x_low, x_high))
A('| 最低可行性（仅满足 80/20 与正负 50/50，牺牲两类负样本均衡） | X≥%d |' % x_min)
A('')
A('## 3. 建议生成方案')
A('')
A('- **建议生成 540 条合成晴天事故**（= 用户推荐目标）：weather=clear，场景 = rear_end 180 / side_impact 180 / pedestrian 180；')
A('  城镇/seed 轮换沿用 batch_v2 机制（5 城镇，每 20 条轮换，运行级 seed），25 帧 @5fps，碰撞帧第 20 帧。')
A('- 新增数据量估算（按实测均大小）：')
A('  - mp4：540 条 × 均 1.06 MB ≈ **%.2f GB**（实测源：`D:\\dataset\\carla_out_v2` 1.12GB/1080，2026-10-04 实测）' % mp4_gb)
A('  - JPG：540 × 25 = **13,500 张** × 均 145,862 B ≈ **%.2f GB**（实测源：交付包 CARLA 54,000 张均大小）' % jpg_gb)
A('  - 合计 ≈ **%.2f GB**（另加清单/日志开销可忽略）' % total_gb)
A('')
A('## 4. 是否需要重新运行 CARLA')
A('')
A('- **是（推荐）**：需在服务器 `/data/xiaojingwen/` 下用 carla 合成脚本批量生成 540 条 weather=clear 事故 episode，'
  '随后下载 mp4、本地转帧 25 帧、并入 `D:\\dataset_final_export\\dataset_final\\frames\\CARLA_ACCIDENT\\`，并写入主清单。')
A('- **若不生成（备选）**：最接近方案 X=0 → 训练集 S=1620 / T=2160 → 合成占比 **%.1f%%**，超出 80/20±0.5%% 容差；'
  '且正常天气事故负样本仅剩真实 135 条（两类负样本 675/135 严重失衡）。不建议。' % fallback_ratio)
A('- **中间量**：若只生成 X∈[108, 474)，可满足 80/20±0.5%% 与正负 50/50，但正常天气事故负样本的合成/真实配比无法达到 540/135 的目标结构。')
A('')
A('## 5. 等待用户确认')
A('')
A('**按指令：未经用户确认不得启动新的 CARLA 批量合成。** 请确认：')
A('1. 生成 540 条（推荐，180/180/180）？')
A('2. 或指定其他数量（≥108 才可维持 80/20±0.5%% 与正负 50/50）？')
A('3. 或暂不生成（接受 75/25 比例的缩减方案）？')
A('')
A('## 6. 来源')
A('- 六类统计/维度分布：`pre_split_inventory.json`（脚本 `scripts\\audit_v2.py` 实测）')
A('- CARLA mp4 均大小：`D:\\dataset\\carla_out_v2` 1080 文件 1.12GB（2026-10-04 PowerShell `Get-ChildItem | Measure-Object`）')
A('- CARLA jpg 均大小：交付包 `frames\\carla_synth_v2` + `carla_neg_v2` 54,000 张（`audit_v2.py` 实测）')

md = '\n'.join(L)
out = os.path.join(REPORTS, 'synthetic_clear_accident_gap.md')
open(out, 'w', encoding='utf-8').write(md)
print('gap report ->', out)
print('cur=%d target=%d frames_new=%d jpg_gb=%.2f mp4_gb=%.2f total_gb=%.2f fallback=%.1f%%'
      % (cur, TARGET, frames_new, jpg_gb, mp4_gb, total_gb, fallback_ratio))
