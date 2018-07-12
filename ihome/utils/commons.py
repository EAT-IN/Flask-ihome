# -*- coding: utf-8 -*-

from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    """自定义正则表达式路由转换器"""
    def __init__(self, url_map, regex):
        """regx是再路由中填写的正则表达式"""
        super(RegexConverter, self).__init__(url_map)
        self.regex = regex