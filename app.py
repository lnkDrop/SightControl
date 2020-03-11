#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File  : app.py.py

from flask import Flask, render_template, json, request, jsonify, redirect, url_for
from datetime import timedelta

app = Flask(__name__, template_folder='view')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


@app.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        print("get")
        return render_template('home.html')
    elif request.method == 'POST':
        img = request.form.get('img')
        label = request.form.get('label')
        print("img:",img)
        print("label:",label)
        return render_template('home.html')

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