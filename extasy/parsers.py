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
import os

from extasy import ActionRegistry
from extasy.actions import ActionNotFoundError
from extasy.languages import LanguageGetter
from extasy.common import locate
from extasy.fixture import Fixture
from extasy.fixture_items import Story, Action, Scenario

class InvalidScenarioError(RuntimeError):
    pass

class FSO(object):
    '''Actual Filesystem'''
    def list_files(self, directories, pattern):
        files = []
        for directory in directories:
            files.extend(locate(root=directory, pattern=pattern))
        return files

    def read_file(self, file_path):
        return open(file_path).read().decode('utf-8')

class FileParser(object):
    def __init__(self, language=None, file_object=None, action_registry=None):
        self.file_object = file_object and file_object or FSO()
        self.action_registry = action_registry and action_registry or ActionRegistry
        self.language = language
        self.used_actions = []

    def get_stories(self, settings):
        if not self.language:
            self.language = LanguageGetter(settings.default_culture)

        fixture = Fixture()

        story_file_list = self.file_object.list_files(directories=settings.tests_dirs, pattern=settings.file_pattern)
        story_file_list.sort()

        for story_file_path in story_file_list:
            try:
                parsed, error, story = self.parse_story_file(story_file_path, settings)
                if parsed:
                    fixture.append_story(story)
                else:
                    fixture.append_no_story_header(story_file_path)
            except IOError, err:
                fixture.append_invalid_test_file(story_file_path, err)
            except InvalidScenarioError, verr:
                fixture.append_no_story_header(story_file_path)
        return fixture

    def parse_story_file(self, story_file_path, settings):
        story_text = self.file_object.read_file(story_file_path)
        story_lines = [line.strip() for line in story_text.splitlines() if line.strip() != ""]
        orig_story_lines = [line for line in story_text.splitlines() if line.strip() != ""]

        headers = self.assert_header(story_lines, settings.default_culture)
        if not headers:
            return (False, self.language.get('no_header_failure'), None)

        as_a = headers[0]
        i_want_to = headers[1]
        so_that = headers[2]

        current_story = Story(as_a=as_a, i_want_to=i_want_to, so_that=so_that, identity=story_file_path)

        scenario_lines = story_lines[3:]
        orig_scenario_lines = orig_story_lines[3:]
        
        current_scenario = None
        offset = 0
        for line_index, line in enumerate(scenario_lines):
            if offset > 0:
                offset -= 1
                continue
            offset = 0
            if self.is_scenario_starter_line(line):
                current_scenario = self.parse_scenario_line(current_story, line, settings)
                current_area = None
                continue

            if self.is_keyword(line, "given"):
                current_area = "given"
                continue
            if self.is_keyword(line, "when"):
                current_area = "when"
                continue
            if self.is_keyword(line, "then"):
                current_area = "then"
                continue

            if current_scenario is None:
                if settings.scenarios_to_run:
                    continue
                else:
                    raise InvalidScenarioError("NoScenario")

            if not current_area:
                raise InvalidScenarioError("NoGivenWhenThen")

            add_method = getattr(current_scenario, "add_%s" % current_area)

            if line.startswith("#"):
                add_method(orig_scenario_lines[line_index], lambda context, *args, **kwargs: None, [], {})
                continue

            action, args, kwargs = self.action_registry.suitable_for(line, settings.default_culture)
            
            rows = []
            parsed_rows = []
            isContextLine = re.match( self.language.get( 'context_line_regex' ), line.strip() )
            if line.strip(' ').endswith(':') and not isContextLine:
                if line_index >= len(scenario_lines):
                    self.raise_action_not_found_for_line(line, current_scenario, story_file_path)
                
                offset, rows, parsed_rows = self.parse_rows(line_index, 
                                                            line, 
                                                            scenario_lines)

            
            if not action:
                self.raise_action_not_found_for_line(line, current_scenario, story_file_path)
            
            if not action in self.used_actions:
                self.used_actions.append(action)

            instance = action()
            if kwargs:
                args = []
            instance.number_of_rows = 1
            
            parsed_line = orig_scenario_lines[line_index]
            
            identation_line = FileParser.get_line_identation( parsed_line )
            instance.identation = identation_line
            
            if parsed_rows:
                kwargs['table'] = parsed_rows
                
                parsed_line = '\r\n'.join( rows )

            add_method(parsed_line, instance.execute, args, kwargs, identation = identation_line )

        return (True, None, current_story)

    def parse_rows(self, line_index, line, scenario_lines):
        line_identation = FileParser.get_line_identation(line)

        offset = 1

        next_line_index = line_index + offset
        next_line = scenario_lines[next_line_index]
        next_line_identation = FileParser.get_line_identation(next_line)
        
        rows = []
        parsed_rows = []
        keys = None

        while (next_line_identation > line_identation):
            next_line.indenteation = next_line_identation
            rows.append(next_line)
            values = [cell.strip(' ') for cell 
                                      in next_line.split('|') 
                                      if cell.strip(' ')]
            
            if not keys:
                keys = values
            else:
                row = {}
                for cell_index, cell in enumerate(values):
                    row[keys[cell_index]] = cell
                parsed_rows.append(row)
            
            offset += 1
            next_line_index = line_index + offset

            if next_line_index == len(scenario_lines):
                break

            next_line = scenario_lines[next_line_index]
            next_line_identation = FileParser.get_line_identation(next_line)
        
        return offset - 1, rows, parsed_rows, line_identation

    @classmethod
    def get_line_identation(self, line):
        identation = 0
        for character in line:
            if character == ' ' or character == '\t':
                identation += 1

        return identation

    def assert_header(self, story_lines, culture):
        as_a = self.language.get('as_a')
        i_want_to = self.language.get('i_want_to')
        so_that = self.language.get('so_that')

        if len(story_lines) < 3:
            return []

        if not as_a in story_lines[0] \
           or not i_want_to in story_lines[1] \
           or not so_that in story_lines[2]:
            return []

        return [story_lines[0].replace(as_a, "").strip(),
                 story_lines[1].replace(i_want_to, "").strip(),
                 story_lines[2].replace(so_that, "").strip()]

    def is_scenario_starter_line(self, line):
        scenario_keyword = self.language.get('scenario')
        return line.strip().startswith(scenario_keyword)

    def is_keyword(self, line, keyword):
        keyword = self.language.get(keyword)
        return line.strip() == keyword

    def parse_scenario_line(self, current_story, line, settings):
        scenario_keyword = self.language.get('scenario')
        scenario_values = line.split(u'-', 1)
        index = scenario_values[0].replace(scenario_keyword,"").strip()
        title = scenario_values[1].strip()
        current_scenario = None
        if not settings.scenarios_to_run or index in settings.scenarios_to_run:
            current_scenario = current_story.append_scenario(index, title)
        return current_scenario

    def raise_action_not_found_for_line(self, line, scenario, filename):
        raise ActionNotFoundError(line, scenario, filename)
