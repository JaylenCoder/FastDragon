# -*- coding: utf-8 -*-
# @Time    : 2022/2/12 18:19
# @Author  : HoxHou
# @File    : core_templates.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
INIT_FILE = """# -*- coding: utf-8 -*-
# @Time    : {create_time}
# @File    : __init__.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
from fastapi import APIRouter

router = APIRouter()
"""

VIEW_FILE = """# -*- coding: utf-8 -*-
# @Time    : {create_time}
# @File    : {view_file}.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
from starlette import status
from app.core.{view_name} import router
from app.main.response import Msg


@router.get("/{view_name}", status_code=status.HTTP_200_OK)
async def {view_name}():
    return Msg(code=status.HTTP_200_OK, message="访问{view_name} API 成功").body()
"""

SCHEMA_FILE = """# -*- coding: utf-8 -*-
# @Time    : {create_time}
# @File    : {schema_file}.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
"""

SERVICE_FILE = """# -*- coding: utf-8 -*-
# @Time    : {create_time}
# @File    : {service_file}.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
"""
