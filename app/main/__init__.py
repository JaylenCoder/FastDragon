# -*- coding: utf-8 -*-
# @Time    : 2022/1/22 12:54
# @Author  : HoxHou
# @File    : __init__.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
import os
import time
import arrow
import platform
from loguru import logger

__all__ = [
    'time', 'arrow', 'logger', 'platform', 'system', 'base_dir', 'now'
]

time = time  # time 时间模块
arrow = arrow  # arrow 时间模块
utc = arrow.utcnow()  # 世界时间
now = arrow.now()  # 本地时间
logger = logger  # 初始化日志
platform = platform  # 站点模块
system = platform.system()  # 系统信息
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))  # 项目根路径

if __name__ == '__main__':
    start_time = time.time()
    time.sleep(0.2)
    _time = time.time() - start_time
    print(_time)
