#!/usr/bin/env python
import re
from distutils.core import Command, setup

__version__ = re.search(r"^__version__ = '(.*)'",
                        open('gevent_inotifyx.py', 'r').read(),
                        re.M).group(1)

class TestCommand(Command):
    """Custom distutils command to run the test suite."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import unittest
        import test_gevent_inotifyx
        suite = unittest.TestLoader().loadTestsFromModule(test_gevent_inotifyx)
        unittest.TextTestRunner(verbosity=2).run(suite)

setup(name='gevent_inotifyx',
      version=__version__,
      description='gevent compatibility for inotifyx',
      author='Stanis Trendelenburg',
      author_email='stanis.trendelenburg@gmail.com',
      url='https://github.com/trendels/gevent_inotifyx',
      license='MIT',
      py_modules=['gevent_inotifyx'],
      cmdclass = {'test': TestCommand},
)
