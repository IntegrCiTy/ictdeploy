#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import ictdeploy

setup(

    name='ictdeploy',

    version=ictdeploy.__version__,

    packages=find_packages(),

    author="Pablo Puerto",

    author_email="pablo.puerto@mines-albi.fr",

    description="Multiple containers deployment with specific environment and orchestration",

    long_description=open('README.md').read(),

    install_requires=["pandas", "networkx >= 2", "docker", "docopt"],

    include_package_data=True,

    url='https://github.com/IntegrCiTy/ictdeploy',

    classifiers=[
        "Natural Language :: English",
        "Operating GraphCreator :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Docker deployment for co-simulation",
    ]

)
