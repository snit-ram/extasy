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



import time
import traceback

from extasy.actions import ActionNotFoundError
from extasy.errors import *
from extasy.common import StatusItem, TimedItem, Status

class Story(StatusItem, TimedItem):
    '''Class that represents a story to be run by EXTasy.
    Contains zero or many scenarios to be run.'''
    def __init__(self, as_a, i_want_to, so_that, identity):
        StatusItem.__init__(self, parent=None)
        TimedItem.__init__(self)
        self.as_a = as_a
        self.i_want_to = i_want_to
        self.so_that = so_that
        self.identity = identity
        self.scenarios = []

    def append_scenario(self, index, title):
        scenario = Scenario(self, index, title)
        self.scenarios.append(scenario)
        return scenario

    def __unicode__(self):
        return "Story - As a %s I want to %s So that %s (%d scenarios) - %s" % \
                (self.as_a, self.i_want_to, self.so_that, len(self.scenarios), self.status)

    def __str__(self):
        return unicode(self)

class Scenario(StatusItem, TimedItem):
    def __init__(self, story, index, title):
        StatusItem.__init__(self, parent=story)
        TimedItem.__init__(self)

        self.story = story
        self.index = index
        self.title = title
        self.givens = []
        self.whens = []
        self.thens = []

    def add_given(self, action_description, execute_function, args, kwargs, identation = None):
        action = Action(self, action_description, execute_function, args, kwargs, identation = identation)
        self.givens.append(action)
        return action

    def add_when(self, action_description, execute_function, args, kwargs, identation = None):
        action = Action(self, action_description, execute_function, args, kwargs, identation = identation)
        self.whens.append(action)
        return action

    def add_then(self, action_description, execute_function, args, kwargs, identation = None):
        action = Action(self, action_description, execute_function, args, kwargs, identation = identation)
        self.thens.append(action)
        return action

    def __unicode__(self):
        return "Scenario %s - %s (%d givens, %d whens, %d thens) - %s" % \
                (self.index, self.title, len(self.givens), len(self.whens), len(self.thens), self.status)
    def __str__(self):
        return unicode(self)

class Action(StatusItem, TimedItem):
    def __init__(self, scenario, description, execute_function, args, kwargs, identation = None):
        StatusItem.__init__(self, parent=scenario)
        TimedItem.__init__(self)

        self.scenario = scenario
        self.description = description
        self.number_of_lines = len(description.split('\n'))
        self.execute_function = execute_function
        self.args = args
        self.kwargs = kwargs
        self.identation = identation

    def execute(self, context):
        if context.settings.on_before_action:
            context.settings.on_before_action(context, self, self.args, self.kwargs)
        try:
            self.execute_function(context, *self.args, **self.kwargs)
            if context.settings.on_action_successful:
                context.settings.on_action_successful(context, self, self.args, self.kwargs)
        except ActionNotFoundError:
            raise
        except AssertionError, err:
            if context.settings.on_action_error:
                context.settings.on_action_error(context, self, self.args, self.kwargs, err)
            self.mark_as_failed(err)
            return False
        except Exception, err:
            if context.settings.on_action_error:
                context.settings.on_action_error(context, self, self.args, self.kwargs, err)
            self.mark_as_failed(ValueError("Error executing action %s - %s" % (self.execute_function, traceback.format_exc(err))))
            return False

        self.mark_as_successful()
        return True

    def __unicode__(self):
        return "Action %s - %s" % (self.description, self.status)
    def __str__(self):
        return unicode(self)

