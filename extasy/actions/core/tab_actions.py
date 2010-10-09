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
import extasy

class TabClickAction(ActionBase):
    '''h3. Example

  * And I click the "book" tab

h3. Description

This action clicks on the given Ext tab.'''
    __builtin__ = True
    regex = LanguageItem("tab_click_regex")
    
 
    def execute(self, context, tab_key):
        self.adjustScope()
        element_type = "tab"
        element_key = self.resolve_element_key(context, element_type, tab_key)

        error_message = context.language.format("element_is_visible_failure", element_type, tab_key)
        self.assert_element_is_visible(context, element_key, error_message)
        context.browser_driver.click_element(element_key)


class TabCloseAction(ActionBase):
    '''h3. Example

  * And I close the "book" tab

h3. Description

This action closes the given Ext tab.'''
    __builtin__ = True
    regex = LanguageItem("tab_close_regex")
    
 
    def execute(self, context, tab_key):
        self.adjustScope()
        element_type = "tab"
        element_key = self.resolve_element_key(context, 'tabCloseButton', tab_key)

        error_message = context.language.format("element_is_visible_failure", element_type, tab_key)
        self.assert_element_is_visible(context, element_key, error_message)
        context.browser_driver.click_element(element_key)



class TabWaitForPresenceAction(ActionBase):
    '''h3. Examples

  * And I wait for "some" tab to be present
  * And I wait for "other" tab to be present for 5 seconds

h3. Description

Waits until a given ext tab appears or times out.

This action is really useful when you have some processing done (maybe AJAX) before an element is dynamically created.
'''
    __builtin__ = True
    regex = LanguageItem("tab_wait_for_presence_regex")

    def execute(self, context, tab_key, timeout):
        self.adjustScope()
        element_type = "tab"
        element_key = self.resolve_element_key( context, element_type, tab_key )

        if not timeout:
            timeout = extasy.DEFAULT_WAIT_FOR_PRESENCE_TIMEOUT
        timeout = int(timeout)

        if not context.browser_driver.wait_for_element_present(element_key, timeout):
            error_message = context.language.format("element_wait_for_presence_failure", element_type, tab_key, timeout, element_key)
            raise self.failed(error_message)