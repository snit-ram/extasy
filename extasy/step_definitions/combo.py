# -*- coding: utf-8 -*-

import extasy
from extasy import *

def _get_open_button_xpath( label ):
    return r"(%(scope_xpath)s//img[contains(concat(' ',@class, ' '),' x-form-arrow-trigger ')]/ancestor::div[contains(concat(' ',@class, ' '),' x-form-item ')]/descendant::label[contains(concat(' ',@class, ' '),' x-form-item-label ') and .='%(label)s'])[last()]/ancestor::div[contains(concat(' ',@class, ' '),' x-form-item ')]//img[contains(concat(' ',@class, ' '),' x-form-arrow-trigger ')]" % {
        'scope_xpath' : extasy.scope.get_xpath(),
        'label' : label
    }

def _get_xpath( label ):
    return r"(%(scope_xpath)s//img[contains(concat(' ',@class, ' '),' x-form-arrow-trigger ')]/ancestor::div[contains(concat(' ',@class, ' '),' x-form-item ')]/descendant::label[contains(concat(' ',@class, ' '),' x-form-item-label ') and .='%(label)s'])[last()]/ancestor::div[contains(concat(' ',@class, ' '),' x-form-item ')]/descendant::input[contains(concat(' ',@class, ' '),' x-form-field ')]" % {
        'scope_xpath' : extasy.scope.get_xpath(),
        'label' : label
    }
    
def _get_options_xpath( comboId ):
    script = """(function( comboId ){
        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );
        if( !combo.list ) return '';
        return combo.list.dom.id;
    })( '%s' )""" % ( comboId )
    comboListId = extasy.selenium.getDriver().exec_js( script )
    return r"//div[@id='%s']//div[contains(concat(' ',@class, ' '),' x-combo-list-item ')]" % ( comboListId )

    
@Given('I open "$label" combo')
@When('I open "$label" combo')
@Then('I open "$label" combo')
def open( context, label ):
    combo_button_xpath = 'xpath=' + _get_open_button_xpath( label )
    combo_xpath = 'xpath=' + _get_xpath( label )
    
    if not extasy.selenium.getDriver().is_element_visible( combo_xpath ):
        raise StepFailure( '"%s" combo should exists and be visible' % label )
    
    comboId = extasy.selenium.getDriver().get_element_id( combo_xpath )
    script = """(function( comboId ){
        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );
        combo.collapse();
        return 'ok';
    })( '%s' )""" % ( comboId )
    extasy.selenium.getDriver().exec_js( script )
    
    extasy.selenium.getDriver().click_element_at( combo_button_xpath, 5, 5 )
    
    
@Given('I close "$label" combo')
@When('I close "$label" combo')
@Then('I close "$label" combo')
def close( context, label ):
    combo_button_xpath = 'xpath=' + _get_open_button_xpath( label )
    combo_xpath = 'xpath=' + _get_xpath( label )
    
    if not extasy.selenium.getDriver().is_element_visible( combo_xpath ):
        raise StepFailure( '"%s" combo should exists and be visible' % label )
    
    comboId = extasy.selenium.getDriver().get_element_id( combo_xpath )
    script = """(function( comboId ){
        var combo = selenium.browserbot.getCurrentWindow().Ext.getCmp( comboId );
        combo.collapse();
        return 'ok';
    })( '%s' )""" % ( comboId )
    result = extasy.selenium.getDriver().exec_js( script )
    

def _options_wait_for_presence( context, label, timeout = None ):
    combo_xpath = 'xpath=' + _get_xpath( label )
    
    if not extasy.selenium.getDriver().is_element_visible( combo_xpath ):
        raise StepFailure( '"%s" combo should exists and be visible' % label )

    comboId = extasy.selenium.getDriver().get_element_id( combo_xpath )
    options_xpath = 'xpath=' + _get_options_xpath( comboId )
    
    if not timeout:
        timeout = extasy.DEFAULT_WAIT_FOR_PRESENCE_TIMEOUT
    timeout = int(timeout)
    
    if not extasy.selenium.getDriver().wait_for_element_present(options_xpath, timeout):
        raise StepFailure( '"%s" combo options should be present in %s seconds' % (label, timeout) )
    
    
@Given('I wait for "$label" combo options to be present')
@When('I wait for "$label" combo options to be present')
@Then('I wait for "$label" combo options to be present')
def options_wait_for_presence( context, label ):
    _options_wait_for_presence( context, label )
 
 
@Given('I wait for "$label" combo options to be present for $timeout seconds')
@When('I wait for "$label" combo options to be present for $timeout seconds')
@Then('I wait for "$label" combo options to be present for $timeout seconds')
def options_wait_for_presence_timeout( context, label, timeout ):
    _options_wait_for_presence( context, label, timeout )