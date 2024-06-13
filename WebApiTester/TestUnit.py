from typing import List, Dict, Callable, Any
from enum import Enum


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    HEAD = "HEAD"
    DELETE = "DELETE"


class Unit:
    path: str
    headers: Dict[str, str] = {}
    query: Dict[str, str] = {}
    fail_callable: Callable = None
    hooks: List[Callable] = None
    description: str = ""

    def add_hooks(self, h: Callable):
        self.hooks.append(h)

    def notify(self, x: Any):
        if not self.description is None and self.description != "":
            print("        description: {}".format(self.description))
        for f in self.hooks:
            f(x)

    def add_headers(self, h: Dict[str, str]) -> None:
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
    method: HTTPMethod

    def __init__(self, path: str, method: HTTPMethod, h: Dict[str, str] = {}, query: Dict[str, str] = {}, hooks: List[Callable] = [], description: str = "") -> None:
        super()
        self.path = path
        self.method = method
        self.headers = h
        self.query = query
        self.hooks = hooks
        self.description = description


class Module(Unit):
    def __init__(self, path: str, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, hooks: List[Callable] = [], apis: List[Api] = [], description: str = "") -> None:
        super()
        self.path = path
        self.headers = headers
        self.query = query
        self.hooks = hooks
        self.apis: List[Api] = apis
        self.description = description

    def add_apis(self, x: List[Api]):
        self.apis.extend(x)


class WebSite(Unit):
    verify: bool

    def __init__(self, host: str, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, verfiy_cert: bool = True, hooks: List[Callable] = [], modules: List[Module] = [], description: str = "") -> None:
        super()
        self.path = host
        self.headers = headers
        self.query = query
        self.verify = verfiy_cert
        self.hooks = hooks
        self.modules: List[Module] = modules
        self.description = description

    def add_modules(self, m: Module):
        self.modules.extend(m)
