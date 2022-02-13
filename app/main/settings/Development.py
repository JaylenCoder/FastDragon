# -*- coding: utf-8 -*-
# @Time    : 2022/1/22 14:02
# @Author  : HoxHou
# @File    : Development.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
from app.main.settings import Config


class DevConfig(Config):
    DEBUG = True

    # 数据库配置 MySQL
    DB_NAME = "fast_dragon"
    SERVER = "127.0.0.1"
    PORT = "3306"
    USER = "root"
    PASSWORD = "123456"
    DEV_DATABASE = f"mysql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB_NAME}?charset=utf8"
    # Tortoise ORM 配置
    MODELS = [
        "app.models.tortoise_orm.fast_dragon",
        "aerich.models"
    ]
    TIME_ZONE = Config().TIME_ZONE
    TORTOISE_ORM = {
        "timezone": TIME_ZONE,
        "connections": {
            # first;second;third...
            "default": {
                "engine": "tortoise.backends.mysql",
                "credentials": {
                    "host": SERVER,
                    "port": PORT,
                    "user": USER,
                    "password": PASSWORD,
                    "database": DB_NAME,
                    "minsize": 1,
                    "maxsize": 5,
                    "charset": "utf8mb4"
                }
            }
        },
        "apps": {
            DB_NAME: {
                "models": MODELS,
                "default_connection": "default"
            },

        }
    }


DevConfig = DevConfig()

if __name__ == '__main__':
    print(DevConfig.TORTOISE_ORM)
