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

class MenuItemClickAction(ActionBase):
    '''h3. Example

  * And I click the "book" menu item

h3. Description

This action clicks on the given Ext menu item.'''
    __builtin__ = True
    regex = LanguageItem("menu_item_click_regex")
    
 
    def execute(self, context, menu_item_key):
        self.adjustScope()
        element_type = "menuItem"
        element_key = self.resolve_element_key(context, element_type, menu_item_key)

        error_message = context.language.format("element_is_visible_failure", element_type, menu_item_key)
        self.assert_element_is_visible(context, element_key, error_message)
        context.browser_driver.click_element(element_key)


class MenuItemMouseoverAction(ActionBase):
    '''h3. Example

  * And I mouseover "book" menu item

h3. Description

This action rolls mouse over the given Ext menu item.'''
    __builtin__ = True
    regex = LanguageItem("menu_item_mouseover_regex")


    def execute(self, context, menu_item_key):
        self.adjustScope()
        element_type = "menuItem"
        element_key = self.resolve_element_key(context, element_type, menu_item_key)

        error_message = context.language.format("element_is_visible_failure", element_type, menu_item_key)
        self.assert_element_is_visible(context, element_key, error_message)
        context.browser_driver.mouseover_element(element_key)
        

class MenuItemWaitForPresenceAction(ActionBase):
    '''h3. Examples

  * And I wait for "some" menu item to be present
  * And I wait for "other" menu item to be present for 5 seconds

h3. Description

Waits until a given ext menu item appears or times out.

This action is really useful when you have some processing done (maybe AJAX) before an element is dynamically created.
'''
    __builtin__ = True
    regex = LanguageItem("menu_item_wait_for_presence_regex")

    def execute(self, context, menu_item_key, timeout):
        self.adjustScope()
        element_type = "menuItem"
        element_key = self.resolve_element_key( context, element_type, menu_item_key )

        if not timeout:
            timeout = extasy.DEFAULT_WAIT_FOR_PRESENCE_TIMEOUT
        timeout = int(timeout)

        if not context.browser_driver.wait_for_element_present(element_key, timeout):
            error_message = context.language.format("element_wait_for_presence_failure", element_type, menu_item_key, timeout, element_key)
            raise self.failed(error_message)