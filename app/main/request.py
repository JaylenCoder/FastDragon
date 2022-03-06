# -*- coding: utf-8 -*-
# @Time    : 2021/08/12 11:18
# @Author  : HoxJinXi
# @File    : request.py
# @Software: PyCharm
import requests
import http.client
from fake_headers import Headers
from requests import exceptions
from functools import wraps
from app.main.response import Msg
from app.utils.run_async import fast_async


def exception_catch(function):
    @wraps(function)
    async def decorated(*args, **kwargs):
        """
        异常捕捉
        @param args:
        @param kwargs:
        @return:
        """
        try:
            function_instance = await function(*args, **kwargs)
            return function_instance
        except exceptions.ChunkedEncodingError as E:
            if "IncompleteRead" in str(E):
                http.client.HTTPConnection._http_vsn = 10
                http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
                try:
                    function_instance = await function(*args, **kwargs)
                    return function_instance
                except Exception as E:
                    return Msg(message="RequestError").body(ChunkedEncodingError=f"{E}")
            else:
                return Msg(message="RequestError").body(ChunkedEncodingError=f"{E}")
        except exceptions.ConnectTimeout as E:
            return Msg(message="RequestError").body(ConnectTimeout=f"{E}")
        except exceptions.ConnectionError as E:
            return Msg(message="RequestError").body(ConnectionError=f"{E}")
        except exceptions.Timeout as E:
            return Msg(message="RequestError").body(Timeout=f"{E}")
        except Exception as E:
            return Msg(message="RequestError").body(ExceptionsContent=f"{E}")

    return decorated


class Requests(object):

    def __init__(self):
        self._req = requests.session()
        self._req.keep_alive = False

    @staticmethod
    def headers(browser="chrome", os="win", _headers: dict = None):
        """

        @param _headers:
        @param browser: 'chrome': chrome,'firefox': firefox,'opera': opera
        @param os: 'win': windows,'mac': macos,'lin': linux
        @return:
        """
        header = Headers(  # generate any browser & os headers
            os=os,
            browser=browser,
            headers=True  # don`t generate misc headers
        )
        header_generate = header.generate()
        header_generate.update(_headers)
        return header_generate

    @staticmethod
    def base_optional(**kwargs):
        """
        基础选项：'files', 'cookies', 'verify', 'timeout', 'auth', 'hooks'
        @param kwargs:
        @return:
        """
        optionals = ['files', 'cookies', 'verify', 'timeout', 'auth', 'hooks']
        kwargs.setdefault('verify', False)
        kwargs.setdefault('timeout', 60)
        return {key: val for key, val in kwargs.items() if key in optionals}

    @staticmethod
    def _response(url, response, resp_template=False):
        """

        @param url:
        @param response:
        @param resp_template: 定义响应模板
        @return:
        """
        if response.text:  # 过滤无响应结果的情况
            try:
                result = response.json()
            except Exception as E:
                result = {
                    "RequestUrl": url,
                    "StatusCode": f"{response.status_code}",
                    "Message": f"{E}",
                    "Exceptions": f"{response.text}"
                }
        else:
            result = {"Exceptions": f"No response content{response.text}"}
        if resp_template:
            return {
                "StatusCode": response.status_code,
                "ResponseTime": float(response.elapsed.microseconds / 1000),
                "ResponseSize": len(response.content),
                "Response": result
            }
        else:
            return result

    @exception_catch
    async def send(self, url: str, method: str, params: dict = None, data: dict = None, json: dict = None, **kwargs):
        """
        封装请求方法：Get/Post
        @param url:
        @param method:
        @param params:
        @param data:
        @param json:
        @param kwargs:
        @return:
        """
        headers = self.headers(_headers=kwargs.get("headers", {}))
        optional = self.base_optional(**kwargs)
        if method.lower() == "get":
            result = self._req.get(url, headers=headers, params=params, **optional)
        elif method.lower() == "post":
            result = self._req.post(url, headers=headers, data=data, json=json, **optional)
        else:
            result = {"Exceptions": "Request method not support !!!"}  # 报错：请求方式不支持
        response = self._response(url, result, resp_template=kwargs.get('resp_template'))
        return response

    async def get(self, url, params: dict = None, **kwargs):
        """

        @param url:
        @param params:
        @param kwargs:
        @return:
        """
        headers = self.headers(_headers=kwargs.get("headers", {}))
        optional = self.base_optional(**kwargs)
        result = self._req.get(url, headers=headers, params=params, **optional)
        response = self._response(url, result, resp_template=kwargs.get('resp_template'))
        return response

    async def post(self, url, data: dict = None, json: dict = None, **kwargs):
        """

        @param url:
        @param data:
        @param json:
        @param kwargs:
        @return:
        """
        headers = self.headers(_headers=kwargs.get("headers", {}))
        optional = self.base_optional(**kwargs)
        result = self._req.post(url, headers=headers, data=data, json=json, **optional)
        response = self._response(url, result, resp_template=kwargs.get('resp_template'))
        return response

    async def put(self, url, data: dict = None, json: dict = None, **kwargs):
        """

        @param url:
        @param data:
        @param json:
        @param kwargs:
        @return:
        """
        headers = self.headers(_headers=kwargs.get("headers", {}))
        optional = self.base_optional(**kwargs)
        result = self._req.put(url, headers=headers, data=data, json=json, **optional)
        response = self._response(url, result, resp_template=kwargs.get('resp_template'))
        return response

    async def patch(self, url, data: dict = None, json: dict = None, **kwargs):
        """

        @param url:
        @param data:
        @param json:
        @param kwargs:
        @return:
        """
        headers = self.headers(_headers=kwargs.get("headers", {}))
        optional = self.base_optional(**kwargs)
        result = self._req.patch(url, headers=headers, data=data, json=json, **optional)
        response = self._response(url, result, resp_template=kwargs.get('resp_template'))
        return response

    async def delete(self, url, data: dict = None, json: dict = None, **kwargs):
        """

        @param url:
        @param data:
        @param json:
        @param kwargs:
        @return:
        """
        headers = self.headers(_headers=kwargs.get("headers", {}))
        optional = self.base_optional(**kwargs)
        result = self._req.delete(url, headers=headers, data=data, json=json, **optional)
        response = self._response(url, result, resp_template=kwargs.get('resp_template', True))
        return response


if __name__ == '__main__':
    _url = "https://www.reddit.com/r/walkoffcommunity/"
    fast_async(Requests().send(_url, "get"))
