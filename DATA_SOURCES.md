# 数据来源与许可说明

本项目整理了三个真实视频来源和用户用 CARLA 0.9.15 生成的合成片段。清单和图像中保留了来源标记。真实来源的图像不是本项目独立创作，使用者应分别遵守原始来源的条款。

| 来源 | 本数据集中的用途 | 原始项目 |
| --- | --- | --- |
| CCD (Car Crash Dataset) | 真实事故 | https://github.com/Cogito2012/CarCrashDataset |
| DADA-2000 | 真实事故 | https://github.com/JWFangit/LOTVS-DADA |
| BDD100K MOT | 真实无事故 | https://bdd-data.berkeley.edu/ |
| CARLA 0.9.15 | 合成事故与无事故 | https://carla.org/ |

BDD100K 数据与其代码采用不同条款。数据许可原文保存在 [BDD100K_DATA_LICENSE.rst](BDD100K_DATA_LICENSE.rst)，源自 [BDD100K 官方文档](https://github.com/bdd100k/bdd100k/blob/master/doc/source/license.rst)。其中要求在复制、修改和分发时保留版权与许可声明，并对用途设有限制。每个包含 BDD100K 帧的 Release ZIP 附件也附有该许可原文。

CCD 仓库中的 MIT `LICENSE` 描述软件，不应据此推断所有原始事故视频均采用 MIT 许可。DADA-2000 的图像条款亦应以原始发布方的说明为准。本项目不向所有来源图像授予统一的开源许可。

请在研究成果中分别引用原始数据集和 CARLA，并说明本项目做过抽帧、重排、标签融合与数据划分。用户已确认公开再分发本发布包中来源图像的授权范围。
