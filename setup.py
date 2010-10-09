#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Rafael Marques Martins <snit.ram@gmail.com>
#
# This software is based in Pyccuracy (www.pyccuracy.org), wich is also
# licensed under Open Software License ("OSL") v. 3.0 (the "License")
#
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/osl-3.0.php
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from setuptools import setup, find_packages
from extasy import Version

#classifier should be changed to "Development Status :: 5 - Production/Stable" soon

setup(
    name = 'EXTasy',
    version = Version,
    description = "EXTasy is a BDD style Acceptance Testing framework based on Pyccuracy for ExtJS interfaces",
    long_description = """EXTasy is a Behavior-Driven Acceptance Testing framework based on Pyccuracy for ExtJS interfaces""",
    keywords = 'Acceptance Testing Accuracy Behavior Driven Development',
    author = 'EXTasy team',
    author_email = 'snit.ram@gmail.com',
    url = '',
    license = 'OSI',
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved',
                   'Natural Language :: English',
                   'Natural Language :: Portuguese (Brazilian)',
                   'Operating System :: MacOS',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.5',
                   'Programming Language :: Python :: 2.6',
                   'Topic :: Software Development :: Quality Assurance',
                   'Topic :: Software Development :: Testing',],
    packages = find_packages(),
    package_dir = {"extasy": "extasy"},
    include_package_data = True,
    package_data = {
        '': ['*.template'],
        'extasy.languages.data': ['*.txt'],
        'extasy.xslt': ['*.xslt'],
    },

    install_requires=[
        "selenium",
    ],

    entry_points = {
        'console_scripts': [
            'extasy_console = extasy.extasy_console:console',
            'extasy_help = extasy.extasy_help:console',
        ],
    },

)


