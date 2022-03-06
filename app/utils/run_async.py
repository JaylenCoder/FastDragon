# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 12:42
# @Author  : HoxHou
# @File    : run_async.py
# @Software: PyCharm
# Life was like a box of chocolates, you never know what you’re gonna get.
import asyncio
from typing import Coroutine


def fast_async(coroutine: Coroutine) -> None:
    """
    Simple async runner.

    Usage::

        from run_async import fast_async

            async def do_stuff():
                await func()
                )

                ...

            fast_async(do_stuff())
    @param coroutine:
    @return:
    """
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coroutine)
