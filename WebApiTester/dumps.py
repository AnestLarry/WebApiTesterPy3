import json
from WebApiTester.TestUnit import *
import copy


class DumpBase:
    def __str__(self) -> str:
        return json.dumps(dict(self))

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self):
        return dict(self)


class ApiDump(DumpBase):
    name: str
    content: Api
    status: bool

    def __init__(self, name: str, content: Module, status: bool) -> None:
        self.name = name
        self.content = content
        self.status = status

    def __iter__(self):
        yield from {
            "name": self.name,
            "content": {k: v for k, v in dict(self.content).items() if not_empty(v)},
            "status": self.status
        }.items()


class ModuleDump(DumpBase):
    name: str
    content: Module
    apis: list[ApiDump] = []

    def __init__(self, name: str, content: Module) -> None:
        self.name = name
        self.content = copy.deepcopy(content)
        self.content.apis = []

    def __iter__(self):
        yield from {
            "name": self.name,
            "content": {k: v for k, v in dict(self.content).items() if not_empty(v)},
            "apis": [{k: v for k, v in dict(api).items() if not_empty(v)} for api in self.apis]
        }.items()


class WebSiteDump(DumpBase):
    name: str
    content: WebSite
    modules: list[ModuleDump] = []

    def __init__(self, name: str, content: WebSite) -> None:
        self.name = name
        self.content = copy.deepcopy(content)
        self.content.modules = []

    def __iter__(self):
        yield from {
            "name": self.name,
            "content": {k: v for k, v in dict(self.content).items() if not_empty(v)},
            "modules": [{k: v for k, v in dict(module).items() if not_empty(v)} for module in self.modules]
        }.items()


class RuntimeDump(DumpBase):
    name: str
    websites: list[WebSiteDump]

    def __init__(self, name: str) -> None:
        self.name = name
        self.websites = []

    def __iter__(self):
        yield from {
            "name": self.name,
            "websites": [{k: v for k, v in dict(website).items() if not_empty(v)} for website in self.websites]
        }.items()

    def __str__(self) -> str:
        return json.dumps(dict(self))

    def __repr__(self) -> str:
        return self.__str__()
