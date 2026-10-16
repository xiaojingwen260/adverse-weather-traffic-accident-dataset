# -*- coding: utf-8 -*-
"""append_freeze_records.py — v1.0 正式冻结记录追加（README / state.yaml / handoff，纯追加）

用户 8 项指令第 7 项：更新 README（冻结记录一节追加）、stages\\06\\handoff.md（追加）、
state.yaml（完成注记追加一行）。仅文档与状态记录，不修改数据内容。
"""
import io
import os

README = r'D:\dataset_final_export\dataset_final\README.md'
HANDOFF = r'D:\workbuddyworkplatform\workflows\crash-synthesis\stages\06_dataset_finalization\handoff.md'
STATE = r'D:\workbuddyworkplatform\workflows\crash-synthesis\state.yaml'

readme_add = '''
### v1.0 正式冻结（2026-10-05）

- 最终验收审计（18 节，独立复核，`reports/final_acceptance_audit.md`）原始判定 **C CONDITIONAL PASS**；
  经用户决策「方案 a：B1 文档化后直接冻结」→ **v1.0 正式冻结，可进入 baseline 训练**。
- **B1（已知限制，正式记录）**：CCD 事故样本 `collision_frame=null` 共 **1500 条**（486 条真实恶劣天气事故正样本 +
  1014 条 clear_accident 负样本）。
- **预测任务评估口径（正式规定）**：
  1. TTA / time-to-accident / collision lead time **仅在 collision_frame 有真实标注的事故正样本上计算**：
     CARLA 事故正 **1080**（cf=20）+ DADA **25**（cf 真值）＝ **1105** 条；其中 prediction_eligible=true **973** 条；
  2. **486 条 CCD 真实恶劣天气事故正样本（collision_frame=null）不参与 TTA 评价**，仍允许用于事故检测、
     分类及其他不依赖 collision_frame 的实验；
  3. 不允许对 CCD 的 collision_frame 做自动估算并当作真值使用；
  4. 不允许将 estimated collision frame 与人工真值混合报告。
- **B1 不阻碍检测/分类实验；预测任务中仅限制 TTA 评价样本范围。**
- 冻结产物：`freeze_v1.0/`（`version_v1.0.json`、`frozen_manifest_hashes.json`、`split_hashes.json`、
  `final_distribution_frozen.json`、`audit_references.json`、`known_limitations_v1.0.md`、`acceptance_audit_final.md`）。
- 数据层零改动：样本 / 标签 / split / prediction_eligible / `manifests\\*.json` 均未修改；后续实验使用本冻结版本，不再直接修改 v1.0。
'''

state_add = '''
# === 完成注记追加（2026-10-05）：v1.0 正式冻结（B1 文档化）===
# 用户选择方案 a：B1（CCD 事故样本 collision_frame=null 共 1500 条：486 真实恶劣天气事故正 + 1014 clear_accident 负）
# 文档化后直接冻结 v1.0。预测任务评估口径：TTA 仅在 collision_frame 有真实标注的事故正样本上计算
# （CARLA 事故正 1080 + DADA 25 = 1105，pe=true 973）；486 条 CCD 真实恶劣天气事故正样本不参与 TTA 评价，
# 仍可用于检测/分类；不对 CCD collision_frame 自动估算并当作真值。冻结产物见
# D:\\dataset_final_export\\dataset_final\\freeze_v1.0\\。数据层零改动；current 保持 07_training。
'''

handoff_add = '''
---

## 06 最终验收与正式冻结（追加记录，2026-10-05）

### 输入
- 冻结 v1.0 只读：`D:\\dataset_final_export\\dataset_final\\`（master 4971 / train 2700 / val_real 200 / test_real 340 / reserve 1731）。

### 最终验收审计（18 节，独立复核）
- 命令：`python scripts\\audit_labels.py`、`audit_cross.py`、`audit_trace.py`、`audit_integrity.py`、
  `audit_integrity_dup_locate.py`、`audit_near_dup.py`、`audit_near_dup_verify.py`、`spot_check_prep.py`（均交付包 `scripts\\` 内，幂等重跑）。
- 结果（全部实测，报告见 `reports\\`）：文件完整性 4971/124,275 JPG、0 缺失/0 解码失败/0 空/0 缺帧/0 孤儿/0 重复 ID；
  深度近重复：跨 split 比对 7,134,440 对，36 对严格疑似经逐帧复核全部排除，MD5 序列重复 0；
  泄漏：sample_id/group_id/original_video_id 六对 split 交集全 0；标签逻辑 A=0；清单交叉一致（split 集合差异 {}）；
  来源可追溯 4796/4971（CCD night 175 本地源 mp4 缺失，C 级）；目检 886 条（17.8%）天气差异约 31 条（3.5%，C 级）。
- 原始判定：**C CONDITIONAL PASS**（唯一 B 级 = B1：1500 条 CCD 事故样本 collision_frame=null）。

### 用户决策（2026-10-05 方案 a：文档化口径直接冻结）
- B1 正式记录为已知限制（`freeze_v1.0\\known_limitations_v1.0.md`）；486 条真实恶劣天气事故正样本不参与 TTA 评价，
  仍可用于检测/分类；1014 条 clear_accident 负样本字段同样为 null 但不影响用途。
- 预测任务评估口径写入 README 与冻结记录：TTA 仅在 cf 有真实标注的事故正样本上计算（CARLA 1080 + DADA 25 = 1105，
  pe=true 973）；不对 CCD cf 自动估算；不混合 estimated 与人工真值。
- 验收结论归档：**v1.0 正式冻结，可进入 baseline 训练**（`freeze_v1.0\\acceptance_audit_final.md` 定稿）。

### 冻结产物（`freeze_v1.0\\`）
version_v1.0.json / frozen_manifest_hashes.json / split_hashes.json / final_distribution_frozen.json /
audit_references.json / known_limitations_v1.0.md / acceptance_audit_final.md。

### 纪律
- 数据层零改动：样本/标签/split/prediction_eligible/manifests\\*.json 未修改；旧版数据（v1/v2/旧 CARLA/旧清单）只读；
  本阶段未启动训练/特征提取/领域自适应；current 保持 07_training。

### 下一个接手的 AI 应该做什么
- 读 `state.yaml`（current → 07_training）与 `stages\\07_training\\handoff.md`；
- 训练输入 `D:\\dataset_final_export\\dataset_final\\`（冻结 v1.0）；评估按天气/域分层；
  预测任务 TTA 仅对 collision_frame 有真值的样本（CARLA 1080 + DADA 25）计算；
- 训练前可参考 `freeze_v1.0\\known_limitations_v1.0.md`（C3 天气目检差异清单可定向复核）。
'''


def append(path, text):
    with io.open(path, 'r', encoding='utf-8') as f:
        old = f.read()
    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(old)
        f.write(text)
    print('appended ->', path, '(+%d chars)' % len(text))


def main():
    append(README, readme_add)
    append(STATE, state_add)
    append(HANDOFF, handoff_add)


if __name__ == '__main__':
    main()
