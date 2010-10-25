#!/usr/bin/python
# -*- coding: utf8 -*-

from finder import (extasy_find_steps_modules,
                    find_text_specs,
                    find_before_all,
                    find_before_each,
                    find_after_all,
                    find_after_each,)
                    
from pycukes.runner import StoryRunner

from optparse import OptionParser
import sys
import os
import extasy

def extasy_console(stories_dir, steps_dir, output, colored=False, settings = None):
    modules = extasy_find_steps_modules(steps_dir)
    extasy.settings.setValues( settings )
    extasy.selenium.getDriver().start_test()
    for spec in find_text_specs(stories_dir):
        StoryRunner(spec, output, colored=colored, modules=modules).run()
    extasy.selenium.getDriver().stop_test()

def main():
    steps_modules = []
    files = []
    before_all_methods = []
    before_each_methods = []
    after_all_methods = []
    after_each_methods = []
    stories_dirname = 'stories'

    parser = OptionParser()
    parser.add_option('-s', '--stories-dir', default=None, dest='stories_dir')
    parser.add_option('-t', '--steps-dir', default=None, dest='steps_dir')
    parser.add_option('-n', '--no-colors', default=None, action='store_true', dest='no_colors')
    parser.add_option('-l', '--language', default='en-us', dest='language')
    parser.add_option('', '--selenium-server', default='localhost', dest='selenium-server')
    parser.add_option('', '--selenium-port', default='4444', dest='selenium-port')
    parser.add_option('', '--browser', default='firefox', dest='browser')
    parser.add_option('', '--base-url', default=None, dest='base-url')
    values, args = parser.parse_args()
    
    extasy.settings.setValues( values )

    for arg in args:
        files.append(arg)
        stories_dirname = os.path.dirname(arg) or '.'
    
    try:
        if values.stories_dir:
            files.extend([values.stories_dir+'/'+filename for filename in os.listdir(values.stories_dir)
                            if filename.endswith('.story')])
            stories_dirname = values.stories_dir
        elif files == []:
            files.extend([stories_dirname+'/'+filename for filename in os.listdir(stories_dirname)
                                              if filename.endswith('.story')])

        steps_modules = extasy_find_steps_modules(values.steps_dir or stories_dirname+'/step_definitions')
    except OSError, e:
        pass

    if os.path.exists(stories_dirname+'/support'):
        before_all_methods = find_before_all(stories_dirname+'/support')
        after_all_methods = find_after_all(stories_dirname+'/support')
        before_each_methods = find_before_each(stories_dirname+'/support')
        after_each_methods = find_after_each(stories_dirname+'/support')

    colored = True
    if values.no_colors:
        colored = False

    exit_code = True
    
    extasy.selenium.getDriver().start_test()
    for index, story in enumerate(files):
        story_status = StoryRunner(open(story).read(),
                                         sys.stdout,
                                         colored=colored,
                                         modules=steps_modules,
                                         language=values.language,
                                         before_all=before_all_methods,
                                         before_each=before_each_methods,
                                         after_all=after_all_methods,
                                         after_each=after_each_methods).run()
        exit_code = exit_code and story_status
        if index < len(files)-1:
            sys.stdout.write('\n\n')

    extasy.selenium.getDriver().stop_test()
    
    exit(int(not exit_code))
