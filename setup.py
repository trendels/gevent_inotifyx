#!/usr/bin/env python
import re
from setuptools import setup

with open('gevent_inotifyx.py') as f:
    version = re.search(r"^__version__ = '(.*)'", f.read(), re.M).group(1)

setup(
    name='gevent_inotifyx',
    version=version,
    description='gevent compatibility for inotifyx',
    author='Stanis Trendelenburg',
    author_email='stanis.trendelenburg@gmail.com',
    url='https://github.com/trendels/gevent_inotifyx',
    license='MIT',
    py_modules=['gevent_inotifyx'],
    install_requires=['gevent', 'inotifyx'],
)
