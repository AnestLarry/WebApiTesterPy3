from datetime import datetime
from typing import List, Dict, Callable, Any, Union
from enum import Enum
from requests import Response

from WebApiTester import utils


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
    fail_callable: Callable[[Response], Union[str, Dict, None]] = None
    hooks: List[Callable[[Response], Union[str, Dict, List, None]]] = None
    description: str = ""
    data: str = ""

    def add_hooks(self, h: Callable):
        self.hooks.append(h)

    def notify(self, x: Callable[[Response], Union[str, Dict, List, None]]) -> List[Union[str, Dict, List, None]]:
        if not self.description is None and self.description != "":
            print("        description: {}".format(self.description))
        res: List[Union[str, Dict, None]] = []
        for f in self.hooks:
            try:
                res.append(f(x))
            except Exception as e:
                res.append({"name": e.__class__.__name__, "message": str(
                    e), "traceback": str(e.__traceback__)})
        return res

    def add_header(self, h: Dict[str, str]) -> None:
        self.headers.update(h)

    def add_query(self, q: Dict[str, str]) -> None:
        self.query.update(q)

    def bind_fail(self, x: Callable[[Response], Union[str, Dict, None]]) -> None:
        self.fail_callable = x

    def fail(self, x: Any) -> Union[str, Dict, None]:
        if not self.fail_callable is None:
            print("{}: {} is fail".format(
                datetime.now().strftime("%Y-%m-%d %H-%M-%S"), self.__class__.__name__))
            return self.fail_callable(x)


class Api(Unit):
    method: Method
    verify: Callable[[Response], bool] = None

    def __init__(self, path: str, method: Method, headers: Dict[str, str] = {}, query: Dict[str, str] = {},
                 hooks: List[Callable[[Response], Union[str, Dict, List, None]]] = [], fail: Callable[[Response], Union[str, Dict, List, None]] = None,
                 verify: Callable[[Response], bool] = None, data: Union[object, str] = None, description: str = "") -> None:
        super()
        self.path = path
        self.method = method
        self.headers = headers
        self.query = query
        self.hooks = hooks
        self.fail_callable = fail
        self.data = data
        self.description = description
        if verify is None:
            self.verify = utils.status_code_eq_200
        else:
            self.verify = verify

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
    def __init__(self, path: str, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, hooks: List[Callable[[Response], Union[str, Dict, List, None]]] = [],
                 fail: Callable[[Response], Union[str, Dict, List, None]] = None, apis: List[Api] = [], description: str = "") -> None:
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

    def __init__(self, host: str, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, verfiy_cert: bool = True,
                 hooks: List[Callable[[Response], Union[str, Dict, List, None]]] = [], fail: Callable[[Response], Union[str, Dict, List, None]] = None,
                 modules: List[Module] = [], description: str = "") -> None:
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
