# -*- coding: utf-8 -*-
# @Time    : 2022/02/12 21:01:19
# @File    : system_schema.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
from pydantic.main import BaseModel


class PersonalAccount(BaseModel):
    user_name: str
