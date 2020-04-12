#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File  : app.py.py

from flask import Flask, render_template, json, request, jsonify, redirect, url_for
from datetime import timedelta
import base64, torch, cv2
import numpy as np
import os

app = Flask(__name__, template_folder='view')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
npList = []
count = 0


def get_img_data(img_data, label):
    # 引用全局变量count 用于给图片命名
    global count
    # 转换进制
    img_data = base64.b64decode(img_data.split(',', 1)[1])  # 裁剪下前端传来的img_data,只需要base64格式的字符就行
    np_arr = np.frombuffer(img_data, np.uint8)
    img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    label_path = 'static/imgData/%s' % (str(label))  # 位置坐标的存储位置(文件夹名)
    img_path = 'static/imgData/%s/%s.png' % (str(label), str(count))  # 图片的存储位置
    if not os.path.exists(label_path):
        os.mkdir(label_path)
    cv2.imwrite(img_path, img_np)
    count += 1
    return


@app.route('/')
def redirect():
    return redirect('home.html')


@app.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        # 训练
        # 收集前端发送过来的数据
        img = request.form.get('img')
        label = request.form.get('label')
        # 对数据进行处理并存储     flag：优化—存储到缓存
        get_img_data(img, label)
        return render_template('home.html')


@app.route('/learn', methods=['GET', 'POST'])
def learn():
    if request.method == 'GET':
        return render_template('learn.html')
    elif request.method == 'POST':
        # 预测
        from prediction import get_prediction  # 接口
        img = request.form.get('img')
        img_data = base64.b64decode(img.split(',', 1)[1])  # 裁剪下前端传来的base64字符格式
        pos = get_prediction(img_data)  # 获取class_name即坐标
        return jsonify({
            'x': pos[0],
            'y': pos[1]
        })


@app.route('/login', methods=['GET', 'POST'])  # 保留功能
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        if(username==str(123) and password==str(123)):
            return jsonify({
                'static': 0,
                'massage': '验证成功'
            })
        else:
            return jsonify({
                'static': 1,
                'massage': '验证失败'
            })


if __name__ == '__main__':
    app.run(debug=True,port=8000)
