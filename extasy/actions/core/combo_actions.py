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

def resolve_element_key(context, element_type, element_name, resolve_function):
    element_category = context.language.get(element_type.encode("utf-8") + "_category")
    return resolve_function(context, element_category, element_name)


class ComboOpenAction(ActionBase):
    '''h3. Example

  * And I open "sports" combo

h3. Description

This action instructs the browser driver to open the specified ext combo.'''

    __builtin__ = True
    regex = LanguageItem("combo_open_regex")

    def execute(self, context, combo_name ):
        self.adjustScope()
        combo_key = self.resolve_element_key( context, 'combobox', combo_name )

        error_message = context.language.format("element_is_visible_failure", 'combobox', combo_name)
        self.assert_element_is_visible(context, combo_key, error_message)

        comboId = context.browser_driver.get_element_id( combo_key )
        
        script = """(function( comboId ){
            var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );
            combo.collapse();
            return 'ok';
        })( '%s' )""" % ( comboId )
        context.browser_driver.exec_js( script )
        
        combo_open_key = self.resolve_element_key( context, 'comboboxOpenButton', combo_name )
        context.browser_driver.click_element_at( combo_open_key, 5, 5 )
        
        
class ComboOptionsWaitForPresenceAction(ActionBase):
    '''h3. Example

  * And I wait for "some" combo options to be present
  * And I wait for "other" combo options to be present for 5 seconds

h3. Description

This action instructs the browser driver to open the specified ext combo.'''

    __builtin__ = True
    regex = LanguageItem("combo_options_wait_for_presence_regex")

    def execute(self, context, combo_name, timeout ):
        self.adjustScope()
        combo_key = self.resolve_element_key( context, 'combobox', combo_name )

        error_message = context.language.format("element_is_visible_failure", 'combobox', combo_name)
        self.assert_element_is_visible(context, combo_key, error_message)

        comboId = context.browser_driver.get_element_id( combo_key )

        script = """(function( comboId ){
            var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );
            if( !combo.list ) return '';
            return combo.list.dom.id;
        })( '%s' )""" % ( comboId )
        comboListId = context.browser_driver.exec_js( script )
        
        if not comboListId:
            error_message = context.language.format("combo_get_list_failure", combo_name )
            raise self.failed(error_message)

        if not timeout:
            timeout = extasy.DEFAULT_WAIT_FOR_PRESENCE_TIMEOUT
        timeout = int(timeout)
        
        element_key = self.resolve_element_key( context, 'comboboxOptions', comboListId )
        if not context.browser_driver.wait_for_element_present(element_key, timeout):
            error_message = context.language.format("element_wait_for_presence_failure", 'comboboxOptions', combo_name, timeout, element_key)
            raise self.failed(error_message)
        

class ComboCloseAction(ActionBase):
    '''h3. Example

  * And I close "sports" combo

h3. Description

This action instructs the browser driver to close the specified ext combo.'''

    __builtin__ = True
    regex = LanguageItem("combo_close_regex")

    def execute(self, context, combo_name ):
        self.adjustScope()
        combo_key = self.resolve_element_key( context, 'combobox', combo_name )

        error_message = context.language.format("element_is_visible_failure", 'combobox', combo_name)
        self.assert_element_is_visible(context, combo_key, error_message)

        comboId = context.browser_driver.get_element_id( combo_key )

        script = """(function( comboId ){
            var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );
            combo.collapse();
            return 'ok';
        })( '%s' )""" % ( comboId )
        result = context.browser_driver.exec_js( script )
        
        if not result:
            error_message = context.language.format("combo_close_failure", combo_name )
            raise self.failed(error_message)


class ComboOptionByValueAction(ActionBase):
    '''h3. Example

  * And I select the option with value of "1" in "sports" combo

h3. Description

This action instructs the browser driver to select the option in the specified ext combo that matches the specified value.'''

    __builtin__ = True
    regex = LanguageItem("combo_option_by_value_regex")

    def execute(self, context, combo_name, option_value):
        self.adjustScope()
        combo_key = self.resolve_element_key( context, 'combobox', combo_name )

        error_message = context.language.format("element_is_visible_failure", 'combo', combo_name)
        self.assert_element_is_visible(context, combo_key, error_message)
        
        comboId = context.browser_driver.get_element_id( combo_key )
        
        script = """(function( comboId, value ){
            var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );
            var record = combo.findRecord( combo.valueField, value );
            if( !record ){
                return '';
            }
            combo.collapse();
            combo.setValue( record.get( combo.valueField ) );
            return 'ok';
        })( '%s', '%s' )""" % ( comboId, option_value )
        
        result = context.browser_driver.exec_js( script )
        
        if not result:
            error_message = context.language.format("combo_option_by_value_failure", combo_name, option_value)
            raise self.failed(error_message)
            


class ComboHasSelectedValueAction(ActionBase):
    '''h3. Example

  * And I see "sports" combo has selected value of "1"

h3. Description

This action asserts that the currently selected option in the specified combo has the specified value.'''
    __builtin__ = True
    regex = LanguageItem("combo_has_selected_value_regex")

    def execute(self, context, combo_name, option_value):
        self.adjustScope()
        combo = resolve_element_key(context, 'combo', combo_name, self.resolve_element_key)
        error_message = context.language.format("element_is_visible_failure", 'combo', combo_name)
        self.assert_element_is_visible(context, combo, error_message)
        
        selected_value = context.browser_driver.get_selected_value(combo)

        if (unicode(selected_value) != unicode(option_value)):
            error_message = context.language.format("combo_has_selected_value_failure", combo_name, option_value, selected_value)
            raise self.failed(error_message)


class ComboOptionByIndexAction(ActionBase):
    '''h3. Example

  * And I select the option with index of 1 in "sports" combo

h3. Description

This action instructs the browser driver to select the option in the specified combo with the specified index.'''
    __builtin__ = True
    regex = LanguageItem("combo_option_by_index_regex")

    def execute(self, context, combo_name, index):
        self.adjustScope()
        index = int(index)
        combo_key = self.resolve_element_key( context, 'combobox', combo_name )

        error_message = context.language.format("element_is_visible_failure", 'combo', combo_name)
        self.assert_element_is_visible(context, combo_key, error_message)
        
        comboId = context.browser_driver.get_element_id( combo_key )
        
        script = """(function( comboId, index ){
            var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );
            if( index >= combo.getStore().getCont() ) return '';
            
            var record = combo.getStore().getAt(index);
            
            combo.setValue( record.get( combo.valueField ) );
            return 'ok';
        })( '%s', '%s' )""" % ( comboId, index )
        
        result = context.browser_driver.exec_js( script )
        
        if not result:
            error_message = context.language.format("combo_option_by_index_failure", combo_name, index)
            raise self.failed(error_message)

class ComboHasSelectedIndexAction(ActionBase):
    '''h3. Example

  * And I see "sports" combo has selected index of 1

h3. Description

This action asserts that the currently selected option in the specified combo has the specified index.'''
    __builtin__ = True
    regex = LanguageItem("combo_has_selected_index_regex")

    def execute(self, context, combo_name, index):
        self.adjustScope()
        combo = resolve_element_key(context, 'combo', combo_name, self.resolve_element_key)
        error_message = context.language.format("element_is_visible_failure", 'combo', combo_name)
        self.assert_element_is_visible(context, combo, error_message)
        
        selected_index = context.browser_driver.get_selected_index(combo)

        if (int(selected_index) != int(index)):
            error_message = context.language.format("combo_has_selected_index_failure", combo_name, index, selected_index)
            raise self.failed(error_message)

class ComboOptionByTextAction(ActionBase):
    '''h3. Example

  * And I select the option with text of "soccer" in "sports" combo

h3. Description

This action instructs the browser driver to select the option in the specified combo with the specified text.'''
    __builtin__ = True
    regex = LanguageItem("combo_option_by_text_regex")

    def execute(self, context, combo_name, text):
        self.adjustScope()
        combo_key = self.resolve_element_key( context, 'combobox', combo_name )

        error_message = context.language.format("element_is_visible_failure", 'combo', combo_name)
        self.assert_element_is_visible(context, combo_key, error_message)
        
        comboId = context.browser_driver.get_element_id( combo_key )
        
        script = """(function( comboId, value ){
            var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );
            var record = combo.findRecord( combo.displayField, value );
            if( !record ){
                return '';
            }
            combo.setValue( record.get( combo.valueField ) );
            return 'ok';
        })( '%s', '%s' )""" % ( comboId, text )
        
        result = context.browser_driver.exec_js( script )
        
        if not result:
            error_message = context.language.format("combo_option_by_text_failure", combo_name, text)
            raise self.failed(error_message)

class ComboHasSelectedTextAction(ActionBase):
    '''h3. Example

  * And I see "sports" combo has selected text of "soccer"

h3. Description

This action asserts that the currently selected option in the specified combo has the specified text.'''
    __builtin__ = True
    regex = LanguageItem("combo_has_selected_text_regex")

    def execute(self, context, combo_name, text):
        self.adjustScope()
        combo = resolve_element_key(context, 'combo', combo_name, self.resolve_element_key)
        error_message = context.language.format("element_is_visible_failure", 'combo', combo_name)
        self.assert_element_is_visible(context, combo, error_message)

        selected_text = context.browser_driver.get_selected_text(combo)

        if (selected_text != text):
            error_message = context.language.format("combo_has_selected_text_failure", combo_name, text, selected_text)
            raise self.failed(error_message)

class ComboDoesNotHaveSelectedIndexAction(ActionBase):
    '''h3. Example

  * And I see "sports" combo does not have selected index of 1

h3. Description

This action asserts that the currently selected option in the specified combo does not have the specified index.'''
    __builtin__ = True
    regex = LanguageItem("combo_does_not_have_selected_index_regex")

    def execute(self, context, combo_name, index):
        self.adjustScope()
        combo = resolve_element_key(context, 'combo', combo_name, self.resolve_element_key)

        error_message = context.language.format("element_is_visible_failure", 'combo', combo_name)
        self.assert_element_is_visible(context, combo, error_message)

        selected_index = context.browser_driver.get_selected_index(combo)

        if (selected_index == index):
            error_message = context.language.format("combo_does_not_have_selected_index_failure", combo_name, index, selected_index)
            raise self.failed(error_message)

class ComboDoesNotHaveSelectedValueAction(ActionBase):
    '''h3. Example

  * And I see "sports" combo does not have selected value of "1"

h3. Description

This action asserts that the currently selected option in the specified combo does not have the specified value.'''
    __builtin__ = True
    regex = LanguageItem("combo_does_not_have_selected_value_regex")

    def execute(self, context, combo_name, value):
        self.adjustScope()
        combo = resolve_element_key(context, 'combo', combo_name, self.resolve_element_key)

        error_message = context.language.format("element_is_visible_failure", 'combo', combo_name)
        self.assert_element_is_visible(context, combo, error_message)

        selected_value = context.browser_driver.get_selected_value(combo)

        if (selected_value == value):
            error_message = context.language.format("combo_does_not_have_selected_value_failure", combo_name, value, selected_value)
            raise self.failed(error_message)

class ComboDoesNotHaveSelectedTextAction(ActionBase):
    '''h3. Example

  * And I see "sports" combo does not have selected text of "soccer"

h3. Description

This action asserts that the currently selected option in the specified combo does not have the specified text.'''
    __builtin__ = True
    regex = LanguageItem("combo_does_not_have_selected_text_regex")

    def execute(self, context, combo_name, text):
        self.adjustScope()
        combo = resolve_element_key(context, 'combo', combo_name, self.resolve_element_key)

        error_message = context.language.format("element_is_visible_failure", 'combo', combo_name)
        self.assert_element_is_visible(context, combo, error_message)

        selected_text = context.browser_driver.get_selected_text(combo)

        if (selected_text == text):
            error_message = context.language.format("combo_does_not_have_selected_text_failure", combo_name, text, selected_text)
            raise self.failed(error_message)

class ComboContainsOptionWithTextAction(ActionBase):
    '''h3. Example

  * And I see "sports" combo contains an option with text "soccer"

h3. Description

This action asserts that the specified combo contains at least one option with the specified text.'''
    __builtin__ = True
    regex = LanguageItem("combo_contains_option_with_text_regex")

    def execute(self, context, combo_name, text):
        self.adjustScope()
        combo_key = self.resolve_element_key( context, 'combobox', combo_name )

        error_message = context.language.format("element_is_visible_failure", 'combo', combo_name)
        self.assert_element_is_visible(context, combo_key, error_message)
        
        comboId = context.browser_driver.get_element_id( combo_key )
        
        script = """(function( comboId, value ){
            var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );
            var record = combo.findRecord( combo.displayField, value );
            if( !record ){
                return '';
            }
            return 'ok';
        })( '%s', '%s' )""" % ( comboId, text )
        
        found = context.browser_driver.exec_js( script )
        
        if not found:
            error_message = context.language.format("combo_contains_option_with_text_failure", combo_name, text)
            raise self.failed(error_message)

class ComboDoesNotContainOptionWithTextAction(ActionBase):
    '''h3. Example

  * And I see "sports" combo does not contain an option with text "soccer"

h3. Description

This action asserts that the specified combo does not contain any options with the specified text.'''
    __builtin__ = True
    regex = LanguageItem("combo_does_not_contain_option_with_text_regex")

    def execute(self, context, combo_name, text):
        self.adjustScope()
        combo_key = self.resolve_element_key( context, 'combobox', combo_name )

        error_message = context.language.format("element_is_visible_failure", 'combo', combo_name)
        self.assert_element_is_visible(context, combo_key, error_message)
        
        comboId = context.browser_driver.get_element_id( combo_key )
        
        script = """(function( comboId, value ){
            var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );
            var record = combo.findRecord( combo.displayField, value );
            if( !record ){
                return '';
            }
            return 'ok';
        })( '%s', '%s' )""" % ( comboId, text )
        
        found = context.browser_driver.exec_js( script )
        
        if found:
            error_message = context.language.format("combo_does_not_contain_option_with_text_failure", combo_name, text)
            raise self.failed(error_message)
