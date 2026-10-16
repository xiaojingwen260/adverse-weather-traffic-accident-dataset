# v1.0 最终验收审计报告（final_acceptance_audit.md）

- 审计对象：`D:\dataset_final_export\dataset_final\`（冻结 v1.0，全程只读）
- 审计时间：2026-10-05（脚本 audit_labels / audit_cross / audit_trace / audit_integrity / audit_near_dup / audit_near_dup_verify / spot_check 独立复核）
- 审计方式：所有结论由本次重新构建的脚本从 master 清单与磁盘逐项实测，不引用冻结期报告为唯一证据（冻结期报告仅作参考输入交叉核对）

---

## 一、最终结论

**C CONDITIONAL PASS —— 有条件通过（存在重要问题，修复后重新验收）**

## 二、一句话结论

**v1.0 可以正式冻结并进入 baseline 训练（检测 / 分类实验无阻碍）；但在预测任务（TTA / 提前量评估）上存在真实正样本碰撞帧缺失的重要问题，需先完成评估口径文档化（或由用户决策是否从源标注回填 collision_frame）后，预测实验结果方可采信。**

---

## 三、验收总表

| 检查项 | 状态 | 问题数量 | 最高严重程度 | 是否阻碍冻结 |
|---|---|---|---|---|
| 文件完整性 | PASS | 0 缺失 / 0 解码失败 / 0 空文件 / 0 缺帧 / 0 孤儿目录 / 0 重复 ID | — | 否 |
| 重复样本（MD5 级） | PASS | 2 组单帧重复（1 组跨样本 train 内末帧、1 组样本内相邻帧） | C | 否 |
| 深度近重复（感知哈希） | PASS | 严格疑似 36 对 → 逐帧复核全部排除（帧级平均最低 6.6） | — | 否 |
| train/val/test 泄漏 | PASS | group_id / original_video_id / sample_id 六对交集全 0；同源跨 split 0 | — | 否 |
| 标签一致性 | PASS | 标签逻辑自洽（A=0）；真实事故 collision_frame=null 1500 条（B） | B | **条件性**（见问题清单 B1） |
| prediction_eligible | PASS（体系自洽） | 早峰 175 全部 peak<18 且 false；无 false 但非 early；无 peak>=18 | C（文档 150 vs 实测 175） | 否（文档修正） |
| 数据划分 | PASS | 各集合数量/构成正确；互斥；不重抽样 | — | 否 |
| 类别分布 | PASS | 见第七节；稀少类别仅为风险提示 | D | 否 |
| 元数据 | PASS（如实记录缺口） | camera_type / day_night / source_url 字段缺失（映射口径已注明） | C | 否 |
| 来源可追溯性 | 部分（4796/4971） | CCD night 175 条本地源 mp4 无法定位（JPG 帧完整且已验收） | C | 否 |
| 标注质量抽检 | PASS（抽样 886 条 / 17.8%） | 天气与画面不一致约 31 条（3.5%）；事故可见性受缩略图限制多为 unclear | C | 否（建议复核） |
| manifest 一致性 | PASS | split json 集合与 master 完全一致；报告/README/handoff 数字一致 | — | 否 |

**最高严重程度 B（1 项，1500 条）→ 按用户规则「存在会实质影响实验可信度的 B 级问题时不建议无条件冻结」，结论为 C CONDITIONAL PASS。**

---

## 四、v1.0 最终统计（master 实测，可复现：scripts/audit_labels.py 输入 manifests/dataset_master.json）

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
| negative_type | adverse_no_accident 1826 / clear_accident 1554 / None(正) 1591 |
| prediction_eligible | true 4796 / false 175 |
| scenario | rear_end 900 / side_impact 900 / pedestrian 900 / unknown(真实) 2271 |
| camera_type | manifest 无字段（全部为前视行车记录仪视角，C 级缺口） |

**train（2700）**：合成 2160（80.000%）/ 真实 540（20.000%）；正 1350 / 负 1350；adverse_no_accident 675 + clear_accident 675；weather rainy 583 / snowy 674 / night 768 / clear 675；prediction_eligible true 2525 / false 175。
**val_real（200）**：100% 真实；正 100 / 负 100（adverse_no_accident 50 + clear_accident 50）；weather snowy 26 / rainy 37 / night 87 / clear 50。
**test_real（340，固定不重抽样）**：100% 真实；正 140 / 负 200（adverse_no_accident 140 + clear_accident 60）；weather snowy 90 / rainy 80 / night 110 / clear 60。
**reserve（1731）**：合成 540 / 真实 1191；正 1（crash_night_rainy_001100）/ 负 1730。

关键组合（combos）：real_accident 1525、real_nonaccident 746、syn_accident 1620、syn_nonaccident 1080、rainy_accident 476、snowy_accident 565、night_accident 550、adverse_accident 1591、adverse_nonaccident 1826、pe_true_real_accident 1525、pe_true_adverse_accident 1459、clear_accident_total 1554。

---

## 五、问题清单（只报告，未修改）

### B 级（重要，条件性阻碍）

**B1 —— 1500 条 CCD 事故样本 `collision_frame=null`（占全库 30.2%）**
- 范围：CCD 全部 accident=1 样本（486 条恶劣天气事故正样本 + 1014 条晴天事故 clear_accident 负样本）。DADA 25 条有 cf（20×23、7×1、13×1），CARLA 1620 条 cf=20，其余 CCD 事故均无碰撞帧标注。
- 影响：① 预测任务「碰撞帧位于 18~22 / TTA 提前量」对 486 条真实 CCD 正样本无法计算——pe=true 正样本中 cf 不在 [18,22] 的共 488 条（486 null + 2 DADA 越界）；② clear_accident 负样本要求「保留实际碰撞帧」未满足（字段 null）。
- 严重程度：B（实质影响预测任务在真实数据上的评估完整性；检测 / 分类任务不受影响）。
- 建议处理（供用户决策，审计不执行）：a) 从 CCD 源标注（ccd_layers 帧级标注或原始视频重新定位碰撞帧）回填 cf 后重新验收；或 b) 文档化评估口径——预测任务 TTA/提前量仅对碰撞帧已知样本（CARLA 合成 + DADA 25）计算，真实 CCD 正样本仅用于检测任务；两者择一并写入 README 与实验设计。
- 阻碍冻结：**是（对预测任务）**；检测/分类实验可不受影响地冻结。

### C 级（一般，不阻碍冻结，建议记录）

**C1 —— 175 条 CCD night 样本本地源 mp4 无法定位**（audit_trace）：JPG 帧完整且通过完整性验收（124,275 帧 0 缺失），但 `D:\dataset\CCD\ccd_adverse_v2\videos\` 下无对应原始 mp4（本地磁盘仅存 crash_day_normal 1014 / crash_day_rainy 106 / crash_day_snowy 205）。性质：来源级文件缺失（可能曾被清理或转帧时源位于其他路径），不影响帧数据本身；如需重新提取/复核原始视频需补源。其余 4796 条（CARLA 2700 / CCD 1325 / DADA 25 / BDD 746）可追溯。

**C2 —— 冻结期文档早峰数 150 vs 实测 175**（audit_labels）：冻结期记录「v2 107 + clear 43 = 150」；master 实测早峰 175（全部 CARLA train：正样本 132 + clear 43），peak<18 全部成立、early↔false 一一对应，标记体系自洽；差异 25 条无法仅凭清单解释（疑似 v2 期 MAD 口径变化）。纯文档偏差，不影响数据。

**C3 —— 标注质量抽检天气与画面不一致约 31 条（3.5%，886 条抽样）**：目检 886 条（17.8%，test_real 340 全 + 早峰 175 全 + 真实正样本 511 全 + 随机补足），其中约 24 条可精确匹配（CCD night「画面明亮」、CCD clear「画面有雪」、DADA rainy「画面无雨」、BDD snowy「画面无雪」等，源于 CCD/DADA 源数据自身标注口径差异）+ 7 条 BDD 行 sample_id 转录不完整无法精确匹配（判读员书写漏字符，非数据问题）。另有 3 条为「可见事故证据」（crash_day_snowy_000054 侧翻车、crash_day_snowy_001030 侧翻货车、crash_day_snowy_001415 抛起人体——正样本事故可见性确认，非矛盾）。事故可见性总体受 96px 缩略图限制，多数判为 unclear，不据此否定正负标签。建议：训练前对 C3 清单做定向复核（如需），不影响冻结。

**C4 —— 2 组单帧 MD5 重复**（audit_integrity + dup_locate）：① `carla_night_side_impact_023` 与 `carla_night_side_impact_033`（均 train）末帧 000025.jpg 完全相同——CARLA 同段素材结尾帧复用；② `crash_night_normal_000989`（val_real）样本内 000022.jpg == 000023.jpg——CCD 源视频静止帧。均不跨 split、无整条序列重复（duplicate_sample_sequence=0）、无泄漏；C 级观察项。

**C5 —— 元数据缺口**（audit_labels metadata_gaps）：camera_type、day_night、source_url 字段缺失；fog 无（源数据不含雾天）。day/night 按 night=夜间、其余=白天映射统计；camera 按来源文档均为前视行车记录仪视角。

### D 级（可接受，不作验收失败理由）

- 类别天然不均衡：真实 snow 事故 205、night 事故 175、DADA 仅 25 条；reserve 真实正样本仅 1 条 → v1.1 无法扩到 300（属未来扩展约束，非当前验收失败条件）。

---

## 六、最终回答 7 个问题

1. **当前 v1.0 是否足够支撑模型训练？** 是。正负 1350/1350、80/20 合成真实、四类天气与事故标签独立分列、group 级防泄漏、124,275 帧完整性 0 错误。
2. **是否足够支撑 validation？** 是。val_real 200 条 100% 真实，正 100/负 100，三类样本齐备（恶劣天气事故 / 恶劣天气无事故 / 正常天气事故），weather 覆盖 snowy/rainy/night/clear。
3. **是否足够支撑正式 test？** 检测 / 分类：是（test_real 340 固定真实，正 140/负 200，正负与天气分布完整）。预测任务（TTA）：受 B1 限制——340 中 200 条 CCD 正样本 cf=null，无法计算提前量；需按 B1 方案文档化口径或回填。
4. **是否存在数据泄漏？** 未发现任何级别的泄漏：sample_id/group_id/original_video_id 六对 split 交集全 0；来源级（source+original_video_id / town+场景+seed）跨 split 交集 0；MD5 序列重复 0；感知哈希 36 对严格疑似经逐帧复核全部排除（帧级平均距离最低 6.6，无一 ≤4）。
5. **是否存在必须先扩充数据才能开始训练的问题？** 否。现有 4971 条满足既定 5 组实验的训练规模；reserve 真实正样本不足仅约束 v1.1 未来扩充，不阻碍 v1.0 训练。
6. **当前 v1.0 是否还有必须完成的优化？** 有 1 项 B 级决策（B1：真实正样本碰撞帧回填或预测评估口径文档化，二选一）与 3 项 C 级记录（C1 源文件、C2 文档数字、C3 天气差异清单、C4 重复帧说明）。均为文档/口径层面，不要求修改数据本身。
7. **当前最合理下一步？** **冻结 v1.0**（保存最终 manifest、split、统计报告与哈希清单，后续实验固定使用）；对 B1 由用户决策后写入 README 评估口径；随后可开始 baseline 训练（检测 / 分类），预测实验在 B1 决策完成后进行。

---

## 七、冻结判定

**建议：正式冻结 v1.0 并进入训练阶段（检测 / 分类 baseline 可立即开始）。**

依据：不存在 A 级问题；唯一 B 级（B1，1500 条 collision_frame=null）不影响标签正确性、不构成泄漏、不损坏文件，仅约束预测任务在真实数据上的 TTA 评估完整性——通过「文档化评估口径」即可消除其对实验可信度的影响，无需修改数据或重新划分。C/D 级问题均为记录性、文档性或未来扩展约束，不构成冻结阻碍。

**冻结时须一并保存**：本次审计全部脚本与报告（scripts/audit_*.py、reports/audit_*.json/md、final_acceptance_aggregate.json、spot_check/ 全套），并将 B1 决策记录追加进 README（本次审计未写入 README/manifests/state.yaml/handoff，严格遵守只读边界）。

**若用户选择回填 collision_frame**：需从 CCD 源标注定位碰撞帧 → 修改 master → 重跑全部验收（框架完整性/标签/泄漏/加载器）→ 重新验收后解除 B1。

---

## 八、审计方法与命令记录

| 脚本 | 内容 | 输出 | 关键结果 |
|---|---|---|---|
| scripts/audit_labels.py | 标签逻辑/prediction_eligible/划分互斥/分布/元数据 | reports/audit_labels.json/md | A=0，B=1500（collision_frame）；pe 体系自洽；六对 split 三重交集 0 |
| scripts/audit_cross.py | master↔split json↔报告↔README↔handoff/state.yaml | reports/audit_cross.json/md | split 集合差异 {}；报告/README/handoff 一致；state current=07_training |
| scripts/audit_trace.py | 来源可追溯（本地源文件存在性） | reports/audit_trace.json/md | 4796 可追溯 / 175 CCD night 本地源缺失 |
| scripts/audit_integrity.py | 逐条 frame_dir + 全量 MD5 + 全量 cv2 解码 | reports/audit_integrity.json/md | 4971/124,275；0 缺失/0 解码失败/0 空/0 缺帧/0 孤儿/0 重复 ID；2 组单帧重复 |
| scripts/audit_integrity_dup_locate.py | 定位重复帧 MD5 归属 | reports/audit_integrity_dup_locate.json | CARLA train 末帧对 1 组 + CCD val 样本内 1 组 |
| scripts/audit_near_dup.py | 5 帧 dHash 跨 split 两两比对（7,134,440 对） | reports/audit_near_dup.json/md | le8=1105、le4=36；seg_near=0 |
| scripts/audit_near_dup_verify.py | 疑似对 25 帧逐帧精确复核 + 对比图 | reports/audit_near_dup_verify.json | 132 对全部排除（最低帧级平均 6.6） |
| scripts/spot_check_prep.py | 抽检 selection + contact sheet 渲染 | reports/spot_check/selection.json/csv、sheets/36 张 | 886 条（17.8%） |
| 目检子代理 ×2 | 886 条结构化判读（只读） | reports/spot_check/spot_result_part1/2.json | weather 不一致约 31 条；事故可见 4 例；early 目检受缩略图限制 |

所有命令：Windows PowerShell + python（3.14, cv2 5.0），后台长任务用 Start-Process + 日志轮询；全程未修改/删除/新增任何数据文件与标签。

---

## 附：审计中的局限（如实声明）

1. 目检事故可见性受 96px 缩略图限制：夜间/远距离事故多数判为 unclear，正样本标签的视觉确认仅 4 例明确；prediction_eligible 的早峰标记由 MAD 峰值数据（peak<18 全 175 条）验证，未做逐条视觉确认。
2. CCD night 175 条源 mp4 缺失，无法做源级帧复核（帧级完整性已由 MD5/解码覆盖）。
3. 7 条 BDD 目检行 sample_id 转录不完整（判读员书写问题），无法精确关联到 master；其「snowy 标签画面无雪」观察与 2 条可匹配 BDD 一致，列入 C3 待复核。
