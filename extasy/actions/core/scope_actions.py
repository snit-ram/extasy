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

from extasy.page import PageRegistry, Page
from extasy.actions import ActionBase
from extasy.languages import LanguageItem
from extasy.scope import ScopeManager

def resolve_element_key(context, element_type, element_name, resolve_function):
    #Descomentar se der bug
    #element_type = element_type.encode("utf-8")
    
    element_category = context.language.get(element_type + "_category")
    
    if element_category:
        return resolve_function(context, element_category, element_name)
    
    return resolve_function(context, element_type, element_name)
    

class EnterScopeAction(ActionBase):
    '''h3. Example

  * And inside "Some" tab

h3. Description

This action enter element context'''
    __builtin__ = True
    regex = LanguageItem("context_line_regex")
 
    def execute(self, context, element_name, element_type = None):
        self.adjustScope()
        element_category = context.language.get(element_type + "_category") or element_type
        
        element_key = resolve_element_key(context, element_type, element_name, self.resolve_element_key)

        error_message = context.language.format("element_is_visible_failure", element_category, element_name)
        self.assert_element_is_visible(context, element_key, error_message)
        
        
        ScopeManager.enterScope( element_category, element_name, self.identation )