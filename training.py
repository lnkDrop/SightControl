#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File  : training.py
import torch
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data.dataloader import DataLoader
from torchvision import transforms, datasets
import os
from Network import Network
from torchvision.datasets import ImageFolder
import sys


# 重写ImageFolder，拿到label的原始数据和tensor键值对
class myImageFolder(ImageFolder):
    def _find_classes(self, dir):
        """
        Finds the class folders in a dataset.

        Args:
            dir (string): Root directory path.

        Returns:
            tuple: (classes, class_to_idx) where classes are relative to (dir), and class_to_idx is a dictionary.

        Ensures:
            No class is a subdirectory of another.
        """
        if sys.version_info >= (3, 5):
            # Faster and available in Python 3.5 and above
            classes = [d.name for d in os.scandir(dir) if d.is_dir()]
        else:
            classes = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]
        classes.sort()
        class_to_idx = {classes[i]: i for i in range(len(classes))}

        return classes, class_to_idx


data_transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
])

train_dataset = myImageFolder(root='static/imgData/', transform=data_transform)
test_dataset = myImageFolder(root='static/imgData/', transform=data_transform)


def get_classes():
    classes = train_dataset.classes
    return classes


train_dataloader = DataLoader(dataset=train_dataset,
                              # batch_size=6,
                              shuffle=True,
                              )
test_dataloader = DataLoader(dataset=test_dataset,
                             # batch_size=6,
                             shuffle=True,
                             )

sample = next(iter(train_dataset))
image, label = sample
# print(image.shape)
batch = next(iter(train_dataloader))
images, lables = batch

# print(lables)


network = Network()


# print(network)


def get_num_correct(preds, labels):
    return preds.argmax(dim=1).eq(labels).sum().item()


optimizer = optim.Adam(network.parameters(), lr=0.0005)


def training(epoch):
    i = 0
    for epoch in range(epoch):
        network.train()
        total_loss = 0
        total_correct = 0
        i += 1
        for batch in train_dataloader:  # Get Batch
            images, labels = batch
            preds = network(images)  # Pass Batch
            loss = F.cross_entropy(preds, labels)  # Calculate Loss

            optimizer.zero_grad()
            loss.backward()  # Calculate Gradients
            optimizer.step()  # Update Weights

            total_loss += loss.item()
            total_correct += get_num_correct(preds, lables)
            # if (i % 10 == 0):
            #     correct = 0.0
            #     total = 0.0
            #     network.eval()
            #     with torch.no_grad():
            #         for test_data in test_dataloader:
            #             test_images, test_lables = test_data
            #             test_outouts = network(test_images)
            #             test_loss = F.cross_entropy(preds, labels)
        print(
            "epoch", epoch,
            "total_correct:", total_correct,
            "loss:", total_loss
        )
    torch.save(network.state_dict(), 'model/model.pt')
    return total_correct / len(train_dataset)


# training(150)
#
# # preds = network(images)
#
#
# @torch.no_grad()
# def get_all_preds(model, loader):
#     all_preds = torch.tensor([])
#     for batch in loader:
#         images, labels = batch
#
#         preds = model(images)
#         all_preds = torch.cat(
#             (all_preds, preds)
#             , dim=0
#         )
#     return all_preds


#
#
# torch.save(network, 'model/model.pt')
# model = torch.load('model/model.pt')
# model.eval()

the_model = Network()
the_model.load_state_dict(torch.load('model/model.pt'))
correct = 0.0
total = 0.0
with torch.no_grad():
    for data in test_dataloader:
        images, lables = data
        outputs = the_model(images)
        _, predicted = torch.max(outputs.data, 1)
        correct += (predicted == lables).sum()
        total += lables.size(0)
print('准确率:', float(correct) / total)
#
# sample = next(iter(train_dataset))
# image, label = sample
# print(the_model.forward(images))
