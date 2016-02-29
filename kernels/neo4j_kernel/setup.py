#!/usr/bin/env python

import setuptools

setuptools.setup(
    name = "demo_neo4j_kernel",
    version = "0.1",
    packages = [
        "demo_neo4j_kernel"],
    package_dir = {
        "demo_neo4j_kernel": "lib"},
    install_requires = [
        "callysto==0.2",
        "py2neo",
        "pydotplus",
        "pygraphviz"])
