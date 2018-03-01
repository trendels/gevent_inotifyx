#!/usr/bin/env python
import re
from setuptools import setup, find_packages, Extension

with open('gevent_inotifyx/__init__.py') as f:
    version = re.search(r"^__version__ = '(.*)'", f.read(), re.M).group(1)

with open('README.rst') as f:
    README = f.read()

setup(
    name='gevent_inotifyx',
    version=version,
    author='Stanis Trendelenburg',
    author_email='stanis.trendelenburg@gmail.com',
    url='https://github.com/trendels/gevent_inotifyx',
    license='MIT',
    packages=find_packages(),
    ext_modules=[
        Extension(
            'gevent_inotifyx.vendor.inotifyx.binding',
            sources=['gevent_inotifyx/vendor/inotifyx/binding.c'],
        )
    ],
    install_requires=['gevent'],
    description='gevent compatibility for inotifyx',
    long_description=README,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
