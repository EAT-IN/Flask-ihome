# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, make_response  # 导入蓝图，全局应用，响应
from flask_wtf.csrf import generate_csrf  # 导入csrf防护机制


html = Blueprint("html", __name__)

# 提供静态的html文件，不需要进行复杂的路径去除掉之前的static/html/直接返回页面
# 上面就决定了这个页面的蓝图的名字叫html，接下来所有的页面的装饰器都要用html开头





@html.route("/<re(r'.*'):file_name>")
def get_html_file(file_name):
    """提供html文件"""
    # 根据用户访问的路径知名的html文件名file-name，提供相应的页面文件
    if not file_name:
        # 表示用户访问的是根路径‘/’
        file_name = "index.html"

    if file_name != "favicon.ico":
        file_name = "html/" + file_name

        # 使用wtf帮我们升恒csrf——token信息
        csrf_token = generate_csrf()

        # 为用户设置cookie csrf_token
        resp = make_response(current_app.send_static_file(file_name))
        resp.set_cookie("csrf_token", csrf_token)

        return resp