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
import extasy, re


class GridWaitForPresenceAction(ActionBase):
    '''h3. Examples

  * And I wait for "some" grid to be present
  * And I wait for "other" grid to be present for 5 seconds

h3. Description

Waits until a given ext tab appears or times out.

This action is really useful when you have some processing done (maybe AJAX) before an element is dynamically created.
'''
    __builtin__ = True
    regex = LanguageItem("grid_wait_for_presence_regex")

    def execute(self, context, grid_key, timeout):
        self.adjustScope()
        element_type = "grid"
        element_key = self.resolve_element_key( context, element_type, grid_key )

        if not timeout:
            timeout = extasy.DEFAULT_WAIT_FOR_PRESENCE_TIMEOUT
        timeout = int(timeout)

        if not context.browser_driver.wait_for_element_present(element_key, timeout):
            error_message = context.language.format("element_wait_for_presence_failure", element_type, grid_key, timeout, element_key)
            raise self.failed(error_message)
            
            
class GridClickOnLineAction(ActionBase):
    '''h3. Examples

  * And I click on the first line of "some" grid
  * And I click on the 1st line of "some" grid
  * And I click on the 2nd line of "some" grid
  * And I click on the 3rd line of "some" grid
  * And I click on the 3th line of "some" grid
  * And I click on the last line of "some" grid

h3. Description

Clicks on the specified line of given grid
'''
    __builtin__ = True
    regex = LanguageItem("grid_click_on_line_regex")

    def execute(self, context, grid_key, grid_line = ''):
        self.adjustScope()
        element_type = "gridLine"
        
        grid_line = grid_line.strip()
        grid_line = re.sub( context.language.get( 'grid_line_number_first_regex' ), '1', grid_line )
        grid_line = re.sub( context.language.get( 'grid_line_number_last_regex' ), 'last', grid_line )
        if grid_line != 'last':
            grid_line = re.sub( r'\D', '', grid_line )
        
        element_key = self.resolve_element_key( context, element_type, grid_key, grid_line=grid_line )

        error_message = context.language.format("element_is_visible_failure", element_type, grid_key)
        self.assert_element_is_visible(context, element_key, error_message)
        context.browser_driver.click_element_at(element_key, 30, 1)
        
        
class GridDoubleClickOnLineAction(ActionBase):
    '''h3. Examples

  * And I doubleclick the first line of "some" grid
  * And I doubleclick the 1st line of "some" grid
  * And I doubleclick the 2nd line of "some" grid
  * And I doubleclick the 3rd line of "some" grid
  * And I doubleclick the 3th line of "some" grid
  * And I doubleclick the last line of "some" grid

h3. Description

Doubleclicks the specified line of given grid
'''
    __builtin__ = True
    regex = LanguageItem("grid_doubleclick_on_line_regex")

    def execute(self, context, grid_key, grid_line = ''):
        self.adjustScope()
        element_type = "gridLine"

        grid_line = grid_line.strip()
        grid_line = re.sub( context.language.get( 'grid_line_number_first_regex' ), '1', grid_line )
        grid_line = re.sub( context.language.get( 'grid_line_number_last_regex' ), 'last', grid_line )
        if grid_line != 'last':
            grid_line = re.sub( r'\D', '', grid_line )

        element_key = self.resolve_element_key( context, element_type, grid_key, grid_line=grid_line )

        error_message = context.language.format("element_is_visible_failure", element_type, grid_key)
        self.assert_element_is_visible(context, element_key, error_message)
        context.browser_driver.double_click_element_at(element_key, 30, 1)