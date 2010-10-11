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

import re

from extasy.errors import ActionFailedError, LanguageDoesNotResolveError
from extasy.languages import LanguageItem, AVAILABLE_GETTERS, LanguageGetter
from extasy.scope import ScopeManager
from extasy.drivers.core import selenium_element_selector
import re

ACTIONS = []

class ActionNotFoundError(Exception):
    def __init__(self, line, scenario, filename):
        self.line = line
        self.scenario = scenario
        self.filename = filename

    def __str__(self):
        return unicode(self)
    def __unicode__(self):
        return "Action Not Found: %s\nScenario: %s\nFilename: %s" % (self.line, self.scenario, self.filename)

class ActionRegistry(object):
    
    @classmethod
    def get_action_regex(cls, action, language, getter=None):
        getter = getter or AVAILABLE_GETTERS[language]
        regex = action.regex
        
        # prepare action regex to be used
        if isinstance(regex, (basestring, LanguageItem)):
            
            # if it's still a language item, get the actual regex in language file
            if isinstance(regex, LanguageItem):
                regex = getter.get(regex)
                if regex is None:
                    raise LanguageDoesNotResolveError('The language "%s" does not resolve the string "%s"' % (language, action.regex))
            
            supported_elements = getter.get("supported_elements")
            regex = regex.replace("<element selector>", supported_elements)
            regex = re.compile(regex)
            
            # store the compiled regex
            action.regex = regex
        
        return regex
        
    @classmethod
    def matches(cls, action, line, language, getter=None):
        ''' Checks if an Action can match a determined line. '''
        regex = cls.get_action_regex(action, language, getter)
        return regex.match(line)
    
    @classmethod
    def suitable_for(cls, line, language, getter=None):
        for Action in ACTIONS:
            matches = ActionRegistry.matches(Action, line, language, getter)
            if matches:
                args = matches.groups()
                kw = matches.groupdict()
                for k, v in kw.items():
                    del kw[k]
                    kw[str(k)] = v
                return Action, args, kw

        return None, None, None

class MetaActionBase(type):
    def __init__(cls, name, bases, attrs):
        if name not in ('ActionBase', ):
            if 'execute' not in attrs:
                raise NotImplementedError("The action %s does not implements the method execute()" % name)
            if 'regex' not in attrs:
                raise NotImplementedError("The action %s does not implements the attribute regex" % name)

            if not isinstance(attrs['regex'], basestring):
                regex = attrs['regex']
                raise TypeError("%s.regex attribute must be a string, got %r(%r)." % (regex.__class__, regex))

            # registering
            ACTIONS.append(cls)
            def actionSorting( a, b ):
                if a.__name__.startswith( 'Element' ):
                    if b.__name__.startswith( 'Element' ):
                        return 1 if a.__name__ >= b.__name__ else -1;
                    else:
                        return 1
                elif b.__name__.startswith( 'Element' ):
                    return -1;
                        
                return 1 if a.__name__ >= b.__name__ else -1;
            ACTIONS.sort( actionSorting )

        super(MetaActionBase, cls).__init__(name, bases, attrs)

class ActionBase(object):
    __metaclass__ = MetaActionBase
    failed = ActionFailedError

    @classmethod
    def can_resolve(cls, string):
        return re.match(cls.regex, string)
        
    def adjustScope( self ):
        from extasy.actions.core.scope_actions import EnterScopeAction
        
        ScopeManager.setBaseIdentationIfNeeded( self.identation )
        
        if isinstance( self, EnterScopeAction ):
            return
            
        if( not ScopeManager.inIdentation( self.identation ) ):
            ScopeManager.goToIdentation( self.identation )
            

    def execute_action(self, line, context, getter=None):
        # the getter is here for unit testing reasons
        Action, args, kwargs = ActionRegistry.suitable_for(line, context.settings.default_culture, getter=getter)

        if not Action:
            raise ActionNotFoundError(line, None, None)

        if isinstance(self, Action):
            raise RuntimeError('A action can not execute itself for infinite recursion reasons :)')

        action_to_execute = Action()
        if kwargs:
            args = []
        action_to_execute.execute(context, *args, **kwargs)

    def resolve_element_key(self, context, element_type, element_key, **kw):
        xpath = r''
        for scopeEl in ScopeManager.all():
            scopeAggregatorXPath = self.resolve_scope_aggregator_key( context, scopeEl[ 'type' ] + 'ScopeAggregator', scopeEl[ 'key' ], scopeEl).replace( '%(xpath)s', '%%(xpath)s%(xpath2)s' ) % { 'xpath2' : xpath }
            
            if( getattr( selenium_element_selector.SeleniumElementSelector, scopeEl[ 'type' ] + 'ScopeAggregatorBody' ) ):
                scopeAggregatorBodyXPath = self.base_resolve_element_key( context, scopeEl[ 'type' ] + 'ScopeAggregatorBody', scopeAggregatorXPath, action_context=context, action=self ).replace( '%(xpath)s', '%%(xpath)s%(xpath2)s' ) % { 'xpath2' : xpath }
                xpath = scopeAggregatorBodyXPath % { 'xpath' : xpath }
        
        xpath = self.base_resolve_element_key( context, element_type, element_key, **kw) % { 'xpath' : xpath }
        
        return 'xpath=%s' % xpath
        
        
    def resolve_scope_aggregator_key(self, context, element_type, element_key, baseScopeEl, **kw):
        xpath = r''
        baseScopeElIndex = ScopeManager.all().index( baseScopeEl )
        scopeList = ScopeManager.all()[:baseScopeElIndex]
        
        for scopeEl in scopeList:
            xpath = self.base_resolve_element_key( context, scopeEl[ 'type' ] + 'ScopeAggregator', scopeEl[ 'key' ], context=context, xpath=xpath ).replace( '%(xpath)s', '%%(xpath)s%(xpath2)s' ) % { 'xpath2' : xpath }

        xpath = self.base_resolve_element_key( context, element_type, element_key, **kw).replace( '%(xpath)s', '%%(xpath)s%(xpath2)s' ) % { 'xpath2' : xpath }

        return 'xpath=%s' % xpath
        

    def base_resolve_element_key(self, context, element_type, element_key, **kw):
        page = context.current_page

        resolved_element = None

        if page:
            resolved_element = page.get_registered_element(element_key, **kw)

        if not resolved_element:
            resolved_element = context.browser_driver.resolve_element_key(context, element_type, element_key, **kw)

        if not resolved_element:
            raise KeyError("No element could be resolved for element type %s and element key %s" % (element_type, element_key))

        resolved_element = re.sub( '^xpath=', '', resolved_element )

        return resolved_element

    def is_element_visible(self, context, selector):
        is_visible = context.browser_driver.is_element_visible(selector)
        return is_visible

    def assert_element_is_visible(self, context, selector, message):
        if not self.is_element_visible(context, selector):
            raise self.failed(message + "(Resolved to Element %s)" % selector)

    def assert_element_is_not_visible(self, context, selector, message):
        if self.is_element_visible(context, selector):
            raise self.failed(message + "(Resolved to Element %s)" % selector)

    @classmethod
    def all(cls):
        return ACTIONS
