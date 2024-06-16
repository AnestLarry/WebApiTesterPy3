from typing import List, Dict, Callable, Any, Union
from enum import Enum
from requests import Response

from WebApiTester.utils import not_empty


class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    HEAD = "HEAD"
    DELETE = "DELETE"


class Unit:
    path: str
    headers: Dict[str, str] = {}
    query: Dict[str, str] = {}
    fail_callable: Callable = None
    hooks: List[Callable[[Response], None]] = None
    description: str = ""
    data: str = ""

    def add_hooks(self, h: Callable):
        self.hooks.append(h)

    def notify(self, x: Callable[[Response], None]):
        if not self.description is None and self.description != "":
            print("        description: {}".format(self.description))
        for f in self.hooks:
            f(x)

    def add_header(self, h: Dict[str, str]) -> None:
        self.headers.update(h)

    def add_query(self, q: Dict[str, str]) -> None:
        self.query.update(q)

    def bind_fail(self, x: Callable):
        self.fail_callable = x

    def fail(self, x: Any):
        print(self.__class__+" is fail")
        if not self.fail_callable is None:
            self.fail_callable(x)


class Api(Unit):
    method: Method

    def __init__(self, path: str, method: Method, h: Dict[str, str] = {}, query: Dict[str, str] = {}, hooks: List[Callable[[Response], None]] = [], fail: Callable[[Response], None] = None, data: Union[object, str] = None, description: str = "") -> None:
        super()
        self.path = path
        self.method = method
        self.headers = h
        self.query = query
        self.hooks = hooks
        self.fail_callable = fail
        self.data = data
        self.description = description

    def __iter__(self):
        yield from {
            "path": self.path,
            "method": self.method.value,
            "headers": dict(self.headers),
            "query": dict(self.query),
            "data": self.data,
            "description": self.description
        }.items()


class Module(Unit):
    def __init__(self, path: str, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, hooks: List[Callable[[Response], None]] = [], fail: Callable[[Response], None] = None, apis: List[Api] = [], description: str = "") -> None:
        super()
        self.path = path
        self.headers = headers
        self.query = query
        self.hooks = hooks
        self.fail_callable = fail
        self.apis: List[Api] = apis
        self.description = description

    def add_apis(self, x: List[Api]):
        self.apis.extend(x)

    def __iter__(self):
        yield from {
            "path": self.path,
            "headers": self.headers,
            "query": self.query,
            "apis": [dict(x) for x in self.apis],
            "description": self.description
        }.items()


class WebSite(Unit):
    verify: bool

    def __init__(self, host: str, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, verfiy_cert: bool = True, hooks: List[Callable[[Response], None]] = [], fail: Callable[[Response], None] = None, modules: List[Module] = [], description: str = "") -> None:
        super()
        self.path = host
        self.headers = headers
        self.query = query
        self.verify = verfiy_cert
        self.hooks = hooks
        self.fail_callable = fail
        self.modules: List[Module] = modules
        self.description = description

    def add_modules(self, m: Module):
        self.modules.extend(m)

    def __iter__(self):
        yield from {
            "path": self.path,
            "headers": dict(self.headers),
            "query": dict(self.query),
            "verify": self.verify,
            "modules": [dict(x) for x in self.modules],
            "description": self.description
        }.items()
