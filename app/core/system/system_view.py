# -*- coding: utf-8 -*-
# @Time    : 2022/02/12 21:01:19
# @File    : system_view.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
from typing import Optional
from fastapi import Header, Request
from fastapi_utils.cbv import cbv

from app.core.system.system_service import DemoClass
from app.main.response import Msg
from app.core.system import router


@cbv(router)  # Step 2: Create and decorate a class to hold the endpoints
class System:
    # Step 3: Add dependencies as class attributes
    # ...
    @router.get("/")
    async def index(self, request: Request, user_agent: Optional[str] = Header(None)):
        """ 主页 """
        visitor_info = {"UserAgent": user_agent, "IP": f"{request.client.host}:{request.client.port}"}
        for key, val in request.items():
            if key in ["http_version", "path", "method"]:
                visitor_info[key] = val
        return Msg(code=200000, message="访问成功，欢迎使用闪龙Web API 框架！").body(data=visitor_info)

    @router.post("/create_item")
    async def create_item(self):
        # Step 4: Write the business logic
        das = await DemoClass().demo_orm()
        return Msg(code=200000, message="Successfully").body(data=das)

    @router.get("/system")
    def query_item(self):
        return Msg(code=200000, message="Successfully").body()

    @router.put("/system")
    def update_item(self):
        return Msg(code=200000, message="Successfully").body()

    @router.delete("/system")
    def delete_item(self):
        return Msg(code=200000, message="Successfully").body()
