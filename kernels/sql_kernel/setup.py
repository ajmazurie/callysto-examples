#!/usr/bin/env python

import setuptools

setuptools.setup(
    name = "example_sql_kernel",
    version = "0.1",
    packages = [
        "example_sql_kernel"],
    package_dir = {
        "example_sql_kernel": "lib"},
    install_requires = [
        "callysto==0.2",
        "sqlparse"])
