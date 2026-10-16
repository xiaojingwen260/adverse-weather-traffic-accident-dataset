# -*- coding: utf-8 -*-
"""dataset_loader.py — dataset_final 统一数据加载器

用法（以交付包根目录为基准，路径可整体移动）：
    from dataset_loader import DatasetFinal
    ds = DatasetFinal(root=r'D:\\dataset_final_export\\dataset_final')
    for split in ('train', 'val_real', 'test_real', 'reserve'):
        for frames, rec in ds.iter_split(split):
            # frames: list[np.ndarray] 长度 25，通道 BGR
            # rec: 主清单条目 dict
    # 尺寸统一：DADA 原生 1584x660 -> resize 到 1280x720（保比例不变形，cv2.INTER_AREA）
"""
import json
import os
import cv2
import numpy as np

OUT_W, OUT_H = 1280, 720


class DatasetFinal:
    def __init__(self, root, master_name='dataset_master.json'):
        self.root = root
        self.manifests_dir = os.path.join(root, 'manifests')
        self.master = json.load(open(os.path.join(self.manifests_dir, master_name),
                                     encoding='utf-8'))
        self.by_split = {}
        for sp in ('train', 'val_real', 'test_real', 'reserve'):
            p = os.path.join(self.manifests_dir, sp + '.json')
            if os.path.exists(p):
                self.by_split[sp] = json.load(open(p, encoding='utf-8'))

    @property
    def splits(self):
        return list(self.by_split)

    def resolve(self, item):
        # The frozen manifests use Windows separators; accept them on Linux too.
        return os.path.join(self.root, *item['frame_dir'].replace('\\', '/').split('/'))

    def load_sample(self, item):
        """读取 25 帧，DADA 等非 1280x720 统一 resize。返回 (frames, item) 或 (None, item)"""
        d = self.resolve(item)
        frames = []
        for k in range(1, item['frame_count'] + 1):
            p = os.path.join(d, '%06d.jpg' % k)
            im = cv2.imread(p, cv2.IMREAD_COLOR)
            if im is None:
                return None, item
            if im.shape[1] != OUT_W or im.shape[0] != OUT_H:
                im = cv2.resize(im, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)
            frames.append(im)
        return frames, item

    def iter_split(self, split):
        for item in self.by_split.get(split, []):
            frames, rec = self.load_sample(item)
            if frames is None:
                raise RuntimeError('不可读: ' + item['sample_id'])
            yield frames, rec

    def summary(self):
        return {sp: len(v) for sp, v in self.by_split.items()}


if __name__ == '__main__':
    ds = DatasetFinal(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print('splits:', ds.summary())
    for sp in ds.splits:
        n = 0
        for frames, rec in ds.iter_split(sp):
            n += 1
        print(sp, n)
