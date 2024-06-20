from datetime import datetime
import json
import os
import requests
from requests import Response
from typing import List, Dict
from WebApiTester.TestUnit import *
from WebApiTester.dumps import RuntimeDump, WebSiteDump, ModuleDump, ApiDump


class client:
    def __init__(self) -> None:
        pass

    def do(self, url: str, method: Method, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, body: Dict[str, str] = {}, verify=True) -> Response:
        match method:
            case Method.GET:
                return requests.get(url=url, headers=headers, params=query, verify=verify)
            case Method.POST:
                return requests.post(url=url, headers=headers, params=query, data=body, verify=verify)
            case Method.PUT:
                return requests.put(url=url, headers=headers, params=query, data=body, verify=verify)
            case Method.PATCH:
                return requests.patch(url=url, headers=headers, params=query, data=body, verify=verify)
            case _:
                raise "The [{}] method is not currently supported".format(
                    method)


class TesterEngine:
    client = client()
    web_sites: List[WebSite] = []

    def __init__(self) -> None:
        pass

    def add_website(self, wb: WebSite):
        self.web_sites.append(wb)

    def __combine_dict(self, ds: List[Dict[str, str]]) -> Dict[str, str]:
        r = {}
        for d in ds:
            r.update(d)
        return r

    def start(self, dumpNeed: bool = False, random_dump_name: bool = False) -> None:
        dump_res = RuntimeDump(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("Tester Starting...")
        for ws in self.web_sites:
            print("\n\nWebSite[{}]:".format(ws.path))
            if dumpNeed:
                dump_res.websites.append(WebSiteDump(
                    "{}-{}".format(self.web_sites.index(ws), ws.path), ws))
            for m in ws.modules:
                print("\n  Module[{}]:".format(m.path))
                if dumpNeed:
                    dump_res.websites[-1].modules.append(ModuleDump(
                        "{}-{}".format(ws.modules.index(m), m.path), m))
                for x in m.apis:
                    print("\n    Api[\"{}\" {}]:".format(x.path, x.method))
                    res: Response = self.client.do(
                        url=ws.path+m.path+x.path,
                        method=x.method,
                        headers=self.__combine_dict(
                            [ws.headers, m.headers, x.headers]),
                        query=self.__combine_dict(
                            [ws.query, m.query, x.query]),
                        body=x.data,
                        verify=ws.verify
                    )
                    x_status = x.verify(res)
                    if dumpNeed:
                        dump_res.websites[-1].modules[-1].apis.append(ApiDump(
                            "{}-{}".format(m.apis.index(x), x.path), x, x_status))
                        if x_status:
                            x_res = [i for i in x.notify(res) if not i is None]
                            m_res = [i for i in m.notify(res) if not i is None]
                            ws_res = [i for i in ws.notify(
                                res) if not i is None]
                            if len(x_res) > 0:
                                dump_res.websites[-1].modules[-1].apis[-1].hooks_results.extend(
                                    x_res)
                            if len(m_res) > 0:
                                dump_res.websites[-1].modules[-1].hooks_results.extend(
                                    m_res)
                            if len(ws_res) > 0:
                                dump_res.websites[-1].hooks_results.extend(
                                    ws_res)
                        else:
                            x_fail, m_fail, ws_fail = x.fail(
                                res), m.fail(res), ws.fail(res)
                            if not x_fail is None:
                                dump_res.websites[-1].modules[-1].apis[-1].hooks_results.append(
                                    x_fail)
                            if not m_fail is None:
                                dump_res.websites[-1].modules[-1].hooks_results.append(
                                    m_fail)
                            if not ws_fail is None:
                                dump_res.websites[-1].hooks_results.append(
                                    ws_fail)
                    else:
                        if x_status:
                            x.notify(res)
                            m.notify(res)
                            ws.notify(res)
                        else:
                            x.fail(res)
                            m.fail(res)
                            ws.fail(res)
        if dumpNeed:
            if not os.path.exists("./dumps"):
                os.mkdir("./dumps")
            filename = __class__.__name__
            if random_dump_name:
                filename = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            with open("./dumps/{}.json".format(filename), "w") as f:
                f.write(json.dumps(dict(dump_res), ensure_ascii=False))
