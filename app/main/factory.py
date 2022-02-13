# -*- coding: utf-8 -*-
# @Time    : 2022/1/22 12:54
# @Author  : HoxHou
# @File    : factory.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
import traceback
from warnings import filterwarnings
import aiomysql
from fastapi import FastAPI, Request, Response
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tortoise import Tortoise, run_async
# from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.main import logger, system, time, routers
from app.main.response import Msg
from app.main.settings.Development import DevConfig


class Application(object):
    def __init__(self, environment):
        env = "default" if system == "Windows" else environment  # 环境配置
        self.config = {
            "default": DevConfig,
            "dev": DevConfig
        }[env]

    @staticmethod
    def app_routers(app):
        """
        路由注册
        @param app:
        @return:
        """
        for router in routers.namespaces:
            app.include_router(**router)

    async def app_database(self):  # 数据库
        """
        Tortoise ORM
        https://tortoise-orm.readthedocs.io/en/latest/
        :return:
        """
        await Tortoise.init(self.config.TORTOISE_ORM)
        filterwarnings("ignore", category=aiomysql.Warning)  # 关闭告警
        # Generate the schema
        await Tortoise.generate_schemas()

    def app_logger(self):  # 应用日志
        """

        :return:
        """
        # logger.remove(handler_id=None)  # 移除控制台日志信息输出
        _zip = {"retention": self.config.RETENTION, "rotation": self.config.ROTATION, "compression": "zip"}
        # System Logs >>> INFO
        logger.add(self.config.LOG_PATH, format=self.config.INFO_FORMAT, level="INFO", enqueue=True, **_zip,
                   filter=lambda x: 'INFO' in str(x['level']).upper())
        # System Logs >>> ERROR
        logger.add(self.config.LOG_ERROR_PATH, format=self.config.ERROR_FORMAT, level="ERROR", enqueue=True, **_zip)
        # System Logs >>> DEBUG
        logger.add(self.config.LOG_PATH, format=self.config.DEBUG_FORMAT, level="DEBUG", enqueue=True, **_zip,
                   filter=lambda x: 'DEBUG' in str(x['level']).upper())

    def super_admin(self):  # 创建超级管理员账号
        pass

    def app_middleware(self, app: FastAPI):  # 应用中间件
        """
        https://fastapi.tiangolo.com/advanced/middleware/
        https://www.starlette.io/middleware/
        :param app:
        :return:
        """
        app.add_middleware(SessionMiddleware, secret_key=self.config.SECRET_KEY)
        app.add_middleware(
            TrustedHostMiddleware, allowed_hosts=["*"]  # 可信任Host访问
        )
        # 响应结果压缩，参数：当返回结果大小小于指定值时不启用压缩(单位为字节，默认值为500)
        app.add_middleware(GZipMiddleware, minimum_size=1000)
        # 指定允许跨域请求的url
        app.add_middleware(
            CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
        )
        # app.add_middleware(AuthenticationMiddleware, backend=BasicAuth())

    def init(self):
        app = FastAPI(
            title='FastDragon Web Service',
            description='闪龙 Web服务',
            version='v1.0.0',
        )

        @app.on_event('startup')
        async def startup():  # 应用启动
            logger.info(
                " ###### FastAPI Web Service *** FastDragon v1.0.0 ######\n"
                " |.--./-.--/-/..../---/-.| \n"
                " =========================== \n"
                " # Application >>> Startup #\n"
                " =========================== \n"
            )
            await self.app_database()  # 数据库初始化-异步操作

        @app.on_event('shutdown')
        async def shutdown():  # 应用停止
            pass

        @app.middleware('http')
        async def add_process_time_header(request: Request, call_next):  # call_next将接收request请求做为参数
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers['X-Process-Time'] = str(process_time)  # 添加自定义的以“X-”开头的请求头
            return response

        @app.middleware("http")
        async def register_hook(request: Request, call_next) -> Response:  # 请求异常处理
            try:
                response = await call_next(request)
            except Exception as e:
                logger.error(traceback.format_exc())
                response = JSONResponse(Msg(code=500000, message="后端服务异常！！！").body(error=str(e)))
            return response

        @app.exception_handler(Exception)  # 全局异常捕捉
        async def all_exception_handler(request: Request, exc: Exception):
            """
            :param request: 全局异常捕捉
            :param exc:
            :return:
            """
            logger.error(
                f">>> 全局异常 >>>\n"
                f"{request.method.upper()}:{request.url}\n"
                f"Headers:{request.headers}\n"
                f"Exception:{exc}\n"
                f"{traceback.format_exc()}")
            return JSONResponse()

        self.app_logger()  # 日志初始化
        self.app_middleware(app)  # 中间件初始化
        self.app_routers(app)  # 路由初始化
        return app
