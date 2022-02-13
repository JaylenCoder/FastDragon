# -*- coding: utf-8 -*-
# @Time    : 2022/1/22 22:52
# @Author  : HoxHou
# @File    : response.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
from __future__ import annotations
from typing import Optional, Any
from app.main.settings import MsgEnum

__all__ = (
    "Msg",
)


class Msg(object):
    """
    Returns a instance depending on the  variable.
    :return:
    """

    def __init__(self, enum: Optional[MsgEnum] = None, msg="", **kwargs):
        if kwargs:
            enum_code = kwargs.get("code", MsgEnum.ServerError.code)
            enum_message = kwargs.get("message", MsgEnum.ServerError.message)
        else:
            enum = MsgEnum.ServerError if enum is None else enum
            enum_code, enum_message = enum.code, str(enum.message)
        code: int = enum_code  # 错误码
        message: str = enum_message.format(msg) if msg else enum_message  # 错误信息
        self.content: dict[str, Any] = dict(code=code, message=message)  # 内容

    def __built_in(self, data=None, ext_fields=None):
        """ 内建方法 """
        if ext_fields:
            self.content.update(ext_fields)
        if data:
            self.content.update(data)
        return self.content

    def add_fields(self, **kwargs):
        """ 新增字段 """
        self.__built_in(ext_fields=kwargs)

    def body(self, **kwargs):
        """ """
        _built_data = self.__built_in(kwargs)
        return _built_data


if __name__ == '__main__':
    print(Msg(MsgEnum.SUCCESS).body(data=[]))
