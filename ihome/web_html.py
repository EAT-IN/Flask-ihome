# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, make_response
from flask_wtf.csrf import generate_csrf


html = Blueprint("html", __name__)

# 提供静态的html文件，不需要进行复杂的路径去除掉之前的static/html/直接返回页面






@html.route("/<re(r'.*'):file_name>")
def get_html_file(file_name):
    """提供html文件"""
    # 根据用户访问的路径知名的html文件名file-name，提供相应的页面文件
    if not file_name:
        # 表示用户访问的跟路径/
        file_name = "index.html"

    if file_name != "favicon.ico":
        file_name = "html/" + file_name

        # 使用wtf帮我们升恒csrf——token信息
        csrf_token = generate_csrf()

        # 为用户设置cookie csrf_token
        resp = make_response(current_app.send_static_file(file_name))
        resp.set_cookie("csrf_token", csrf_token)

        return resp