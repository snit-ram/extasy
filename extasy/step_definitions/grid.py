import extasy
import extasy.selenium
import re
from extasy import *


def _getxpath( title = None ):
    if title:
        return r"(%(scope_xpath)s//div[contains(concat(' ',@class, ' '),' x-grid-panel ')]/descendant::span[contains(concat(' ',@class, ' '),' x-panel-header-text ') and .='%(title)s'])[last()]" % {
            'scope_xpath' : extasy.scope.get_xpath(),
            'title' : title
        }
        
    return r"(%(scope_xpath)s//div[contains(concat(' ',@class, ' '),' x-grid-panel ')])[last()]" % {
        'scope_xpath' : extasy.scope.get_xpath()
    }


def _get_line_xpath( title = None, line = None ):
    if title:
        return r"((%(scope_xpath)s//span[contains(concat(' ',@class, ' '),' x-panel-header-text ') and .='%(title)s']/ancestor::div[contains(concat(' ',@class, ' '),' x-grid-panel ')])[last()])/descendant::div[contains(concat(' ',@class, ' '),' x-grid3-row ')][%(line)s]//div[@class=contains( concat( ' ', @class, ' '), ' x-grid3-cell-inner ') ][1]" % {
            'scope_xpath' : extasy.scope.get_xpath(),
            'title' : title,
            'line' : line
        }

    return r"((%(scope_xpath)s//div[contains(concat(' ',@class, ' '),' x-grid-panel ')])[last()])/descendant::div[contains(concat(' ',@class, ' '),' x-grid3-row ')][%(line)s]//div[@class=contains( concat( ' ', @class, ' '), ' x-grid3-cell-inner ') ][1]" % {
        'scope_xpath' : extasy.scope.get_xpath(),
        'line' : line
    }
    
def _get_lines_xpath( title = None ):
    if title:
        return r"((%(scope_xpath)s//span[contains(concat(' ',@class, ' '),' x-panel-header-text ') and .='%(title)s']/ancestor::div[contains(concat(' ',@class, ' '),' x-grid-panel ')])[last()])/descendant::div[contains(concat(' ',@class, ' '),' x-grid3-row ')]" % {
            'scope_xpath' : extasy.scope.get_xpath(),
            'title' : title
        }

    return r"((%(scope_xpath)s//div[contains(concat(' ',@class, ' '),' x-grid-panel ')])[last()])/descendant::div[contains(concat(' ',@class, ' '),' x-grid3-row ')]" % {
        'scope_xpath' : extasy.scope.get_xpath()
    }



def _get_line_accessor( line ):
    line = line.strip()
    
    if extasy.lang.get( 'first' ) == line:
        return 1
    
    if extasy.lang.get( 'last' ) == line:
        return 'last()'
        
    return re.sub( '\D+', '', line ) 
    

@Given( \
    'I wait for grid to be present', \
    'I wait for "$title" grid to be present', \
    'I wait for grid to be present for $timout seconds', \
    'I wait for "$title" grid to be present for $timout seconds'
)
@When( \
    'I wait for grid to be present', \
    'I wait for "$title" grid to be present', \
    'I wait for grid to be present for $timout seconds', \
    'I wait for "$title" grid to be present for $timout seconds' \
)
@Then( \
    'I wait for grid to be present', \
    'I wait for "$title" grid to be present', \
    'I wait for grid to be present for $timout seconds', \
    'I wait for "$title" grid to be present for $timout seconds' \
)
def wait_for_presence( context, title = None, timeout = None ):
    xpath = 'xpath=%s' % _getxpath( title = title )

    if not timeout:
        timeout = extasy.DEFAULT_WAIT_FOR_PRESENCE_TIMEOUT
    timeout = int( timeout )

    if not extasy.selenium.getDriver().wait_for_element_present(xpath, timeout):
        if title:
            message = '"%s" grid should appear in %s seconds' % ( title, timeout )
        else:
            message = 'grid should appear in %s seconds' % ( timeout )
        raise StepFailure( message )


@Given( \
    'I wait for grid lines to be present', \
    'I wait for grid lines to be present for $timout seconds', \
    'I wait for "$title" grid lines to be present', \
    'I wait for "$title" grid lines to be present for $timout seconds' \
)
@When( \
    'I wait for grid lines to be present', \
    'I wait for grid lines to be present for $timout seconds', \
    'I wait for "$title" grid lines to be present', \
    'I wait for "$title" grid lines to be present for $timout seconds' \
)
@Then( \
    'I wait for grid lines to be present', \
    'I wait for grid lines to be present for $timout seconds', \
    'I wait for "$title" grid lines to be present', \
    'I wait for "$title" grid lines to be present for $timout seconds', \
    'grid lines should appear', \
    'grid lines should appear in $timeout seconds', \
    '"$title" grid lines should appear', \
    '"$title" grid lines should appear in $timeout seconds' \
)
def lines_wait_for_presence( context, title = None, timeout = None ):
    xpath = 'xpath=%s' % _get_lines_xpath( title = title )

    if not timeout:
        timeout = extasy.DEFAULT_WAIT_FOR_PRESENCE_TIMEOUT
    timeout = int( timeout )

    if not extasy.selenium.getDriver().wait_for_element_present(xpath, timeout):
        if title:
            message = 'lines of "%s" grid should appear in %s seconds' % ( title, timeout )
        else:
            message = 'lines of grid should appear in %s seconds' % ( timeout )
        raise StepFailure( message )  
 
def _line_click( context, title = None, line = None, dblclick = False ):
    line = _get_line_accessor( line )
    xpath = 'xpath=%s' % _get_line_xpath( title = title, line = line )

    if not extasy.selenium.getDriver().is_element_visible( xpath ):
        if title :
            message = '"%s" grid should exists and have lines' % ( title )
        else:
            message = 'grid should exists and have lines'
        raise StepFailure( message )

    if dblclick:
        extasy.selenium.getDriver().double_click_element_at(xpath, 1, 1)
    else:
        extasy.selenium.getDriver().click_element_at(xpath, 1, 1)
 
    
@Given( 'I click on $line line of grid', 'I click on $line line of "$title" grid' )
@When( 'I click on $line line of grid', 'I click on $line line of "$title" grid' )
@Then( 'I click on $line line of grid', 'I click on $line line of "$title" grid' )
def line_click( context, title = None, line = None ):
    return _line_click( context, title = None, line = None, dblclick = False )
    
@Given( 'I doubleclick $line line of grid', 'I doubleclick $line line of "$title" grid' )
@When( 'I doubleclick $line line of grid', 'I doubleclick $line line of "$title" grid' )
@Then( 'I doubleclick $line line of grid', 'I doubleclick $line line of "$title" grid' )
def line_doubleclick( context, title = None, line = None ):
    return _line_click( context, line=line, dblclick = True )