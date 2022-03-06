# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 17:14
# @Author  : HoxHou
# @File    : database.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
from typing import Any
import peewee
import peewee_async
from playhouse.shortcuts import model_to_dict
from peewee import Model
from pydantic.utils import GetterDict

from app.main import platform_system, environment
from app.main.settings.Development import DevConfig

"""

"""
env = "default" if platform_system == "Windows" else environment  # 环境配置
config = {
    "default": DevConfig,
    "dev": DevConfig
}[env]
db = peewee_async.MySQLDatabase(database=config.DB_NAME,
                                host=config.SERVER, port=int(config.PORT), user=config.USER, password=config.PASSWORD)
# Create async models manager:
mysql_async = peewee_async.Manager(db)
# Set the sync False:
db.set_allow_sync(False)


class CRUDMixin:
    model: Model = None
    _service = dict()
    objects = peewee_async.Manager(db)

    @classmethod
    def instance(cls):
        """Method  instance
        :return: cls
        """
        instance = cls._service.get(cls.__name__, None)
        if not instance:
            instance = cls.__new__(cls)
            cls._service.setdefault(cls.__name__, instance)
        return instance

    @staticmethod
    async def execute(sql):
        """执行sql"""
        try:
            return await peewee_async.execute(sql)
        except Exception as e:
            return None

    async def insert(self, **kwargs):
        """保存数据"""
        try:
            return await self.objects.create(self.model, **kwargs)
        except Exception as e:
            return None

    async def find_one(self, *args, **kwargs):
        """查找一条数据"""
        try:
            return await self.objects.get(self.model, *args, **kwargs)
        except self.model.DoesNotExist:
            return None
        except Exception as e:
            return None

    async def find(self, *args, **kwargs):
        """查询指定字段，查找多条数据"""
        if not args:
            raise Exception("fields is empty")

        sql = self.model.select(*[getattr(self.model, k) for k in args])
        for key, val in kwargs.items():
            sql = sql.where(getattr(self.model, key) == val)
        try:
            return await self.objects.execute(sql)
        except Exception as e:
            return []


def m2d(obj):
    """ peewee model 实现转dict 方法"""
    if type(obj) == peewee_async.AsyncQueryWrapper:
        return [model_to_dict(o, recurse=True) for o in obj]
    else:
        values = model_to_dict(obj, recurse=True)
        for key, val in values.items():
            if type(val) == bytes:
                values[key] = str(val, encoding="utf8")
        return values


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res

# from peewee import Model
# from loguru import logger
# from peewee_async import execute
# from databases import MysqlPool, RedisPool
#
#
# class BaseService:
#     model: Model = None
#     _service = dict()
#
#     @classmethod
#     def instance(cls):
#         """Method  instance
#         :return: cls
#         """
#         instance = cls._service.get(cls.__name__, None)
#         if not instance:
#             instance = cls.__new__(cls)
#             cls._service.setdefault(cls.__name__, instance)
#         return instance
#
#     @staticmethod
#     async def execute(sql):
#         """执行sql"""
#         try:
#             return await execute(sql)
#         except Exception as e:
#             logger.exception(str(e))
#             return None
#
#     async def insert(self, **kwargs):
#         """保存数据"""
#         try:
#             return await self.db.create(self.model, **kwargs)
#         except Exception as e:
#             logger.exception(str(e))
#             return None
#
#     async def update(self, data):
#         """更新一条数据"""
#         try:
#             return await self.db.update(data)
#         except self.model.DoesNotExist:
#             return None
#         except Exception as e:
#             logger.exception(str(e))
#             return None
#
#     async def find_one(self, *args, **kwargs):
#         """查找一条数据"""
#         try:
#             if not args:
#                 return await self.db.get(self.model, *args, **kwargs)
#             res = await self.find(*args, **kwargs)
#             if len(res) > 1:
#                 raise Exception("find multiple data")
#             elif len(res) == 1:
#                 return res[0]
#             return None
#         except self.model.DoesNotExist:
#             return None
#         except Exception as e:
#             logger.exception(str(e))
#             return None
#
#     async def find(self, *args, **kwargs):
#         """查询指定字段，查找多条数据"""
#         if not args:
#             raise Exception("fields is empty")
#
#         sql = self.model.select(*[getattr(self.model, k) for k in args])
#         for key, val in kwargs.items():
#             sql = sql.where(getattr(self.model, key) == val)
#         try:
#             return await self.db.execute(sql)
#         except Exception as e:
#             logger.exception(str(e))
#             return []
#
#     @property
#     def db(self):
#         return MysqlPool().get_manager
#
#     @property
#     def redis(self):
#         return RedisPool().get_conn()
