# v1.0 已知限制说明（known_limitations_v1.0.md）

- 数据集版本：v1.0（2026-10-05 正式冻结）
- 本文档冻结产物位置：`D:\dataset_final_export\dataset_final\freeze_v1.0\`
- 说明：以下均为已知限制/观察项，按严重程度列出；数据层未做任何修改，全部来自本次最终验收审计的独立复核（reports/audit_*.json/md）。

---

## B1（重要，已由用户决策为文档化口径）— CCD 事故样本 collision_frame=null

- 数量：**1500 条**（CCD 全部 accident=1 样本）＝ 486 条真实恶劣天气事故正样本 + 1014 条 clear_accident 负样本。
- 影响：
  - **486 条真实恶劣天气事故正样本不得参与 TTA / 碰撞提前量评价**（collision_frame 缺失）；
  - 这些样本仍允许用于事故检测、分类及其他不依赖 collision_frame 的实验；
  - 1014 条 clear_accident 负样本的「实际碰撞帧」字段同样为 null（不影响其负样本标签与检测/分类用途）。
- 决策（2026-10-05 用户选择方案 a）：**文档化口径，直接冻结 v1.0，不做数据层改动、不对 CCD collision_frame 做自动估算**。

### 预测任务评估口径（写入 README 冻结记录）

1. **TTA / time-to-accident / collision lead time 仅在 collision_frame 有真实标注的样本上计算**：即 CARLA 事故正样本 **1080** 条（cf=20）+ DADA **25** 条（cf 真值：20×23、7×1、13×1），合计 **1105** 条；其中 prediction_eligible=true **973** 条（CARLA 1080−早峰 132 + DADA 25）。
2. **不允许对 CCD 的 collision_frame 做自动估算并当作真值使用**。
3. **不允许将 estimated collision frame 与人工真值混合报告**。
4. 另有 CARLA clear_accident 负样本 540 条（cf=20，生成真值）——属负样本，不计入 TTA 正样本评价；可用于负样本窗口核对。
5. **B1 不阻碍检测/分类实验；预测任务中仅限制 TTA 评价样本范围。**

---

## C 级（一般观察项，不阻碍冻结）

### C1 — 175 条 CCD night 样本本地源 mp4 无法定位
- JPG 帧完整且通过完整性验收（124,275 帧 0 缺失 / 0 解码失败）；`D:\dataset\CCD\ccd_adverse_v2\videos\` 下无对应原始 mp4（本地仅有 crash_day_normal 1014 / crash_day_rainy 106 / crash_day_snowy 205）。
- 如需重新提取/复核原始视频需补源；不影响帧数据本身。

### C2 — 早峰文档数字偏差（冻结期文档 150 vs 实测 175）
- 实测：早峰 175 条（全部 CARLA train：事故正 132 + clear 43），peak<18 全部成立、early↔prediction_eligible=false 一一对应，标记体系自洽；
- 冻结期文档记录「v2 107 + clear 43 = 150」，差额 25 疑似 v2 期 MAD 检测口径变化——纯文档偏差，不影响数据。

### C3 — 标注质量抽检天气与画面不一致约 31 条（3.5%，抽样 886 条）
- 目检 886 条（17.8%）中 weather_visual=no 共 31 条；可精确匹配 24 条（CCD night「画面明亮」、CCD clear「画面有雪」、DADA rainy「画面无雨」、BDD snowy「画面无雪」等，源于 CCD/DADA 源数据自身标注口径差异）+ 7 条 BDD 行 sample_id 转录不完整无法精确匹配（判读员书写问题，非数据问题）。
- 另有 3 条为「可见事故证据」确认（crash_day_snowy_000054 侧翻车 / 001030 侧翻货车 / 001415 抛起人体），非矛盾。
- 建议：训练前如需可对 C3 清单定向复核；不阻碍冻结。

### C4 — 2 组单帧 MD5 重复（不跨 split、无整条序列重复）
1. `carla_night_side_impact_023` 与 `carla_night_side_impact_033`（均 train）末帧 000025.jpg 完全相同——CARLA 同段素材结尾帧复用；
2. `crash_night_normal_000989`（val_real）样本内 000022.jpg == 000023.jpg——CCD 源视频静止帧。
- duplicate_sample_sequence=0（无整条 25 帧重复）；无泄漏。

### C5 — 元数据缺口
- camera_type / day_night / source_url 字段缺失；fog 无（源数据不含雾天）。
- 映射口径：day/night 按 weather=night→夜间、其余→白天；camera 按来源文档均为前视行车记录仪视角。

---

## D 级（可接受，不作验收失败理由）

- 类别天然不均衡：真实 snow 事故 205、night 事故 175、DADA 仅 25 条；reserve 真实正样本仅 1 条（crash_night_rainy_001100）→ v1.1 无法扩到 300 条（未来扩展约束，非 v1.0 验收失败条件）。

---

## 冻结声明

- v1.0 正式冻结（2026-10-05）；后续所有实验使用本冻结版本，不再直接修改 v1.0。
- 数据层零改动：样本 / 标签 / split / prediction_eligible / manifests\*.json 均未修改。
- 详细验收见 `acceptance_audit_final.md` 与 `reports/` 下各审计报告。
