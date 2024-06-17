from setuptools import setup, find_packages
print(find_packages())
setup(
    name="WebApiTester",
    version="0.0.2",
    keywords=["setup", "Web API Tester"],
    description="A web API tester with easy use.",
    long_description="A web API tester with easy use. Using website, module and api as unit.",
    author="AnestLarry",
    author_email="32736719+AnestLarry@users.noreply.github.com",
    url="https://github.com/AnestLarry/WebApiTester",
    packages=["WebApiTester"],
    requires=["requests"],
    python_requires='>=3.10'
)
