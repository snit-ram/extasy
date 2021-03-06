#!/usr/bin/python
# -*- coding: utf8 -*-

Version = "0.9.5"
Release = "Sunblast"
DEFAULT_WAIT_FOR_PAGE_TIMEOUT = 30
DEFAULT_WAIT_FOR_PRESENCE_TIMEOUT = 10
DEFAULT_WAIT_FOR_DISAPPEAR_TIMEOUT = 10
                    
class StepFailure( AssertionError ):
    pass
    
class _Settings( object ):
    settings = {}
    
    def setValues( self, values ):
        self.settings = {}
        for x in dir( values ):
            if not x.startswith( '_' ):
                self.settings[ x ] = getattr( values, x )
        return self.settings
    
    def get( self, att, default = None ):
        if att in self.settings:
            return self.settings[ att ] or default
            
        return default
        
    def set( self, att, value = None ):
        self.settings[ att ] = value
        
        
settings = _Settings()

                    
from pycukes.hooks import BeforeAll, AfterAll, BeforeEach, AfterEach
from console import extasy_console
from pycukes import *
import console

from scopemanager import *
import decorators
import scenario
import parser
import runner
import lang
import finder
import step_definitions as steps
from decorators import *
