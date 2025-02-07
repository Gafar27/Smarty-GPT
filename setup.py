#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages
import smartygpt

setup(
    name='smarty-gpt',
    version=smartygpt.__version__,
    description=(
        'A library of prompts/contexts that allows to enhance GPT models responses without the involvement of the user'
    ),
    url='https://github.com/citiususc/Smarty-GPT',
    author='Marcos Fernández-Pichel',
    author_email='marcosfernandez.pichel@usc.es',
    license='Apache License (Version 3.0)',
    packages=find_packages(),
    zip_safe=False,
    python_requires=">=3.6")