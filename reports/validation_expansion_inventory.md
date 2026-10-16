# dataset_final v1.1 验证集扩充 · 第一步只读审计（reserve 候选）

审计时间：2026-10-04 18:40:10

输入：`manifests/dataset_master.json`（冻结 v1.0，只读）；reserve 共 **1731** 条。

## 候选定义与数量

| 类别 | 定义 | 数量 | 闸门要求 | 是否通过 |
|---|---|---|---|---|
| 正样本候选 | real ∧ accident=1 ∧ adverse_weather=1 ∧ target=1 ∧ prediction_eligible=true | 1 | ≥50 | **不通过** |
| 负样本A候选 | real ∧ accident=0 ∧ adverse_weather=1 ∧ negative_type=adverse_no_accident | 421 | ≥25 | 通过 |
| 负样本B候选 | real ∧ accident=1 ∧ adverse_weather=0 ∧ negative_type=clear_accident | 769 | ≥25 | 通过 |

## 各候选详细统计

### 正样本候选(pos)（1 条）

| 维度 | 分布 |
|---|---|
| weather | {"night": 1} |
| source | {"CCD": 1} |
| prediction_eligible | {"true": 1} |
| quality_flag | {"": 1} |
| 唯一 original_video_id | 1 |
| 唯一 group_id | 1 |

### 负样本A候选(adverse_no_accident)（421 条）

| 维度 | 分布 |
|---|---|
| weather | {"night": 398, "snowy": 17, "rainy": 6} |
| source | {"BDD100K": 421} |
| prediction_eligible | {"true": 421} |
| quality_flag | {"": 421} |
| 唯一 original_video_id | 421 |
| 唯一 group_id | 421 |

### 负样本B候选(clear_accident)（769 条）

| 维度 | 分布 |
|---|---|
| weather | {"clear": 769} |
| source | {"CCD": 769} |
| prediction_eligible | {"true": 769} |
| quality_flag | {"": 769} |
| 唯一 original_video_id | 769 |
| 唯一 group_id | 769 |

### 正样本候选 sample_id 全清单

```
crash_night_rainy_001100
```

## 闸门判定

**闸门未通过：正样本候选 1 < 50（reserve 中真实恶劣天气事故正样本实际仅剩 1 条）。按指令不修改任何清单、不复制/重复使用样本、不下载、不生成 CARLA；输出缺口报告并停止等待用户确认。**

可达最大平衡规模（按三类中最小者）：**1**（正 1 / 负A 1 / 负B 1）

## 缺口说明

reserve 中真实恶劣天气事故正样本**实际仅剩 1 条**（CCD 恶劣天气事故总量 486，train 已用 270 / 原 val_real 已用 75 / test_real 已用 140，余 1）。DADA 25 条已全部在原 val_real；负样本A 候选仅 BDD（421）；负样本B 候选仅 CCD（769）。

按用户指令：任一不足 → **不修改任何清单、不复制/重复使用样本、不下载、不生成 CARLA，停止并等待用户确认**。
