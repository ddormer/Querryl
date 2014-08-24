#!/usr/bin/env python
import os
from inspect import cleandoc
from setuptools import setup


def get_version():
    """
    Get the version from version module without importing more than
    necessary.
    """
    version_module_path = os.path.join(
        os.path.dirname(__file__), "querryl", "_version.py")
    # The version module contains a variable called __version__
    with open(version_module_path) as version_module:
        exec(version_module.read())
    return locals()["__version__"]


def read(path):
    """
    Read the contents of a file.
    """
    with open(path) as f:
        return f.read()


setup(
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Database :: Front-Ends",
        "Topic :: Communications :: Chat :: Internet Relay Chat"],
    name="querryl",
    version=get_version(),
    description=cleandoc("""
        Querryl is a Quassel-database searching web application.
        """),
    install_requires=["zope.interface>=3.6.0",
                      "twisted>=14.0.0",
                      "service_identity>=14.0.0",
                      "psycopg2>=2.5.3",
                      "txpostgres>=1.2",
                      "pyopenssl>=0.14"
                     ],
    keywords="twisted web irc log search quassel",
    license="MIT",
    packages=["querryl", "querryl.test"],
    url="https://github.com/ddormer/querryl",
    maintainer="Darren Dormer",
    long_description=read('README.rst'),
    test_suite="querryl")
