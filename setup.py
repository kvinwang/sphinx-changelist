from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sphinx_changelist

classifiers = [
    "Programming Language :: Python :: 2",
]

with open("README.rst", "r") as fp:
    long_description = fp.read()

setup(name="sphinx_changelist",
      version=sphinx_changelist.__version__,
      author="Loongw",
      author_email="wy721@qq.com",
      url="http://pypi.python.org/pypi/sphinx_changelist/",
      py_modules=["sphinx_changelist"],
      description="A sphinx extension make is easy to place a Change list into your rst file",
      long_description=long_description,
      license="MIT",
      classifiers=classifiers
      )
