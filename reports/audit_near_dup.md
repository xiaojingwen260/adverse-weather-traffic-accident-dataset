# v1.0 最终验收审计 · 重复与深度近重复/泄漏

审计时间：2026-10-05 14:44:07（耗时 167s）

方法：L1 MD5/序列MD5(见 audit_integrity)；L2 5帧dHash按位多数指纹 跨split两两汉明(numpy 分块，pair=7134440)；L3 CARLA 运行段内 5 帧序列精确比较

| 项 | 值 |
|---|---|
| 参与样本 | 4971 |
| 跨 split 比对对数 | 7134440 |
| 疑似（汉明<=8） | 1105 |
| 严格疑似（汉明<=4） | 36 |
| CARLA 运行段内近重复（序列汉明<=20） | 0 |
| 结论 | **NEAR_DUP_FOUND** |

## 严格疑似对（<=4）

| A | B | 汉明 | 跨集 | 域 | 来源 |
|---|---|---|---|---|---|
| carla_snowy_pedestrian_085 | crash_day_normal_000657 | 4 | train-val_real | synthetic-real | CARLA-CCD |
| crash_day_snowy_001105 | crash_day_snowy_000303 | 2 | train-val_real | real-real | CCD-CCD |
| carla_rainy_rear_end_000 | carla_neg_rainy_side_impact_000 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_rainy_rear_end_000 | carla_neg_rainy_pedestrian_032 | 3 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_rainy_rear_end_000 | carla_neg_rainy_pedestrian_099 | 3 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_rainy_rear_end_047 | carla_neg_rainy_pedestrian_032 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_rainy_rear_end_047 | carla_neg_rainy_pedestrian_099 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_rainy_rear_end_047 | carla_neg_snowy_pedestrian_091 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_rainy_side_impact_030 | carla_neg_rainy_pedestrian_032 | 2 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_rainy_side_impact_101 | carla_neg_rainy_side_impact_000 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_snowy_rear_end_035 | carla_neg_snowy_pedestrian_033 | 3 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_snowy_rear_end_065 | carla_neg_rainy_pedestrian_032 | 2 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_snowy_rear_end_065 | carla_neg_snowy_rear_end_066 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_snowy_rear_end_075 | carla_neg_rainy_pedestrian_032 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_snowy_rear_end_075 | carla_neg_snowy_rear_end_066 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_snowy_rear_end_093 | carla_neg_snowy_pedestrian_091 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_snowy_side_impact_025 | carla_neg_rainy_pedestrian_032 | 3 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_snowy_side_impact_035 | carla_neg_rainy_pedestrian_032 | 3 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_snowy_pedestrian_085 | carla_neg_snowy_rear_end_032 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_snowy_pedestrian_085 | crash_day_normal_000459 | 4 | train-reserve | synthetic-real | CARLA-CCD |
| carla_neg_rainy_rear_end_035 | carla_neg_rainy_side_impact_030 | 3 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_neg_rainy_side_impact_018 | carla_neg_snowy_rear_end_066 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_neg_rainy_pedestrian_026 | carla_neg_rainy_pedestrian_032 | 3 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_neg_rainy_pedestrian_114 | carla_neg_rainy_side_impact_016 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_neg_snowy_rear_end_023 | carla_neg_rainy_side_impact_016 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_neg_snowy_rear_end_023 | carla_neg_rainy_side_impact_026 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_neg_snowy_rear_end_023 | carla_neg_snowy_rear_end_032 | 3 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_neg_snowy_rear_end_025 | carla_neg_snowy_rear_end_032 | 3 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_neg_snowy_side_impact_029 | carla_neg_rainy_side_impact_016 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_neg_snowy_side_impact_029 | carla_neg_snowy_rear_end_032 | 3 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_neg_snowy_side_impact_037 | carla_neg_snowy_pedestrian_070 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_neg_snowy_side_impact_069 | carla_neg_snowy_rear_end_032 | 4 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_neg_snowy_pedestrian_025 | carla_neg_snowy_side_impact_030 | 2 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_clear_side_impact_002 | carla_neg_rainy_pedestrian_032 | 3 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| carla_clear_side_impact_002 | carla_neg_snowy_pedestrian_091 | 3 | train-reserve | synthetic-synthetic | CARLA-CARLA |
| 018aca44-9a616a49 | crash_day_normal_000200 | 4 | test_real-reserve | real-real | BDD100K-CCD |
