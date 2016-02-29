#!/usr/bin/env python

import setuptools

setuptools.setup(
    name = "demo_bash_kernel",
    version = "0.1",
    packages = [
        "demo_bash_kernel"],
    package_dir = {
        "demo_bash_kernel": "lib"},
    install_requires = [
        "callysto==0.2",
        "pexpect"])
