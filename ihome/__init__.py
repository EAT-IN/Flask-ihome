# -*- coding: utf-8 -*-

import redis
import logging

from flask import Flask
from config import config_dict  # 把配置文件里面的工程模式字典导入，进行匹配模式
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from logging.handlers import RotatingFileHandler
from utils.commons import RegexConverter


# 构建数据库对象
db = SQLAlchemy()  # 本来是db = SQLAlchemy(app)  但是为了延时操作放在下面进行app初始化

# 构建redis连接对象
redis_store = None

# 为flask补充csrf防护机制
csrf = CSRFProtect()  # CSRFProtect(app)延时初始化

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日记录器
logging.getLogger().addHandler(file_log_handler)


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

    # 向app中添加自定义的路由转换器
    app.url_map.converters["re"] = RegexConverter

    # 注册蓝图
    import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1_0")

    # 提供html静态文件的蓝图
    import web_html
    app.register_blueprint(web_html.html)

    return app