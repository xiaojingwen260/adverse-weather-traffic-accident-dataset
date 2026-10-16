# dataset_final 阶段 1 · 数据审计报告（pre-split inventory）

- 输入：`D:\dataset_v2_export\dataset_v2\dataset_planB_v2.json`（4431 条，交付包相对路径版）
- 输出：`reports\pre_split_inventory.{json,csv,md}`（本文件）
- 日期：2026-10-04；本阶段只读，未重新划分数据，未启动 CARLA/训练

## 1. 六类样本统计（主任务定义：target = accident AND adverse_weather）

| 类别 | 定义 | 数量 |
|---|---|---:|
| syn_adverse_acc | synthetic + 恶劣天气事故 | 1080 |
| syn_adverse_noacc | synthetic + 恶劣天气无事故 | 1080 |
| syn_clear_acc | synthetic + 晴天事故 | 0 |
| real_adverse_acc | real + 恶劣天气事故 | 511 |
| real_adverse_noacc | real + 恶劣天气无事故 | 746 |
| real_clear_acc | real + 晴天事故 | 1014 |
| syn_clear_noacc | synthetic + 晴天无事故 | 0 |
| real_clear_noacc | real + 晴天无事故 | 0 |

总计 4431 条；sample_id 重复 0；晴天无事故（两类）合计 0（该类不进入主任务，应入 reserve）

## 2. 维度分布

| 维度 | 分布 |
|---|---|
| source | bdd100k_mot=746, carla_neg_v2=1080, carla_synth_v2=1080, ccd_real=1500, dada_real=25 |
| weather | clear=1014, night=1545, rainy=885, snowy=987 |
| domain | real=2271, synthetic=2160 |
| accident | 0=1826, 1=2605 |
| target | 0=2840, 1=1591 |
| negative_type | None=1591, adverse_no_accident=1826, clear_accident=1014 |
| split(v2) | test=1180, train=2315, val=936 |
| scenario | None=2271, pedestrian=720, rear_end=720, side_impact=720 |
| town(CARLA) | None=2271, Town01=704, Town02=362, Town04=362, Town05=373, Town10HD_Opt=359 |
| collision_frame（有碰撞帧的正样本 1105 条） | 7=1, 13=1, 20=1103 |

## 3. 六类 × split(v2)

| 类别 \ split | train | val | test |
|---|---|---:|---:|---:|
| syn_adverse_acc | 300 | 360 | 420 |
| syn_adverse_noacc | 300 | 360 | 420 |
| syn_clear_acc | 0 | 0 | 0 |
| real_adverse_acc | 314 | 57 | 140 |
| real_adverse_noacc | 545 | 61 | 140 |
| real_clear_acc | 856 | 98 | 60 |
| syn_clear_noacc | 0 | 0 | 0 |
| real_clear_noacc | 0 | 0 | 0 |

## 4. weather × domain × accident

| weather | domain | accident | n |
|---|---|---|---:|
| clear | real | 1 | 1014 |
| night | real | 0 | 635 |
| night | synthetic | 0 | 360 |
| night | synthetic | 1 | 360 |
| rainy | synthetic | 0 | 360 |
| rainy | synthetic | 1 | 360 |
| snowy | synthetic | 0 | 360 |
| snowy | synthetic | 1 | 360 |
| snowy | real | 1 | 205 |
| night | real | 1 | 190 |
| rainy | real | 1 | 116 |
| snowy | real | 0 | 62 |
| rainy | real | 0 | 49 |

## 5. TEST_REAL 340 构成（v2 固定，不得重新抽样）

| source | weather | accident | negative_type | n |
|---|---|---|---|---:|
| bdd100k_mot | night | 0 | adverse_no_accident | 60 |
| ccd_real | clear | 1 | clear_accident | 60 |
| ccd_real | night | 1 | None | 50 |
| ccd_real | snowy | 1 | None | 50 |
| bdd100k_mot | rainy | 0 | adverse_no_accident | 40 |
| bdd100k_mot | snowy | 0 | adverse_no_accident | 40 |
| ccd_real | rainy | 1 | None | 40 |

## 6. 关键发现（供缺口判断）

- **synthetic + 晴天事故 = 0**（CARLA 合成仅 rainy/snowy/night；训练结构要求的合成正常天气事故负样本需新增生成或调整方案）→ 详见 `reports\synthetic_clear_accident_gap.md`
- 晴天无事故（两类）= 0（本就无此数据，reserve 为空类）
- real 恶劣天气事故按天气：{'night': 190, 'rainy': 116, 'snowy': 205}
- real 恶劣天气无事故按天气：{'night': 635, 'rainy': 49, 'snowy': 62}
- 训练结构可行性（推荐 2700 方案）所需的 real 侧供给：恶劣天气事故正 ≥270（可用 511）、恶劣天气无事故负 ≥135（可用 746）、晴天事故负 ≥135（可用 1014）

## 7. 来源
- 全部数字由 `scripts\audit_v2.py` 从输入清单实测统计；可复现。CARLA jpg 均大小 145862 B（54000 张，供缺口估算）。