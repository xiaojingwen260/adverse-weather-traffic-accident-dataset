# dataset_final 数据集构建报告

构建时间：2026-10-04 18:20:24

## 1. 任务定义

主任务：恶劣天气交通事故识别与预测。
`target = accident AND adverse_weather`；`adverse_weather`：rainy/snowy/night=1，clear=0。
天气、事故、主任务标签分列保存（见 manifests/dataset_master.json）。

## 2. 输入与来源

- v2 交付包：`D:\dataset_v2_export\dataset_v2\dataset_planB_v2.json`（4431 条，只读）
- 新增合成 clear 事故：`D:\dataset\carla_clear_out_v2\`（540 条，晴天事故；流程说明见 3.1）
- v1 冻结数据与旧 CARLA 目录全程只读，未触碰。

## 3. 本阶段实际执行命令

### 3.1 服务器端 540 条 clear 事故生成

> **流程说明**：540 条 CARLA 晴天事故数据在明确确认流程完成前被提前生成，属于流程违规；数据完成后经用户复核决定保留。该事件已如实记录，不影响数据真实性与质量验收结论。

1. 修改 `carla_synth.py` → `carla_synth_clear.py`：新增 `make_weather("clear")` 分支（cloudiness 5~20、precipitation 0、fog 0~2、sun_altitude 35~60°）；`--weather` choices 增加 `clear`。
2. 新批次驱动 `batch_v2_clear.py`（复用负样本看门狗模式：30s 轮询、manifest 断点续跑、progress.json、CARLA 自动重启、随机 seed、max-fails=20）。
3. 上传至服务器 `/data/xiaojingwen/carla_clear_acc/`（独立目录，未覆盖 carla_batch/carla_neg/carla_out）。
4. 冒烟测试 1 条通过（碰撞第 26 帧原始帧 → 裁窗对齐输出第 20 帧；ffprobe 本地复核 25 帧/1280×720/5fps）。
5. 启动：`nohup conda run -n carla37 python3 batch_v2_clear.py --target 180 --out /data/xiaojingwen/carla_clear_acc > carla_clear.log 2>&1 &`（2026-10-04 10:45:42 启动，12:29:36 完成）。
6. 下载：服务器 `tar czf carla_clear.tar.gz clear manifest.json`（897,044,620 字节）→ scp → 本地 `tar -xzf` 到 `D:\dataset\carla_clear_out_v2\`。

### 3.2 本地验收与构建

- `scripts/verify_clear_v2.py`：540 条 mp4 验收 + 转帧（每条 25 张 JPG → `frames/CARLA_ACCIDENT/`）+ MAD 峰检测 → `reports/clear_download_acceptance.json`、`reports/clear_verify.json`
- `scripts/build_master.py`：统一主清单、group_id、划分、分布/防泄漏/标签检查 → `manifests/*.json`、`reports/final_distribution.{json,csv,md}`、`reports/split_leakage_check.json`、`reports/label_logic_check.json`
- `scripts/frame_integrity.py`：全量帧完整性 + 重复帧序列 → `reports/frame_integrity_check.json`
- `loaders/dataset_loader.py` + `scripts/test_loader_delivery.py`：加载器全量遍历 → `reports/loader_delivery_result.json`

## 4. 数据筛选规则

1. `test_real=340` 固定：v2 既定真实测试集（CCD 事故 200 + BDD 无事故 140），不重抽样、不调整。
2. `val_real=200`：100% 真实；恶劣天气事故正 100（DADA 25 固定 + CCD 75 按 night/snowy/rainy 分层）；恶劣天气无事故负 50（BDD，rainy 仅 9 条可用，保留真实分布）；正常天气事故负 50（CCD clear）。正:负=1:1。
3. `train=2700`：合成 2160（恶劣天气事故 1080 全部 + 恶劣天气无事故 540 + clear 事故 540 全部）；真实 540（恶劣天气事故 270 + 恶劣天气无事故 135 + 正常天气事故 135）；80%/20%±0.5%，正负各 50%，两类负样本各 50%。
4. 天气分层选择：真实正样本按 night/snowy/rainy 尽量均衡（池：night125/rainy66/snowy155 于 test/val 之外）；真实雪天充足、雨天偏紧（rainy 66 中 train 取 90 目标→不足则取全部并保留真实分布）。
5. 未选中有效数据 → reserve（1731）。

## 5. 最终数量

| 集合 | 数量 | 说明 |
|---|---|---|
| 总样本 | 4971 | 每条 25 帧/5fps/5 秒 |
| 总 JPG | 124275 | 约 17.52 GB（见 frame_integrity_check.json）|
| train | 2700 | 合成 80.000% / 真实 20.000% |
| val_real | 200 | 100% 真实 |
| test_real | 340 | 100% 真实，固定 |
| reserve | 1731 | 有效未选中数据 |

## 6. 正负样本分布（train）

| 类型 | 合成 | 真实 | 合计 |
|---|---|---|---|
| 恶劣天气事故（正） | 1080 | 270 | 1350 |
| 恶劣天气无事故（负） | 540 | 135 | 675 |
| 正常天气事故（负） | 540 | 135 | 675 |
| 合计 | 2160 | 540 | 2700 |

## 7. 验证集/测试集分布

- val_real：正 100（DADA 25：night15+rainy10；CCD 75：night/snowy/rainy 分层）/ 负 100（adverse_no_accident 50：BDD night/rainy/snowy；clear_accident 50：CCD clear）。
- test_real：CCD 事故 200（clear60/night50/rainy40/snowy50）+ BDD 无事故 140（night60/rainy40/snowy40）。
详见 `reports/final_distribution.md`。

## 8. 防泄漏

- `group_id`：CCD/DADA/BDD 按原始视频 ID；CARLA 按 Town+场景+天气+序号（每条为独立 episode）。
- group_id 实际重算（`scripts/group_stats.py`，读取 dataset_master.json，非手工赋值）：
  - 样本总数=4971，非空 group_id=4971，唯一 group_id=4971
  - 各 split 唯一 group_id：train=2700 / val_real=200 / test_real=340 / reserve=1731
  - 唯一 group_id == 样本总数 ⇒ 每条样本对应独立 episode；缺失 group_id 样本=0；重复 group_id 组=0
- 同原始视频的全部片段只进一个 split；`split_leakage_check.json`：
  - group_overlap=0
  - duplicate_sample_id=0
  - duplicate_frame_sequence=0
  - video_overlap_across_splits=0
  - path_errors=0

## 9. 质量控制与已知问题

- 早期 MAD 峰（碰撞第 18 帧前已明显）：v2 既有 107 条 + 新增 clear 43 条 → `quality_flag=["early_motion_peak"]`、`prediction_eligible=false`（保留用于检测，不直接用于预测）。
- DADA 原生 1584×660 保留，加载器统一 resize（保比例）。
- CARLA mp4 编码 mpeg4/mp4v 非 H.264（JPG 训练管线不受影响；如需转码留待后续阶段）。
- CCD 少量非 1280×720 帧（21 条 960×720、14 条 640×360，v2 已记录）由加载器 resize。
- 真实雪天/雨天样本相对有限：val 的 adverse_no_accident 负样本中 rainy 仅 9 条（BDD 池 rain 总量 49、test 已占 40），已保留真实分布并在分布报告中体现，未复制补齐。
- 合成 clear 事故与现有正样本/负样本为独立 episode（pos manifest 无 seed；neg seed 为运行级随机），无成对反事实跨 split；重复帧序列检查提供经验性兜底。

## 10. 验收结果汇总

| 验收项 | 结果 | 依据 |
|---|---|---|
| 主清单 JSON 合法、sample_id 唯一 | 0 重复 | label_logic_check.json / split_leakage_check.json |
| 所有相对路径可解析、每条 25 帧、JPG 可读 | ok=4971/4971，缺帧 0，坏解码 0 | frame_integrity_check.json |
| 训练集合成占比 80%±0.5% / 真实 20%±0.5% | 80.000% / 20.000% | final_distribution.json |
| 训练集正负各 50% | 1350 / 1350 | final_distribution.json |
| 两类负样本各 50% | 675 / 675 | final_distribution.json |
| 验证集 100% 真实且含三类样本 | 200 条（正 100/负 100） | final_distribution.json |
| TEST_REAL 340 保持不变 | 340 | manifests/test_real.json |
| group_id 跨 split 重叠 = 0 | 0 | split_leakage_check.json |
| group_id 实际统计（重算，非手工） | 唯一组=4971/样本=4971；重复组=0；缺失组=0 | split_leakage_check.json |
| 路径错误 = 0 | 0 | split_leakage_check.json |
| 重复帧序列 = 0 | 0 | split_leakage_check.json |
| 标签逻辑错误 = 0 | 0 | label_logic_check.json |
| 加载器全量遍历错误 = 0 | 4971/4971，errors=0 | loader_delivery_result.json |

## 11. 产物绝对路径

- 交付包根：`D:\dataset_final_export\dataset_final\`
- 帧：`frames\{CCD,DADA,BDD100K,CARLA_ACCIDENT,CARLA_NON_ACCIDENT}\`（4971 条）
- 清单：`manifests\{dataset_master,train,val_real,test_real,reserve}.json`
- 加载器：`loaders\dataset_loader.py`
- 报告：`reports\`（pre_split_inventory、synthetic_clear_accident_gap、clear_download_acceptance、final_distribution、split_leakage_check、frame_integrity_check、label_logic_check、loader_delivery_result、dataset_construction_report）
- 脚本：`scripts\`（verify_clear_v2、build_master、frame_integrity、test_loader_delivery、gen、count_splits_v2、audit_v2、gap_report_v2）

## 12. 阶段边界

本阶段仅构建/重组/验收数据，**未启动任何模型训练、特征提取或领域自适应实验**。
下一步（07_training）待工作台状态更新后另行启动。

## 13. 冻结记录（2026-10-04，来源级检查通过后）

本数据集于下列检查全部通过后正式冻结：

| 检查项 | 结果 | 依据 |
|---|---|---|
| 主清单 JSON 合法 / sample_id 唯一 | PASS（4971 条 / 4971 唯一） | dataset_master.json |
| 划分合计与结构 | PASS（2700+200+340+1731=4971；train 合成 80.000%/真实 20.000%；正负各 1350/1350；两类负样本各 675） | final_reverify.json |
| 标签逻辑 | PASS（0 错误） | label_logic_check.json |
| 完整性 | PASS（124275 JPG / 17.52GB，bad=0，重复帧序列=0） | frame_integrity_check.json |
| 加载器全量遍历 | PASS（4971/4971，errors=0） | loader_delivery_result.json |
| group_id 防泄漏（重算） | PASS（唯一组 4971 = 样本数；跨 split 交集 0） | split_leakage_check.json |
| 来源级防泄漏（冻结前追加） | PASS（逐原始视频跨 split 交集 = 0） | source_lineage_leakage_check.json |

**来源级检查结论**（`reports/source_lineage_leakage_check.json`）：
- 分组方法：真实数据按 source+original_video_id；CARLA 按逐原始视频（L1）/运行段 town+scenario+weather[+seed]（L2）/批次（L3）三级重建，不沿用 group_id，不编造 episode_id/base_scene_id 字段。
- 真实数据（CCD 1500 / DADA 25 / BDD100K 746）：唯一视频数 = 样本数，每条原始视频恰好产出 1 个 25 帧片段，不存在同视频切多片段；跨 split 交集 = 0。
- CARLA 逐原始视频（2700）：全部唯一，跨 split 交集 = 0。
- 来源级（逐原始视频）跨 split 交集 = 0 ⇒ **无同源场景泄漏**。
- 如实记录：负样本按运行级 seed 段分组有 49 段横跨 train/reserve（train 540/reserve 540 为 seed=42 确定性逐条挑选所致）；该运行段不等于同一基础场景（同 seed 批覆盖 5 个不同 town；seed 为运行级随机种子、非逐视频场景种子；同段内各条为独立 episode），故不构成同源泄漏，但已如实记录备查。
- 正/负/clear 为独立生成批次、无逐视频场景种子配对键，「同一基础场景在批次间复用」无法仅凭清单字段排除（可验证程度已写入检查报告）。
