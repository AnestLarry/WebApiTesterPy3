# this project is achieved. please use another [ts-version web-api-tester](https://github.com/AnestLarry/WebApiTester) to instead.

# WebApiTester

A web API tester with easy use.

## Getting Started

```python
from WebApiTester import TesterEngine
from WebApiTester.TestUnit import *

# example with Simserver project of mine
ws = WebSite("http://127.0.0.1:5000", modules=[
    Module(
        "/api/dl/ls/",
        apis=[
            Api("/", Method.GET,
                headers={"User-Agent": "TesterEngine"},
                hooks=[
                    lambda x: print(x.text)
                ],
                fail=print),
            Api("/", Method.GET,
                query={"page": 3},
                hooks=[
                    lambda x: x.text
                ],
                fail=print)
        ]
    )
])

engine = TesterEngine()
engine.add_website(ws)
engine.start(dumpNeed=True)
```

Running this example will get the result of `http://127.0.0.1:5000/api/dl/ls//` and `http://127.0.0.1:5000/api/dl/ls//?page=3` in console. If `dumpNeed` is set to `True`, the dumped data will be saved in `dump` folder.

### Installing

You can install it from PyPI. Python 3.10+ is required.

```shell
pip install git+https://github.com/AnestLarry/WebApiTester.git
```

Then you can import it in your project and using as `Getting Started`

## Deployment

You can deploy it with your favorite way. Or you could waiting for me to make another tool.

## Built With

- [Python](https://python.org/) - Programming Language.

## Contributing

Anyone can fork this project and make pull request. Feel free to contribute to this project. Please typed your variables or functions in coding and add comments to your code.

## Authors

- **Anest Larry** - Hobby and professional programmer.

See also the list of [contributors](https://github.com/AnestLarry/WebApiTester/contributors) who participated in this project.

## License

This project is licensed under the Dual License - see the [LICENSE.md](LICENSE.md) file for details
