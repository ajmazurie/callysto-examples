#!/usr/bin/env python

import setuptools

setuptools.setup(
    name = "example_bash_kernel",
    version = "0.1",
    packages = [
        "example_bash_kernel"],
    package_dir = {
        "example_bash_kernel": "lib"},
    dependency_links = [
        ("https://github.com/fgimian/paramiko-expect/tarball/"
         "943630a#egg=paramiko-expect-0.2+git")],
    install_requires = [
        "callysto==0.2",
        "paramiko",
        "paramiko-expect==0.2+git",
        "pexpect"])
