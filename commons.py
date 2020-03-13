#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File  : commons.py
import torch, base64
import io
from torchvision import transforms
from PIL import Image
from training import Network, get_classes


def get_model():
    the_model = Network()
    the_model.load_state_dict(torch.load('model/model.pt'))
    the_model.eval()
    return the_model


def tensorfrom_img(base64_data):
    data_transform = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
    ])

    image = Image.open(io.BytesIO(base64_data)).convert('RGB')
    return data_transform(image).unsqueeze(0)


def format_class_name(label):
    class_name = get_classes()
    class_name = class_name[eval(label)]
    x_pos = class_name.split('_')[0]
    y_pos = class_name.split('_')[1]
    return x_pos, y_pos
