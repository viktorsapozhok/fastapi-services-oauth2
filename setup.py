import os
from setuptools import setup

VERSION = "1.0.0"
APP_NAME = "app"

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION_PATH = os.path.join(ROOT_DIR, APP_NAME, "version.py")

with open(VERSION_PATH, "w") as f:
    f.write("__version__ = '{}'\n".format(VERSION))


def get_requirements():
    r = []
    with open("requirements.txt") as fp:
        for line in fp.read().split("\n"):
            if not line.startswith("#"):
                r += [line.strip()]
    return r


setup(
    name=APP_NAME,
    version=VERSION,
    description="FastAPI services with OAuth2",
    author="viktorsapozhok",
    url="https://github.com/viktorsapozhok/fastapi-services-oauth2",
    packages=[APP_NAME],
    include_package_data=True,
    zip_safe=False,
    install_requires=get_requirements(),
    entry_points={
        "console_scripts": [
            "mmapi=app.cli:main",
        ]
    },
    python_requires=">=3.10"
)
