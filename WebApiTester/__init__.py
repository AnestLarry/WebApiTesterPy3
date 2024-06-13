import requests
from requests import Response
from typing import List, Dict
from WebApiTester.TestUnit import *


class client:
    def __init__(self) -> None:
        pass

    def get(self, url: str, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, verify=True) -> Response:
        res = requests.get(url=url, headers=headers,
                           params=query, verify=verify)
        return res

    def post(self, url: str, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, body: Dict[str, str] = {}) -> Response:
        res = requests.get(url=url, headers=headers, params=query, data=body)
        return res


class TesterEngine:
    client = client()
    web_sites: List[WebSite] = []

    def __init__(self) -> None:
        pass

    def add_website(self, wb: WebSite):
        self.web_sites.append(wb)

    def start(self) -> None:
        print("Tester Starting...")
        for ws in self.web_sites:
            print("\n\n  WebSite[{}]:".format(ws.path))
            for m in ws.modules:
                print("\n    Module[{}]:".format(m.path))
                m.add_headers(ws.headers)
                m.add_query(ws.query)
                for x in m.apis:
                    print("\n      Api[{}]:".format(x.path))
                    x.add_headers(m.headers)
                    x.add_query(m.query)
                    res = self.client.get(
                        url=ws.path+m.path+x.path,
                        headers=x.headers,
                        query=x.query,
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
