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



from os.path import dirname, abspath, join, split
from glob import glob

base_path = abspath(dirname(__file__))
pattern = join(base_path, "*.py")
__all__ = [split(x)[1][:-3] for x in glob(pattern)]
