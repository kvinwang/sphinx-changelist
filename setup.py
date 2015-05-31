from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sphinx_changelist

with open("README.rst", "r") as fp:
    long_description = fp.read()

setup(name="sphinx_changelist",
      version=sphinx_changelist.__version__,
      author="Loongw",
      author_email="wy721@qq.com",
      url="https://github.com/loongw/sphinx-changelist",
      py_modules=["sphinx_changelist"],
      description="A sphinx extension make is easy to place a **Changelist** into your rst file",
      long_description=long_description,
      license="MIT",
      classifiers=[
          "Programming Language :: Python :: 2"]
      )
