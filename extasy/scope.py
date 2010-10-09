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

class ScopeManager(object):
    _scopeStack = []
    _baseIdentation = None
    
    def __init__( self ):
        raise Exception( "This is a singleton and must not be instantiated" )

    @classmethod
    def setBaseIdentationIfNeeded( self, identation ):
        if not ScopeManager._baseIdentation:
            ScopeManager._baseIdentation = identation

    @classmethod
    def restart( self ):
        ScopeManager._scopeStack = []
        ScopeManager._baseIdentation = None

    @classmethod
    def getIdentation( self ):
        if not ScopeManager._scopeStack:
            return ScopeManager._baseIdentation
            
        return ScopeManager._scopeStack[-1]['identation']
    
    @classmethod
    def inIdentation( self, identation ):
        return ScopeManager.getIdentation() == identation

    @classmethod
    def goToIdentation( self, identation ):
        if identation > ScopeManager.getIdentation():
            #increment last scope identation
            if not ScopeManager._scopeStack:
                ScopeManager._baseIdentation = identation
            else:
                ScopeManager._scopeStack[-1]['identation'] = identation
        else:
            #quit to given identation
            while ScopeManager._scopeStack:
                item = ScopeManager._scopeStack.pop()
                if item['identation'] <= identation:
                    return

    @classmethod
    def all( self ):
        return ScopeManager._scopeStack[:]

    @classmethod
    def enterScope( self, element_type, element_name, identation ):
        ScopeManager._scopeStack.append( {
            'type' : element_type,
            'key' : element_name,
            'identation' : identation
        } )