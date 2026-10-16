# dataset_final 最终分布统计

生成时间：2026-10-04 18:20:24

总样本数：**4971**（v2 4431 + 新增 clear 540）

## 训练集比例

| 项 | 数值 |
|---|---|
| 合成 | 2160（80.000%）|
| 真实 | 540（20.000%）|
| 正样本(target=1) | 1350 |
| 负样本(target=0) | 1350 |
| adverse_no_accident | 675 |
| clear_accident | 675 |

## split × 主任务标签（target）

| split | 取值 | 数量 |
|---|---|---|
| train | 0 | 1350 |
| train | 1 | 1350 |
| val_real | 0 | 100 |
| val_real | 1 | 100 |
| test_real | 0 | 200 |
| test_real | 1 | 140 |
| reserve | 0 | 1730 |
| reserve | 1 | 1 |

## split × 域（domain）

| split | 取值 | 数量 |
|---|---|---|
| train | real | 540 |
| train | synthetic | 2160 |
| val_real | real | 200 |
| test_real | real | 340 |
| reserve | real | 1191 |
| reserve | synthetic | 540 |

## split × 天气（weather）

| split | 取值 | 数量 |
|---|---|---|
| train | clear | 675 |
| train | night | 768 |
| train | rainy | 583 |
| train | snowy | 674 |
| val_real | clear | 50 |
| val_real | night | 87 |
| val_real | rainy | 37 |
| val_real | snowy | 26 |
| test_real | clear | 60 |
| test_real | night | 110 |
| test_real | rainy | 80 |
| test_real | snowy | 90 |
| reserve | clear | 769 |
| reserve | night | 580 |
| reserve | rainy | 185 |
| reserve | snowy | 197 |

## split × 来源（source）

| split | 取值 | 数量 |
|---|---|---|
| train | BDD100K | 135 |
| train | CARLA | 2160 |
| train | CCD | 405 |
| val_real | BDD100K | 50 |
| val_real | CCD | 125 |
| val_real | DADA | 25 |
| test_real | BDD100K | 140 |
| test_real | CCD | 200 |
| reserve | BDD100K | 421 |
| reserve | CARLA | 540 |
| reserve | CCD | 770 |

## split × 负样本类型（negative_type）

| split | 取值 | 数量 |
|---|---|---|
| train | None | 1350 |
| train | adverse_no_accident | 675 |
| train | clear_accident | 675 |
| val_real | None | 100 |
| val_real | adverse_no_accident | 50 |
| val_real | clear_accident | 50 |
| test_real | None | 140 |
| test_real | adverse_no_accident | 140 |
| test_real | clear_accident | 60 |
| reserve | None | 1 |
| reserve | adverse_no_accident | 961 |
| reserve | clear_accident | 769 |

## split × accident/adverse_weather（accident_x_adverse）

| split | 取值 | 数量 |
|---|---|---|
| train | 0/1 | 675 |
| train | 1/0 | 675 |
| train | 1/1 | 1350 |
| val_real | 0/1 | 50 |
| val_real | 1/0 | 50 |
| val_real | 1/1 | 100 |
| test_real | 0/1 | 140 |
| test_real | 1/0 | 60 |
| test_real | 1/1 | 140 |
| reserve | 0/1 | 961 |
| reserve | 1/0 | 769 |
| reserve | 1/1 | 1 |

## domain × target

| domain | target | 数量 |
|---|---|---|
| real | 0 | 1760 |
| real | 1 | 511 |
| synthetic | 0 | 1620 |
| synthetic | 1 | 1080 |

## domain × negative_type

| domain | negative_type | 数量 |
|---|---|---|
| real | None | 511 |
| real | adverse_no_accident | 746 |
| real | clear_accident | 1014 |
| synthetic | None | 1080 |
| synthetic | adverse_no_accident | 1080 |
| synthetic | clear_accident | 540 |