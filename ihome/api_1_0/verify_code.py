# -*- coding: utf-8 -*-

from . import api
from ihome.utils.captcha.captcha import captcha
from flask import current_app,jsonify, make_response
from ihome import redis_store, constants
from ihome.utils.response_code import RET


@api.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
    """提供图片验证"""
    # 获取参数
    # 名字，验证码真实值，图片的二进制内容
    name, text, image_data = captcha.generate_captcha()
    # 保存验证码的真实值与编号
    try:
        # redis_store.set("image_code_%s"% image_code_id, text)
        # redis_store.expires("image_code_%s"% image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES)
        redis_store.setex("image_code_%s"% image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 在日志中记录异常
        current_app.logger.error(e)
        resp = {
            "error":RET.DBERR,
            "errmsg":"保存验证码失败"
        }
        return jsonify(resp)

    # 返回验证码图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp

    # 还要返回一个相应头，声明一下图片的格式