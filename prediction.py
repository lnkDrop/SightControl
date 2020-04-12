#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File  : prediction.py

import torch

from commons import get_model, format_class_name, tensorfrom_img

model = get_model()


def get_prediction(image_bytes):
    tensor = tensorfrom_img(image_bytes)
    output = model(tensor)

    _, predicted = torch.max(output.data, 1)
    label = str(predicted.item())
    class_name = format_class_name(label)
    return class_name
