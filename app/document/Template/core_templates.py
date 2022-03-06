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
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()  # Step 1: Create a router
"""

VIEW_FILE = """# -*- coding: utf-8 -*-
# @Time    : {create_time}
# @File    : {view_file}.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
from fastapi_utils.cbv import cbv
from app.main.response import Msg
from app.core.{view_name} import router


@cbv(router)  # Step 2: Create and decorate a class to hold the endpoints
class {class_name}:
    # Step 3: Add dependencies as class attributes
    # ...
    
    @router.post("/{view_name}")
    async def create_item(self):
        # Step 4: Write the business logic
        return Msg(code=200000, message="Successfully").body()

    @router.get("/{view_name}")
    def query_item(self):
        return Msg(code=200000, message="Successfully").body()
    
    @router.put("/{view_name}")
    def update_item(self):
        return Msg(code=200000, message="Successfully").body()

    @router.delete("/{view_name}")
    def delete_item(self):
        return Msg(code=200000, message="Successfully").body()
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
