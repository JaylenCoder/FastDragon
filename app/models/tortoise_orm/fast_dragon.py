# -*- coding: utf-8 -*-
# @Time    : 2022/2/12 15:27
# @Author  : HoxHou
# @File    : fast_dragon.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id = fields.IntField(pk=True)
    uid = fields.CharField(35, null=False, unique=True, description="UID:用户唯一标签")
    user_name = fields.CharField(255, null=False, unique=True, description="用户名")
    password = fields.CharField(255, null=False, description="密码 hashed password")
    phone = fields.CharField(20, null=True, description="手机号")
    email = fields.CharField(255, null=True, description="邮箱")
    avatar = fields.CharField(255, null=True, description="头像")
    real_name = fields.CharField(10, null=True, default="", description="真实姓名")
    login_ip = fields.CharField(50, null=False, description="登录IP")
    login_time = fields.DatetimeField(null=True, auto_now=True, description="登录时间")
    super_admin = fields.CharField(2, null=False, default="0", description="超级管理员(0：否，1：是) Super User")
    creator_id = fields.CharField(50, null=False, description="创建人ID")
    tag = fields.CharField(10, null=True, description="标签")
    remark = fields.CharField(512, null=True, description="备注")
    created_time = fields.DatetimeField(null=True, auto_now_add=True, description="创建时间")
    modified_time = fields.DatetimeField(null=True, auto_now=True, description="修改时间")
    status = fields.CharField(3, null=False, default="1", description="状态(0：禁用，1：启用)")
    deleted = fields.IntField(null=False, default="0", description="是否删除(0：未删除，1：已删除")
    dept_id = fields.IntField(null=True, description="部门id")

    class Meta:  # 添加索引和表注释
        app = "fast_dragon"
        table = "user"
        table_description = "用户表"
        ordering = ["id"]

    class PydanticMeta:
        exclude = ["created_time", "modified_time", "id"]

    class Fields:
        template = {

        }

    def __str__(self):
        return self.user_name


"""
Model实例化
"""
UsersSchemaModel = pydantic_model_creator(User, name="Users")
