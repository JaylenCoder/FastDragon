# -*- coding: utf-8 -*-
# @Time    : 2022/2/12 17:27
# @Author  : HoxHou
# @File    : command.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
import click

from app.main.generator import Generator


@click.command()
@click.option('--name', prompt='模块名', help='输入模块名，生成业务层模块')
def core_creator(name):
    """ 业务模块生成器 """
    click.echo(f'Create {name} template files')
    Generator().core(name)


if __name__ == '__main__':
    core_creator()
