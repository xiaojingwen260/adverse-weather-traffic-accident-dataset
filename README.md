# 恶劣天气交通事故识别与预测数据集（dataset_final）

## GitHub 发布与下载

仓库保存清单、加载器、构建脚本和验收报告。124,275 张 JPG 帧约 17.6 GB，放在 [Releases](https://github.com/xiaojingwen260/adverse-weather-traffic-accident-dataset/releases) 的 `v1.0` 附件中，以 `frames-part-01.zip` 等分包提供。下载该版本的全部 `frames-part-*.zip`，在仓库根目录依次解压，最终目录应包含 `frames/`、`manifests/` 和 `loaders/`。附件的 SHA-256 与帧数量见 `release-assets.json`。

使用前请阅读 [数据来源和使用条款](DATA_SOURCES.md)，尤其是 BDD100K 的原始数据许可。本仓库中的真实图像来自原始数据集；文件由其原始权利人分别管理。此整合数据集没有统一覆盖所有来源图像的宽松开源许可。

```python
from loaders.dataset_loader import DatasetFinal
ds = DatasetFinal(".")
for frames, rec in ds.iter_split("train"):
    pass
```

依赖：Python 3、`numpy`、`opencv-python`。

统一真实—合成融合数据集，主任务为 **恶劣天气交通事故识别与预测**（非普通事故/无事故二分类）。

## 1. 任务与标签定义

- `weather`: rainy / snowy / night / clear
- `adverse_weather`: `1` iff weather ∈ {rainy, snowy, night}；clear → `0`
- `accident`: `1` = 发生交通事故，`0` = 无事故（标签独立保存，不因天气合并）
- `target`（主任务标签）: `1` iff `accident=1 AND adverse_weather=1`（恶劣天气事故）
- `negative_type`:
  - `adverse_no_accident`：恶劣天气无事故（`accident=0, adverse_weather=1, target=0`）
  - `clear_accident`：正常天气事故（`accident=1, adverse_weather=0, target=0`，困难负样本）
  - `null`：主任务正样本（`target=1`）
- 天气、事故、主任务标签**分列保存**，可区分模型在学习事故、天气还是两者组合。

## 2. 目录结构

```
dataset_final/
├── frames\
│   ├── CCD\              # 真实事故（CCD，含各天气）
│   ├── DADA\             # 真实事故（DADA，val 固定 25 条，原生 1584×660）
│   ├── BDD100K\          # 真实无事故（BDD100K MOT，恶劣天气）
│   ├── CARLA_ACCIDENT\   # 合成事故（1080 恶劣天气 + 540 正常天气）
│   └── CARLA_NON_ACCIDENT\  # 合成无事故（1080 恶劣天气）
├── manifests\
│   ├── dataset_master.json  # 统一主清单（4971 条，路径相对本包根目录）
│   ├── train.json
│   ├── val_real.json
│   ├── test_real.json
│   └── reserve.json
├── loaders\dataset_loader.py
├── reports\              # 全部验收与统计报告
├── scripts\              # 构建/验收/提取脚本
└── README.md
```

## 3. 数据规模（构建后实测）

| 分项 | 数量 |
|---|---|
| 总样本 | 4971（每条 25 帧，5fps，5 秒） |
| 总 JPG | 124,275（17.52 GB 实测，见 reports/frame_integrity_check.json） |
| 合成（CARLA） | 2160 恶劣天气事故 + 1080 恶劣天气无事故 + 540 正常天气事故 |
| 真实（CCD/DADA/BDD100K） | 2271 |
| 训练集 | 2700（合成 2160 / 真实 540 = 80% / 20% ±0.5%） |
| 验证集 val_real | 200（100% 真实，正负 1:1） |
| 测试集 test_real | 340（100% 真实，固定不重抽样） |
| reserve | 1731（未选中有效数据） |

训练集结构（正负各 50%，两类负样本各 50%）：

| 类型 | 合成 | 真实 | 合计 |
|---|---|---|---|
| 恶劣天气事故（正） | 1080 | 270 | 1350 |
| 恶劣天气无事故（负） | 540 | 135 | 675 |
| 正常天气事故（负） | 540 | 135 | 675 |
| 合计 | 2160 | 540 | 2700 |

## 4. 划分与防泄漏

- 固定真实测试集 `test_real=340`：CCD 事故 200 + BDD 无事故 140（继承 v2 既定测试集，**不重抽样、不调整比例**）
- `val_real`：100% 真实，三类样本齐备（恶劣天气事故正、恶劣天气无事故负、正常天气事故困难负），正负 ≈ 1:1
- `group_id` 按原始视频/独立 episode 唯一：
  - CCD / DADA / BDD100K：按原始视频 ID
  - CARLA：按 Town + 场景 + episode（每视频独立 episode；正/负为独立运行，无成对反事实跨 split）
- 同原始视频的所有片段只进一个 split；`group_overlap=0`、`duplicate_sample_id=0`、`duplicate_frame_sequence=0`
- 合成数据不进入 test_real / val_real

## 5. 样本规格与质量控制

- 25 帧 / 5fps / 5 秒 / 1280×720（DADA 原生 1584×660，加载器统一 resize，保比例）
- 恶劣天气事故正样本：碰撞帧位于第 18~22 帧（CARLA 统一对齐第 20 帧）
- 早期 MAD 峰样本（峰 < 18 帧）：`quality_flag=["early_motion_peak"]`，`prediction_eligible=false`（保留用于事故检测，不直接用于事故预测）
- 全部样本路径有效、25 帧齐全、JPG 可解码（见 `reports/frame_integrity_check.json`）

## 6. 使用

```python
import sys; sys.path.insert(0, 'loaders')
from dataset_loader import DatasetFinal
ds = DatasetFinal('.')
for split in ('train', 'val_real', 'test_real', 'reserve'):
    for frames, rec in ds.iter_split(split):
        # frames: 25 张 BGR ndarray；rec: 主清单条目
        pass
```

## 7. 验收结论

- 主清单 JSON 合法；sample_id 唯一；相对路径全部可解析（`loader_delivery_result.json`：4971/4971，0 错误）
- 训练集合成 80% / 真实 20%（±0.5%），正负各 50%，两类负样本各 50%
- 验证集/测试集 100% 真实；TEST_REAL=340 保持不变
- 标签逻辑 0 错误；防泄漏 group_overlap=0；重复帧序列=0（`label_logic_check.json` / `split_leakage_check.json`）

## 8. 数据来源与版本

- 真实：CCD（事故）、DADA（事故，val 固定）、BDD100K MOT（无事故）
- 合成：CARLA 0.9.15（`carla_synth.py` 系列，1280×720/25fps 物理 20Hz 抽帧）
- v1 冻结 `D:\dataset_v1_export\dataset_v1\`（只读）；v2 交付包 `D:\dataset_v2_export\dataset_v2\`（只读输入）；本包为新构建产物
- 本阶段未启动任何模型训练 / 特征提取 / 领域自适应实验

## 9. 冻结记录（2026-10-04）

本数据集于下列检查全部通过后正式冻结：

| 检查项 | 结果 | 依据文件 |
|---|---|---|
| 主清单 JSON 合法 / sample_id 唯一 | PASS（4971 条 / 4971 唯一） | dataset_master.json |
| 划分合计与结构 | PASS（2700+200+340+1731=4971；train 合成 80.000%/真实 20.000%；正负各 1350；两类负样本各 675） | final_reverify.json |
| 标签逻辑 | PASS（0 错误） | label_logic_check.json |
| 完整性（25 帧/解码/路径） | PASS（124,275 JPG / 17.52GB，bad=0，重复帧序列=0） | frame_integrity_check.json |
| 加载器全量遍历 | PASS（4971/4971，errors=0） | loader_delivery_result.json |
| group_id 防泄漏（重算） | PASS（唯一组 4971 = 样本数；跨 split 交集 0） | split_leakage_check.json |
| **来源级防泄漏（冻结前追加）** | PASS（见下） | source_lineage_leakage_check.json |

**来源级检查结论**（`reports/source_lineage_leakage_check.json`）：
- 分组方法：真实数据按 `source+original_video_id`；CARLA 按逐原始视频（L1）/运行段 `town+scenario+weather[+seed]`（L2）/批次（L3）三级重建，不沿用 group_id，不编造 episode_id/base_scene_id 字段。
- 真实数据（CCD 1500 / DADA 25 / BDD100K 746）：**唯一视频数 = 样本数**，即每条原始视频恰好产出 1 个 25 帧片段，不存在同视频切多片段；跨 split 交集 = 0。
- CARLA 逐原始视频（2700）：全部唯一，跨 split 交集 = 0。
- 来源级（逐原始视频）跨 split 交集 = **0** ⇒ **无同源场景泄漏**。
- 如实记录：负样本按运行级 seed 段（town+scenario+weather+seed）分组有 49 段横跨 train/reserve（train 540/reserve 540 为 seed=42 确定性逐条挑选所致）；该运行段**不等于同一基础场景**（同 seed 批覆盖 5 个不同 town；seed 为运行级随机种子、非逐视频场景种子；同段内各条为独立 episode），故不构成同源泄漏，但已如实记录备查。正/负/clear 为独立生成批次、无逐视频场景种子配对键，「同一基础场景在批次间复用」无法仅凭清单字段排除（可验证程度已写入检查报告）。

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
- 数据层零改动：样本 / 标签 / split / prediction_eligible / `manifests\*.json` 均未修改；后续实验使用本冻结版本，不再直接修改 v1.0。


