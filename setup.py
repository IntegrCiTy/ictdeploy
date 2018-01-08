#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import deployict

setup(

    name='deployict',

    version=deployict.__version__,

    packages=find_packages(),

    author="Pablo Puerto",

    author_email="pablito.73@hotmail.fr",

    description="help for multiple container deployment with specific environment",

    long_description=open('README.md').read(),

    install_requires=["pandas", "networkx >= 2", "docker"],

    include_package_data=True,

    # url='http://github.com/',

    classifiers=[
        "Natural Language :: English",
        "Operating GraphCreator :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Docker deployment",
    ]

)
