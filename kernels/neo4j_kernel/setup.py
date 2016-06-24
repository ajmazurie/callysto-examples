#!/usr/bin/env python

import setuptools

setuptools.setup(
    name = "example_neo4j_kernel",
    version = "0.1",
    packages = [
        "example_neo4j_kernel"],
    package_dir = {
        "example_neo4j_kernel": "lib"},
    install_requires = [
        "callysto==0.2",
        "neo4j-driver"])
