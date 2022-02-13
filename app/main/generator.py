# -*- coding: utf-8 -*-
# @Time    : 2022/2/12 17:27
# @Author  : HoxHou
# @File    : command.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
import traceback
from pathlib import Path
from app.document.Template.core_templates import INIT_FILE, VIEW_FILE, SCHEMA_FILE, SERVICE_FILE
from app.main import base_dir, now, logger


class Generator(object):

    @staticmethod
    def py_file_creator(file_dir, file_template):
        try:
            with open(file_dir, 'w', encoding='utf-8') as f:
                f.write(file_template)
        except ValueError:
            logger.error(f"Python 文件创建失败： {traceback.format_exc()}")

    def core(self, file_name):
        """

        :param file_name:
        :return:
        """
        file_dir = Path(base_dir) / "app" / "core" / file_name  # 创建文件目录
        create_time = now.format("YYYY/MM/DD HH:mm:ss")
        has_files = Path(file_dir).exists()  # 判断目录是否存在
        init_template = INIT_FILE.format(create_time=create_time)
        if has_files is False:
            file_dir.mkdir(parents=True, exist_ok=True)  # 创建目录
        init_py = file_dir / "__init__.py"  # 创建Python __init__.py文件
        self.py_file_creator(init_py, init_template)
        # 创建 view 文件
        view_py, view_file = file_dir / f"{file_name}_view.py", f"{file_name}_view"
        view_template = VIEW_FILE.format(create_time=create_time, view_file=view_file, view_name=file_name)
        self.py_file_creator(view_py, view_template)
        # 创建 schema 文件
        schema_py, schema_file = file_dir / f"{file_name}_schema.py", f"{file_name}_schema"
        view_template = SCHEMA_FILE.format(create_time=create_time, schema_file=schema_file)
        self.py_file_creator(schema_py, view_template)
        # 创建 service 文件
        service_py, service_file = file_dir / f"{file_name}_service.py", f"{file_name}_service"
        service_template = SERVICE_FILE.format(create_time=create_time, service_file=service_file)
        self.py_file_creator(service_py, service_template)


if __name__ == '__main__':
    name = "test"
    Generator().core(name)
