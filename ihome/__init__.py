# -*- coding: utf-8 -*-

import redis

from flask import Flask
from config import config_dict  # 把配置文件里面的工程模式字典导入，进行匹配模式
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import api_1_0


# 构建数据库对象
db = SQLAlchemy()  # 本来是db = SQLAlchemy(app)  但是为了延时操作放在下面进行app初始化

# 构建redis连接对象
redis_store = None

# 为flask补充csrf防护机制
csrf = CSRFProtect()  # CSRFProtect(app)延时初始化


# 工厂模式 再manger里面传入要使用的模式  然后把配置里面导入的字典进行匹配  就得到使用什么模式进行配置
def create_app(config_name):
    """创建flask应用对象"""
    app = Flask(__name__)

    conf = config_dict[config_name]  # 字典里面保存的是config文件里面的两个工程模式对象的引用

    # 设置flask的配置信息
    app.config.from_object(conf)

    # 初始化数据库db
    db.init_app(app)

    # 初始化redis
    global  redis_store
    redis_store = redis.StrictRedis(host=conf.REDIS_HOST,port=conf.REDIS_PORT)

    # 初始化csrf app
    csrf.init_app(app)

    # 将flask里的session数据保存到redis中
    Session(app)

    # 注册蓝图
    import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1_0")

    return app