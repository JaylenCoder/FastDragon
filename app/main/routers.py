# -*- coding: utf-8 -*-
# @Time    : 2022/2/13 11:56
# @Author  : HoxHou
# @File    : routers.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
"""
Framework API routers registration list.
接口路由注册表
"""
from app.core.system import system_view

namespaces = [
    {"router": system_view.router, "prefix": "", "tags": ['主页']},
]
