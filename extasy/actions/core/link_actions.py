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

class LinkHasHrefOfAction(ActionBase):
    '''h3. Example

  * And I see "logout" link has "/app/logout" href

h3. Description

This action asserts that a link has the given href attribute.'''
    __builtin__ = True
    regex = LanguageItem("link_has_href_regex")

    def execute(self, context, link_name, href):
        self.adjustScope()
        link = self.resolve_element_key(context, Page.Link, link_name)

        error_message = context.language.format("element_is_visible_failure", "link", link_name)
        self.assert_element_is_visible(context, link, error_message)

        current_href = context.browser_driver.get_link_href(link)

        if not current_href or current_href.lower().find(href.lower()) == -1:
            error_message = context.language.format("link_has_href_failure", link_name, href, current_href)
            raise self.failed(error_message)
