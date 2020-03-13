# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
# # @File  : datasetTest.py
#
# import torch
# from torch.utils.data import DataLoader
# from torchvision import transforms, datasets
# import matplotlib.pyplot as plt
# import numpy as np
import torch.nn as nn
import torch.nn.functional as F


# # https://pytorch.org/tutorials/beginner/data_loading_tutorial.html
#
# # data_transform = transforms.Compose([
# #     transforms.RandomResizedCrop(224),
# #     transforms.RandomHorizontalFlip(),
# #     transforms.ToTensor(),
# #     transforms.Normalize(mean=[0.485, 0.456, 0.406],
# #                          std=[0.229, 0.224, 0.225])
# # ])
#
# data_transform = transforms.Compose([
#     transforms.Resize((36, 36)),
#     transforms.RandomHorizontalFlip(),
#     transforms.ToTensor(),
#
# ])
#
# train_dataset = datasets.ImageFolder(root='static/imgData/', transform=data_transform)
# train_dataloader = DataLoader(dataset=train_dataset,
#                               batch_size=4,
#                               shuffle=True,
#                               )
#
# sample = next(iter(train_dataset))
# image, label = sample
#
#
# # print(sample)
#
#
# def get_num_correct(preds, labels):
#     return preds.argmax(dim=1).eq(labels).sum().item()
#
#
# batch = next(iter(train_dataloader))
# images, labels = batch
# print(labels)
class Network(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5)
        self.conv2 = nn.Conv2d(in_channels=6, out_channels=12, kernel_size=5)

        self.fc1 = nn.Linear(in_features=12 * 4 * 4, out_features=120)
        self.fc2 = nn.Linear(in_features=120, out_features=60)
        self.out = nn.Linear(in_features=60, out_features=10)

    def forward(self, t):
        # (1) input layer
        t = t

        # (2) hidden conv layer
        t = self.conv1(t)
        t = F.relu(t)
        t = F.max_pool2d(t, kernel_size=2, stride=2)

        # (3) hidden conv layer
        t = self.conv2(t)
        t = F.relu(t)
        t = F.max_pool2d(t, kernel_size=2, stride=2)

        # (4) hidden linear layer
        t = t.reshape(-1, 12 * 4 * 4)
        t = self.fc1(t)
        t = F.relu(t)

        # (5) hidden linear layer
        t = self.fc2(t)
        t = F.relu(t)

        # (6) output layer
        t = self.out(t)
        # t = F.softmax(t, dim=1)

        return t


network = Network()
print(network)