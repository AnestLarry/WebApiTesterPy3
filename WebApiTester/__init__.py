import requests
from requests import Response
from typing import List, Dict
from WebApiTester.TestUnit import *


class client:
    def __init__(self) -> None:
        pass

    def do(self, url: str, method: Method, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, body: Dict[str, str] = {}, verify=True) -> Response:
        res: Response
        if method == Method.GET:
            res = requests.get(
                url=url, headers=headers, params=query, verify=verify)
        elif method == Method.POST:
            res = requests.post(
                url=url, headers=headers, params=query, data=body, verify=verify)
        elif method == Method.PUT:
            res = requests.put(
                url=url, headers=headers, params=query, data=body, verify=verify)
        elif method == Method.PATCH:
            res = requests.patch(
                url=url, headers=headers, params=query, data=body, verify=verify)
        else:
            raise "The [{}] method is not currently supported".format(method)
        return res


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

    def start(self, dumpNeed: bool = False) -> None:
        print("Tester Starting...")
        for ws in self.web_sites:
            print("\n\n  WebSite[{}]:".format(ws.path))
            for m in ws.modules:
                print("\n    Module[{}]:".format(m.path))
                for x in m.apis:
                    print("\n      Api[\"{}\" {}]:".format(x.path, x.method))
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
                    if res.status_code == 200:
                        x.notify(res)
                        m.notify(res)
                        ws.notify(res)
                    else:
                        x.fail(res)
                        m.fail(res)
                        ws.fail(res)
