# -*- coding: utf-8 -*-
# @Time    : 2022/02/12 21:01:19
# @File    : system_view.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
from starlette import status
from typing import Optional
from fastapi import Header, Request
from app.core.system import router
from app.main.response import Msg


@router.get("/", status_code=status.HTTP_200_OK)
@router.post("/", status_code=status.HTTP_200_OK)
async def index(request: Request, user_agent: Optional[str] = Header(None)):
    """ 主页 """
    visitor_info = {"UserAgent": user_agent, "IP": f"{request.client.host}:{request.client.port}"}
    for key, val in request.items():
        if key in ["http_version", "path", "method"]:
            visitor_info[key] = val
    return Msg(code=status.HTTP_200_OK, message="访问成功，欢迎使用闪龙Web API 框架！").body(data=visitor_info)
