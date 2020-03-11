#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File  : training.py
import torch
from torch.utils.data.dataset import Dataset
from torch.utils.data.dataloader import DataLoader
from skimage import io, transform
from torchvision import transforms
import os
import cv2
import numpy as np


class eyesDataset(Dataset):
    def __init__(self, root, transform=None):
        self.root_dir = root
        self.transform = transform
        self.image_files = np.array([x.path for x in os.scandir(root) if x.name.endswith(".png")])

    def __getitem__(self, index):
        img_index = self.image_files[index]
        # 不进行图像增强，直接返回tensor
        img = cv2.imread(img_index)
        img_path = os.path.join(self.root_dir, img_index)
        # static / imgData
        label = img_path.split('/')[-1].split('_')[1].split('.png')[0]
        sample = {'image': img, 'label': label}
        if self.transform:
            sample = self.transform(sample)
        return sample

    def __len__(self):
        return len(self.image_files)


class ToTensor(object):

    def __call__(self, sample):
        image = sample['image']
        image_new = np.transpose(image, (2, 0, 1))
        return {'image': torch.from_numpy(image_new),
                'label': sample['label']}


# # 变换Resize
class Resize(object):

    def __init__(self, output_size: tuple):
        self.output_size = output_size

    def __call__(self, sample):
        # 图像
        image = sample['image']
        # 使用skitimage.transform对图像进行缩放
        image_new = transform.resize(image, self.output_size)
        return {'image': image_new, 'label': sample['label']}


# 利用之前创建好的eyesDataset类去创建数据对象
eye_train_set = eyesDataset("static/imgData/",
                            transform=transforms.Compose(
                                [Resize((60, 60)),
                                 ToTensor()]
                            ))
# 利用dataloader读取数据对象，并设定batch-size和工作现场,多线程读取
eye_train_loader = DataLoader(eye_train_set, batch_size=4, num_workers=4, shuffle=True)

# 字典数据的tensor变换


sample = next(iter(eye_train_set))

print(sample['image'].shape,sample['label'])
