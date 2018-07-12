# -*- coding: utf-8 -*-
from flask_script import Manager  # 负责脚本控制使用manager来运行整个程序
from flask_migrate import MigrateCommand, Migrate  # 对app以及db数据库的迁移

from ihome import create_app, db  # 导入应用模块下的创建app和db对象的方法

# 创建flask的app
app = create_app("develop")  # 这里把要进行的模式接口 develop是开发模式 product是生产模式

# 创建管理工具对象 之后就可以使用manager进行整体的代码运行了
manager = Manager(app)
Migrate(app, db)  # 使用migrate进行整体的数据库以及app的控制
manager.add_command("db", MigrateCommand)  # 进行数据注册


if __name__ == '__main__':
    manager.run()