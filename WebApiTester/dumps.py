from WebApiTester.TestUnit import *


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
            "content": dict(self.content),
            "status": self.status
        }.items()


class ModuleDump(DumpBase):
    name: str
    content: Module
    apis: list[ApiDump] = []

    def __init__(self, name: str, content: Module) -> None:
        self.name = name
        self.content = content

    def __iter__(self):
        yield from {
            "name": self.name,
            "content": dict(self.content),
            "apis": [dict(x) for x in self.apis]
        }.items()


class WebSiteDump(DumpBase):
    name: str
    content: WebSite
    modules: list[ModuleDump] = []

    def __init__(self, name: str, content: WebSite) -> None:
        self.name = name
        self.content = content

    def __iter__(self):
        yield from {
            "name": self.name,
            "content": dict(self.content),
            "modules": [dict(x) for x in self.modules]
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
            "websites": [dict(website) for website in self.websites]
        }.items()

    def __str__(self) -> str:
        return json.dumps(dict(self))

    def __repr__(self) -> str:
        return self.__str__()
