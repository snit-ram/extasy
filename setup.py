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
from src import Version
README = open('README.rst').read()

setup(
    name = 'extasy',
    version = Version,
    description = "EXTasy is a BDD framework bult on top of PyCukes for ExtJS interfaces",
    long_description=README,
    keywords = 'bdd behaviour behavior pyhistorian story',
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
    include_package_data = True,
    packages=['extasy',],
    package_dir={'extasy': 'src'},

    zip_safe=False,
    install_requires=[
        'story_parser>=0.1.2',
        'should_dsl',
        'pyhistorian>=0.6.8',
        'pycukes',
        'selenium'
    ],

    entry_points= {
        'console_scripts': ['extasy = extasy.console:main']},
)


