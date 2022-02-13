# -*- coding: utf-8 -*-
# @Author  : HoxHou
# @File    : run.py
# @Software: PyCharm
import uvicorn
from app.main import system
from app.main.factory import Application

""" FastAPI Web服务启动

命令启动：uvicorn run:app --reload --host=localhost --port=8002
1.http://localhost:8001/
2.http://localhost:8001/docs
3.http://localhost:8001/redocs

"""
environment = ["dev", "pro", "remote"][0]  # 环境配置：dev-开发环境/pro-线上环境/remote-远程配置
app = Application(environment).init()  # 初始化应用


def management():
    """运行管理器 Run Management Utility."""
    if system != 'Windows':  # 本地开发环境
        import asyncio
        loop = asyncio.get_event_loop()
        config = uvicorn.Config(app=app, host='0.0.0.0', port=8082, reload=True, debug=True, workers=10, loop=loop,
                                lifespan='on', timeout_keep_alive=10)
        server = uvicorn.Server(config)
        loop.run_until_complete(server.serve())
    else:
        uvicorn.run('run:app', host='0.0.0.0', port=8080, reload=True, debug=True, workers=1)


if __name__ == '__main__':
    management()