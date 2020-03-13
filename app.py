#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File  : app.py.py

from flask import Flask, render_template, json, request, jsonify, redirect, url_for
from datetime import timedelta
import base64, torch, cv2
import numpy as np
import os

# import training

app = Flask(__name__, template_folder='view')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
npList = []
count = 0


def getImgData(imgData, label):
    # 引用全局变量count
    global count
    # 转换进制
    imgData = base64.b64decode(imgData.split(',', 1)[1])  # 裁剪下前端传来的base64字符格式
    nparr = np.frombuffer(imgData, np.uint8)
    # torchnp = torch.from_numpy(nparry)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    label_path = 'static/imgData/%s' % (str(label))
    img_path = 'static/imgData/%s/%s.png' % (str(label), str(count))
    if not os.path.exists(label_path):
        os.mkdir(label_path)
    cv2.imwrite(img_path, img_np)
    count += 1
    return


@app.route('/')
def redict():
    return redirect('home')


@app.route('/home', methods=['GET', 'POST'])
def index():
    i = 0
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        # 收集训练数据
        img = request.form.get('img')
        label = request.form.get('label')
        getImgData(img, label)

        return render_template('home.html')


@app.route('/learn', methods=['GET', 'POST'])
def learn():
    i = 0
    if request.method == 'GET':
        print("get")
        return render_template('learn.html')
    elif request.method == 'POST':
        from interface import get_prediction
        # 预测
        img = request.form.get('img')
        imgData = base64.b64decode(img.split(',', 1)[1])  # 裁剪下前端传来的base64字符格式
        pos = get_prediction(imgData)
        return jsonify({
            'x': pos[0],
            'y': pos[1]
        })


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        return jsonify({
            'static': 0,
            'massage': '111'
        })
    else:
        return jsonify({
            'static': 1,
            'massage': '222'
        })


@app.route("/upload_row/", endpoint="upload_row", methods=["GET", "POST"])
def upload_row():
    # 文件对象保存在request.files上，并且通过前端的input标签的name属性来获取
    fp = request.files.get("f1")
    # 保存文件到服务器本地
    fp.save("a.jpg")
    return redirect(url_for("login.index"))


if __name__ == '__main__':
    app.run(debug=True)
