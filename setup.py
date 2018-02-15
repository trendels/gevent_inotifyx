#!/usr/bin/env python
import re
from distutils.core import setup, Extension

with open('gevent_inotifyx/__init__.py') as f:
    version = re.search(r"^__version__ = '(.*)'", f.read(), re.M).group(1)

setup(
    name='gevent_inotifyx',
    version=version,
    description='gevent compatibility for inotifyx',
    author='Stanis Trendelenburg',
    author_email='stanis.trendelenburg@gmail.com',
    url='https://github.com/trendels/gevent_inotifyx',
    license='MIT',
    packages=['gevent_inotifyx'],
    ext_modules=[
        Extension(
            'gevent_inotifyx.vendor.inotifyx.binding',
            sources=['gevent_inotifyx/vendor/inotifyx/binding.c'],
        )
    ],
    install_requires=['gevent'],
)
