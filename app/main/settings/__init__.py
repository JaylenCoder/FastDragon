# -*- coding: utf-8 -*-
# @Time    : 2022/1/22 14:00
# @File    : __init__.py
"""
Service settings for project.
1.全局配置 Config
2.响应体枚举 MsgData
"""
import os
from pathlib import Path
from pydantic import BaseSettings
from app.main import system
from typing import NamedTuple
from enum import EnumMeta, Enum, unique
from types import DynamicClassAttribute


class Config(BaseSettings):
    app_name: str = "Web Service API"
    admin_email: str = ""
    items_per_user: int = 50
    """Quick-start development settings - unsuitable for production."""
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'e$od9f28jce8q47u3wis^$(e%$@lff6r89ux+=f!e1a$e42+#7'

    """SECURITY WARNING: don't run with debug turned on in production!"""
    DEBUG = False
    # Token Settings, 30天过期
    INVALID_TIME = 60 * 60 * 24 * 3650

    """Internationalization 国际化"""
    LANGUAGE_CODE = 'zh-Hans'
    TIME_ZONE = 'Asia/Shanghai'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = False

    """ 日志配置 """
    # 每条日志输出格式
    INFO_FORMAT = '{time:YYYY-MM-DD HH:mm:ss} [{level}] - {file}|{function}:{line} >>> {message}'
    ERROR_FORMAT = '{time:YYYY-MM-DD HH:mm:ss} [{level}] {process} {file}|{name}.{function}:{line} >>> {message}'
    DEBUG_FORMAT = '{time:YYYY-MM-DD HH:mm:ss} [{level}] {process} {file}|{name}.{function}:{line} >>> {message}'
    WIN_LOGS = os.path.join(Path().resolve(), "logs")
    LINUX_LOGS = f'/home/www/logs'
    LOG_FILE = WIN_LOGS if system == "Windows" else LINUX_LOGS
    LOG_PATH = os.path.join(LOG_FILE, '{time:%Y-%m-%d}.log')
    LOG_ERROR_PATH = os.path.join(LOG_FILE, '{time:%Y-%m-%d}-error.log')
    # 日志打包
    ROTATION = '00:00'  # rotation='500 MB' 日志超出500M自动分割日志文件（{time}.log/rotation='00:00' 定时自动生成）
    RETENTION = '7 days'  # 设置日志保留时长
    COMPRESSION = 'zip'  # 设置日志压缩格式


config = Config()  # 全局配置实例


class MsgData(NamedTuple):
    """ System response body. """
    code: int = 000000  # 业务码
    message: str = "请求成功"  # 响应信息

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MsgData):
            raise NotImplemented
        return self.code == other.code


class _ECEnumMeta(EnumMeta):
    """错误码枚举元类"""

    def __new__(mcs, *args, **kwargs):
        enum_class = super(_ECEnumMeta, mcs).__new__(mcs, *args, **kwargs)
        return unique(enum_class)  # 唯一


class BaseMsgEnum(Enum, metaclass=_ECEnumMeta):
    """错误码基类"""

    @DynamicClassAttribute
    def code(self) -> int:
        """业务码"""
        return self.value.code

    @DynamicClassAttribute
    def message(self):
        """业务信息"""
        return self.value.message

    @DynamicClassAttribute
    def error(self):
        """error码"""
        return self.name


class MsgEnum(BaseMsgEnum):
    """ 业务码枚举类 """
    SUCCESS = MsgData(200000, "请求成功")
    ServerError = MsgData(500000, "服务异常，请稍后重试")
