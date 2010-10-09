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

class CheckboxCheckAction(ActionBase):
    '''h3. Example

  * And I check the "book" checkbox

h3. Description

This action checks the given checkbox.'''
    __builtin__ = True
    regex = LanguageItem("checkbox_check_regex")
 
    def execute(self, context, checkbox_key = None, checkbox_group_key = None):
        self.adjustScope()
        element_type = "checkbox"
        element_key = self.resolve_element_key(context, element_type, checkbox_key, checkbox_group_key=checkbox_group_key )

        error_message = context.language.format("element_is_visible_failure", element_type, checkbox_key)
        self.assert_element_is_visible(context, element_key, error_message)
        context.browser_driver.checkbox_check(element_key)

class CheckboxUncheckAction(ActionBase):
    '''h3. Example

  * And I uncheck the "book" checkbox

h3. Description

This action unchecks the given checkbox.'''
    __builtin__ = True
    regex = LanguageItem("checkbox_uncheck_regex")
 
    def execute(self, context, checkbox_key, checkbox_group_key = None):
        self.adjustScope()
        element_type = "checkbox"
        element_key = self.resolve_element_key(context, element_type, checkbox_key, checkbox_group_key=checkbox_group_key)

        error_message = context.language.format("element_is_visible_failure", element_type, checkbox_key)
        self.assert_element_is_visible(context, element_key, error_message)
        context.browser_driver.checkbox_uncheck(element_key)

class CheckboxIsCheckedAction(ActionBase):
    '''h3. Example

  * And I see the "book" checkbox is checked

h3. Description

This action asserts that the given checkbox is checked.'''
    __builtin__ = True
    regex = LanguageItem("checkbox_is_checked_regex")

    def execute(self, context, checkbox_key, checkbox_group_key = None):
        self.adjustScope()
        element_type = "checkbox"
        element_key = self.resolve_element_key(context, element_type, checkbox_key, checkbox_group_key=checkbox_group_key)

        error_messsage = context.language.format("element_is_visible_failure", element_type, checkbox_key)
        self.assert_element_is_visible(context, element_key, error_messsage)
        if not context.browser_driver.checkbox_is_checked(element_key):
            error_messsage = context.language.format("checkbox_is_checked_failure", checkbox_key)
            raise self.failed(error_messsage)

class CheckboxIsNotCheckedAction(ActionBase):
    '''h3. Example

  * And I see the "book" checkbox is not checked

h3. Description

This action asserts that the given checkbox is not checked.'''
    __builtin__ = True
    regex = LanguageItem("checkbox_is_not_checked_regex")

    def execute(self, context, checkbox_key, checkbox_group_key = None):
        self.adjustScope()
        element_type = "checkbox"
        element_key = self.resolve_element_key(context, element_type, checkbox_key, checkbox_group_key=checkbox_group_key)

        error_messsage = context.language.format("element_is_visible_failure", element_type, checkbox_key)
        self.assert_element_is_visible(context, element_key, error_messsage)
        if context.browser_driver.checkbox_is_checked(element_key):
            error_messsage = context.language.format("checkbox_is_not_checked_failure", checkbox_key)
            raise self.failed(error_messsage)
