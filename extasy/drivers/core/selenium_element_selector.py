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



class SeleniumElementSelector(object):
    @staticmethod
    def element(element_type, element_name, **kw):
        if element_type == "element":
            return SeleniumElementSelector.generic(element_name, **kw)
        method = getattr(SeleniumElementSelector, element_type, SeleniumElementSelector.generic)
        return method(element_name, **kw)

    @staticmethod
    def generic(element_name):
        '''
        Returns a xpath that matches a generic element
        '''
        return r"%%(xpath)s//*[(@name='%s' or @id='%s')]" % (element_name, element_name)

    @staticmethod
    def button(element_name):
        '''
        Returns an xpath that matches input type="button", input type="submit" or button tags with
        the specified argument as id or name.
        '''
        return r"xpath=(%%(xpath)s//input[(@value='%s') and (@type='button' or @type='submit')])|(%%(xpath)s//button[.='%s'])" % (element_name, element_name)

    @staticmethod
    def radio(element_name, radio_group_key = None):
        '''
        Returns an xpath that matches ext radio with
        the specified label or boxlabel.
        '''
        if radio_group_key:
            return r"xpath=(%%(xpath)s//label[contains(concat(' ',@class, ' '),' x-form-item-label ') and .='%s']/../descendant::label[contains(concat(' ',@class, ' '),' x-form-cb-label ') and .='%s']/../input[contains(concat(' ',@class, ' '),' x-form-radio ')])[last()]" % (radio_group_key, element_name)
            
        return r"xpath=(%%(xpath)s//label[contains(concat(' ',@class, ' '),' x-form-cb-label ') and .='%s']/../input[contains(concat(' ',@class, ' '),' x-form-radio ')])[last()] | (%%(xpath)s//label[contains(concat(' ',@class, ' '),' x-form-item-label ') and .='%s']/../descendant::input[contains(concat(' ',@class, ' '),' x-form-radio ')])[last()]" % (element_name, element_name)


    @staticmethod
    def grid( element_name ):
        '''
        Returns an xpath that matches ext grid with
        the specified title.
        '''
        if element_name:
            return r"xpath=(%%(xpath)s//div[contains(concat(' ',@class, ' '),' x-grid-panel ')]/descendant::span[contains(concat(' ',@class, ' '),' x-panel-header-text ') and .='%s'])[last()]" % ( element_name )
            
        return r"xpath=(%(xpath)s//div[contains(concat(' ',@class, ' '),' x-grid-panel ')])[last()]"
        
    
    @staticmethod
    def window( element_name ):
        '''
        Returns an xpath that matches ext window with
        the specified title.
        '''
        if element_name:
            return r"xpath=(//div[contains(concat(' ',@class, ' '),' x-window ')]/descendant::span[contains(concat(' ',@class, ' '),' x-window-header-text ') and .='%s'])[last()]" % ( element_name )

        return r"xpath=(//div[contains(concat(' ',@class, ' '),' x-window ')])[last()]"
        
        
    @staticmethod
    def windowCloseButton( element_name ):
        '''
        Returns an xpath that matches ext window with
        the specified title.
        '''
        if element_name:
            return r"xpath=(//span[contains(concat(' ',@class, ' '),' x-window-header-text ') and .='%s']/ancestor::div[contains(concat(' ',@class, ' '),' x-window ')])[last()]/descendant::div[contains(concat(' ',@class, ' '),' x-tool-close ')]" % ( element_name )

        return r"xpath=(//div[contains(concat(' ',@class, ' '),' x-window ')])[last()]/descendant::div[contains(concat(' ',@class, ' '),' x-tool-close ')]"

     
        
    @staticmethod
    def gridLine( element_name, grid_line ):
        '''
        Returns an xpath that matches ext grid with
        the specified title.
        '''
        if grid_line == 'last':
            line_accessor = 'last()'
        else:
            line_accessor = 'position()=%s' % grid_line
            
        if element_name:
            return r"xpath=((%%(xpath)s//span[contains(concat(' ',@class, ' '),' x-panel-header-text ') and .='%s']/ancestor::div[contains(concat(' ',@class, ' '),' x-grid-panel ')])[last()])/descendant::div[contains(concat(' ',@class, ' '),' x-grid3-row ')][%s]" % ( element_name, line_accessor )

        return r"xpath=((%%(xpath)s//div[contains(concat(' ',@class, ' '),' x-grid-panel ')])[last()])/descendant::div[contains(concat(' ',@class, ' '),' x-grid3-row ')][%s]" % line_accessor
        
        

    @staticmethod
    def div(element_name):
        '''
        Returns an xpath that matches div tags with
        the specified argument as id or name.
        '''
        return r"//div[(@name='%s' or @id='%s')]" % (element_name, element_name)

    @staticmethod
    def link(element_name):
        '''
        Returns an xpath that matches link(a) tags with
        the specified argument as id or name.
        '''
        return r"//a[(@name='%s' or @id='%s' or contains(., '%s'))]" % \
                            (element_name, element_name, element_name)
    @staticmethod
    def checkbox(element_name, checkbox_group_key = None):
        '''
        Returns an xpath that matches ext checkbox with
        the specified label or boxlabel.
        '''
        if checkbox_group_key:
            return r"xpath=(%%(xpath)s//label[contains(concat(' ',@class, ' '),' x-form-item-label ') and .='%s']/../descendant::label[contains(concat(' ',@class, ' '),' x-form-cb-label ') and .='%s']/../input[contains(concat(' ',@class, ' '),' x-form-checkbox ')])[last()]" % (checkbox_group_key, element_name)
            
        return r"xpath=(%%(xpath)s//label[contains(concat(' ',@class, ' '),' x-form-cb-label ') and .='%s']/../input[contains(concat(' ',@class, ' '),' x-form-checkbox ')])[last()] | (%%(xpath)s//label[contains(concat(' ',@class, ' '),' x-form-item-label ') and .='%s']/../descendant::input[contains(concat(' ',@class, ' '),' x-form-checkbox ')])[last()]" % (element_name, element_name)


    @staticmethod
    def combobox(element_name):
        '''
        Returns an xpath that matches id of given combobox.
        '''
        return r"(%%(xpath)s//img[contains(concat(' ',@class, ' '),' x-form-arrow-trigger ')]/ancestor::div[contains(concat(' ',@class, ' '),' x-form-item ')]/descendant::label[contains(concat(' ',@class, ' '),' x-form-item-label ') and .='%s'])[last()]/ancestor::div[contains(concat(' ',@class, ' '),' x-form-item ')]/descendant::input[contains(concat(' ',@class, ' '),' x-form-field ')]" % (element_name)


    @staticmethod
    def select(element_name):
        '''
        Returns an xpath that matches Select tags with
        the specified argument as id or name.
        '''
        return r"//select[@name='%s' or @id='%s']" % (element_name, element_name)

    @staticmethod
    def textbox(element_name):
        '''
        Returns an xpath that matches input type="text", input without type attribute or textarea tags with
        the specified argument as id or name.
        '''
        return r"xpath=(%%(xpath)s//label[contains(concat(' ',@class, ' '),' x-form-item-label ') and .='%s']/..//input)[last()] | (%%(xpath)s//label[contains(concat(' ',@class, ' '),' x-form-item-label ') and .='%s']/..//textarea)[last()]" % (element_name,element_name)

    @staticmethod
    def image(element_name):
        '''
        Returns an xpath that matches img tags with
        the specified argument as id or name.
        '''
        return r"//img[@name='%s' or @id='%s']" % (element_name, element_name)
        
    @staticmethod
    def tab(element_name):
        '''
        Returns an xpath that matches ext tabs with 
        the specified argument as title.
        '''
        return r"xpath=(%%(xpath)s//span[contains(concat(' ',@class, ' '),' x-tab-strip-text  ') and .='%s'])[last()]/../../.." % (element_name)


    @staticmethod
    def tabScopeAggregator(element_name):
        '''
        Returns an xpath that matches ext tabs with 
        the specified argument as title.
        '''
        return r"xpath=//div[@id=substring-after(((%%(xpath)s//span[contains(concat(' ',@class, ' '),' x-tab-strip-text  ') and .='%s'])[last()]/ancestor::li)[1]/@id, '__')]" % (element_name)


    @staticmethod
    def tabCloseButton(element_name):
        '''
        Returns an xpath that matches ext tab close button with 
        the specified argument as title.
        '''
        return r"xpath=(%%(xpath)s//span[contains(concat(' ',@class, ' '),' x-tab-strip-text  ') and .='%s'])[last()]/../../../../a[contains(concat(' ',@class, ' '),' x-tab-strip-close ')]" % (element_name)


    @staticmethod
    def menuItem(element_name):
        '''
        Returns an xpath that matches ext menu item with
        the specified argument as title.
        '''
        return r"xpath=(%%(xpath)s//a[contains(concat(' ',@class, ' '),' x-menu-item ')]/span[.='%s'])[last()]/.." % (element_name)


    @staticmethod
    def treeNode(element_name):
        '''
        Returns an xpath that matches ext tree node with 
        the specified argument as title.
        '''
        return r"xpath=(%%(xpath)s//a[contains(concat(' ',@class, ' '),' x-tree-node-anchor ')]/span[.='%s'])[last()]/.." % (element_name)
        
    
    @staticmethod
    def treeNodeOpenButton(element_name):
        '''
        Returns an xpath that matches ext tree node open button with 
        the specified argument as title.
        '''
        return r"xpath=(%%(xpath)s//a[contains(concat(' ',@class, ' '),' x-tree-node-anchor ')]/span[.='%s'])[last()]/ancestor::div[contains(concat(' ',@class, ' '),' x-tree-node-el ')]/descendant::img[contains(concat(' ',@class, ' '),' x-tree-elbow-plus ') or contains(concat(' ',@class, ' '),' x-tree-elbow-end-plus ')]" % (element_name)


    @staticmethod
    def table(element_name):
        '''
        Returns an xpath that matches table tags with
        the specified argument as id or name.
        '''
        return r"//table[@name='%s' or @id='%s']" % (element_name, element_name)