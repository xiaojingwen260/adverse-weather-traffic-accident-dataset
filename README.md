# 恶劣天气交通事故识别与预测数据集

这是冻结的 `v1.0` 实验数据包，共 4,971 条样本、124,275 张 JPG 图像帧。每条样本包含 25 帧。仓库提供实验所需的划分清单、加载器和说明；全部图像帧在 [v1.0 Release](https://github.com/xiaojingwen260/adverse-weather-traffic-accident-dataset/releases/tag/v1.0) 中分卷下载。

## 下载与目录

下载 Release 中**所有** `frames-part-*.zip`，逐一解压到本仓库根目录。各分卷路径互不重复，解压后目录应如下：

```text
frames/
manifests/
loaders/
README.md
DATA_SOURCES.md
BDD100K_DATA_LICENSE.rst
release-assets.json
requirements.txt
```

`release-assets.json` 列出每个 ZIP 的字节数、SHA-256 和帧数，下载后请据此校验。图像文件不在 Git 仓库中；只克隆仓库无法读取帧。

## 实验划分

| 划分 | 样本数 | 用途 |
| --- | ---: | --- |
| `train` | 2,700 | 训练；合成 80%，真实 20% |
| `val_real` | 200 | 真实数据验证 |
| `test_real` | 340 | 固定真实测试集 |
| `reserve` | 1,731 | 备用样本，不应混入上述固定划分 |

`manifests/dataset_master.json` 是完整主清单，各划分另有同名 JSON 文件。清单中的 `frame_dir` 相对于数据包根目录；每条记录包含来源、天气、事故、主任务标签和其他实验字段。

## 标签与评估

- `accident=1` 表示交通事故，`adverse_weather=1` 表示雨、雪或夜间。
- 主任务 `target=1` 当且仅当 `accident=1` 且 `adverse_weather=1`。`clear_accident` 是正常天气事故困难负样本；`adverse_no_accident` 是恶劣天气无事故负样本。
- 事故预测的 TTA / 碰撞提前量只在有真实 `collision_frame` 标注且满足相应筛选条件的样本上评估。CCD 的 1,500 条事故样本 `collision_frame=null`，不可把自动估计值当作真值；这些样本仍可用于不依赖碰撞时刻的实验。
- 使用固定划分进行报告，避免将 `reserve` 样本混入测试集。详细字段和筛选标志以清单记录为准。

## 加载

安装 Python 依赖：

```bash
python -m pip install -r requirements.txt
```

将 Release 图像分卷解压到仓库根目录后：

```python
from loaders.dataset_loader import DatasetFinal

ds = DatasetFinal(".")
print(ds.summary())
for frames, record in ds.iter_split("train"):
    # frames: 25 张 BGR 图像；record: 对应清单记录
    pass
```

加载器会统一调整图像大小；DADA 原始帧尺寸与其他来源不同。请阅读 [数据来源与许可说明](DATA_SOURCES.md) 及 [BDD100K 数据许可](BDD100K_DATA_LICENSE.rst)，并在论文中引用原始来源。本整合包不向所有来源图像授予统一的开源许可。
