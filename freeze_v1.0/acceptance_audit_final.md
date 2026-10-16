# v1.0 最终验收审计 · 定稿（acceptance_audit_final.md）

> 本文件为冻结定稿版本，基于 `reports/final_acceptance_audit.md` 并追加「正式冻结决策记录」。
> 审计过程与全部实测数据见 `reports/` 下各审计报告（audit_labels / audit_cross / audit_trace / audit_integrity / audit_near_dup / audit_near_dup_verify / spot_check），冻结产物哈希见 `freeze_v1.0/`。

---

## 一、审计结论（原始）

- 原始判定：**C CONDITIONAL PASS —— 有条件通过**（存在重要问题 B1，修复后重新验收）。
- A 级问题：0；B 级问题：1 项（1500 条 CCD 事故样本 collision_frame=null）；C 级：5 项；D 级：可接受。

## 二、正式冻结决策记录（2026-10-05，用户选择方案 a）

1. **B1 处理方式**：文档化口径，直接冻结 v1.0；不对数据做任何层改动；不对 CCD collision_frame 做自动估算并当作真值。
2. **预测任务评估口径**：
   - TTA / time-to-accident / collision lead time 仅在 collision_frame 有真实标注的事故正样本上计算：CARLA 事故正 **1080**（cf=20）+ DADA **25**（cf 真值）＝ **1105** 条；其中 prediction_eligible=true **973** 条；
   - **486 条 CCD 真实恶劣天气事故正样本（collision_frame=null）不在 TTA 评价范围**，仅用于事故检测/分类等不依赖 collision_frame 的实验；
   - 不允许 estimated collision frame 与人工真值混合报告。
3. **B1 不阻碍检测/分类实验；预测任务中仅限制 TTA 评价样本范围。**
4. **最终结论（定稿）：v1.0 正式冻结，可进入 baseline 训练。**

## 三、验收总表（实测，与定稿一致）

| 检查项 | 状态 | 问题数 | 最高严重程度 | 是否阻碍冻结 |
|---|---|---|---|---|
| 文件完整性 | PASS | 0 缺失/0 解码失败/0 空/0 缺帧/0 孤儿/0 重复 ID | — | 否 |
| 重复样本（MD5） | PASS | 2 组单帧（不跨 split） | C | 否 |
| 深度近重复 | PASS | 36 对严格疑似逐帧复核全部排除 | — | 否 |
| train/val/test 泄漏 | PASS | sample_id/group_id/original_video_id 六对交集全 0；感知哈希近重复 0 | — | 否 |
| 标签一致性 | PASS | 逻辑自洽 A=0；B1=1500 条 cf=null（文档化） | B→已决策 | 否（文档化后） |
| prediction_eligible | PASS | 体系自洽（175 早峰 peak<18 全成立） | C | 否 |
| 数据划分 | PASS | 各集合数量/构成正确、互斥、不重抽样 | — | 否 |
| 类别分布 | PASS | 稀少类别仅为风险提示 | D | 否 |
| 元数据 | PASS | camera_type/day_night/source_url 缺口（口径注明） | C | 否 |
| 来源可追溯 | 部分 | 4796/4971；CCD night 175 本地源缺失（帧完整） | C | 否 |
| 标注抽检 | PASS | 886 条（17.8%）；天气差异约 31 条（3.5%） | C | 否（建议复核） |
| manifest 一致性 | PASS | split json 与 master 集合差异 {}；报告/README/handoff 一致 | — | 否 |

## 四、v1.0 最终统计（master 实测）

| 维度 | 数值 |
|---|---|
| 总样本 | 4971 |
| JPG 帧 | 124,275（4971×25） |
| split | train 2700 / val_real 200 / test_real 340 / reserve 1731 |
| target | 正 1591 / 负 3380 |
| domain | synthetic 2700 / real 2271 |
| weather | rainy 885 / snowy 987 / night 1545 / clear 1554 |
| source | CARLA 2700 / CCD 1500 / DADA 25 / BDD100K 746 |
| accident | 1: 3145 / 0: 1826 |
| negative_type | adverse_no_accident 1826 / clear_accident 1554 / None 1591 |
| prediction_eligible | true 4796 / false 175 |
| scenario | rear_end 900 / side_impact 900 / pedestrian 900 / unknown 2271 |
| camera_type | manifest 无字段（前视行车记录仪视角，C 级） |

train 2700：合成 2160（80.000%）/ 真实 540（20.000%）；正 1350 / 负 1350；adverse_no_accident 675 + clear_accident 675。
val_real 200：100% 真实；正 100 / 负 100（50+50）；weather snowy 26 / rainy 37 / night 87 / clear 50。
test_real 340：100% 真实、固定；正 140 / 负 200（adverse_no_accident 140 + clear_accident 60）。
reserve 1731：合成 540 / 真实 1191；正 1 / 负 1730。

## 五、问题清单（冻结状态）

- **B1（已文档化）**：CCD 事故 1500 条 collision_frame=null（486 正 + 1014 clear_accident）；486 条真实正样本不参与 TTA 评价；仍可用于检测/分类。详见 known_limitations_v1.0.md。
- **C1**：CCD night 175 条本地源 mp4 缺失（帧完整）。
- **C2**：早峰文档 150 vs 实测 175（纯文档偏差）。
- **C3**：目检天气差异约 31 条（3.5%）。
- **C4**：2 组单帧 MD5 重复（不跨 split）。
- **C5**：camera_type / day_night / source_url 元数据缺口。
- **D**：类别天然不均衡；reserve 真实正样本 1 条（v1.1 约束，非 v1.0 失败条件）。

## 六、7 问定位（定稿）

1. 支撑训练：**是**（正负 1350/1350、80/20、防泄漏完备）。
2. 支撑 validation：**是**（val_real 200 全真实，正负 100/100，三类样本齐备）。
3. 支撑 test：**是**（test_real 340 固定真实；预测任务 TTA 按上述口径在 1105 条真值样本上评估）。
4. 数据泄漏：**未发现任何级别泄漏**。
5. 必须先扩充才能训练：**否**。
6. 必须完成的优化：**无数据层必须项**（B1 已文档化；C 级为记录/建议）。
7. 下一步：**冻结 v1.0，进入 baseline 训练（检测/分类），预测实验按 B1 口径执行。**

## 七、冻结判定（定稿）

**v1.0 正式冻结（2026-10-05）。** 不存在 A 级问题；B1 经用户决策以文档化口径处理，不阻碍检测/分类实验、仅限制预测任务 TTA 评价样本范围；C/D 级均为记录性/文档性。保存冻结产物于 `freeze_v1.0/`（版本信息、清单哈希指针、split 哈希、统计快照、审计引用、已知限制、本定稿），后续所有实验使用该冻结版本，不再直接修改 v1.0。
