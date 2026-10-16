# v1.0 最终验收审计 · 主清单与各清单/报告交叉一致性

审计时间：2026-10-05 14:39:16

## 1. master ↔ split json

| split | json 条数 | master 条数 | 集合差异 |
|---|---|---|---|
| train | 2700 | 2700 | 一致 |
| val_real | 200 | 200 | 一致 |
| test_real | 340 | 340 | 一致 |
| reserve | 1731 | 1731 | 一致 |

## 2. master 实测统计

| 维度 | 实测 |
|---|---|
| total | 4971 |
| split | {"train": 2700, "reserve": 1731, "val_real": 200, "test_real": 340} |
| target | {"1": 1591, "0": 3380} |
| domain | {"synthetic": 2700, "real": 2271} |
| weather | {"rainy": 885, "snowy": 987, "night": 1545, "clear": 1554} |
| source | {"CARLA": 2700, "CCD": 1500, "DADA": 25, "BDD100K": 746} |
| negative_type | {"null": 1591, "adverse_no_accident": 1826, "clear_accident": 1554} |

## 3. 报告交叉差异

| 检查 | 结果 |
|---|---|
| final_distribution | 一致 |
| final_reverify | PASS |
| loader_delivery_result | 4971/4971, errors=0 |
| README 关键数字 | 齐全 |
| state.yaml current | 07_training ✓ |
| handoff 关键数字 | 齐全 |

## 4. 结论

**PASS**
