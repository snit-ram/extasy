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



from __future__ import absolute_import

from os.path import abspath, dirname, join, exists
import warnings
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

from extasy.extasy_console import main as run_extasy
from extasy.common import locate

class Command(BaseCommand):
    help = "Runs extasy tests for all apps (EXPERIMENTAL)"
    option_list = BaseCommand.option_list + (
        make_option("-s", "--scenario", dest=u"scenario", default=None, help=u"Number (index) for the scenario to be executed. Use commas for several scenarios. I.e.: -s 3,6,7 or --scenario=3,6,7."),
        make_option("-t", "--testfolder", dest=u"testfolder", default="tests/acceptance", help=u"Directory to look for tests (starting from each app)."),
        make_option("-l", "--loglevel", dest=u"loglevel", default=1, help=u"Verbosity: 1, 2 ou 3."),
        make_option("-u", "--baseurl", dest=u"baseurl", default=u"http://localhost:8000", help=u"Base Url for acceptance tests. Defaults to http://localhost:8000."),
        make_option("-p", "--pattern", dest=u"pattern", default=u"*.story", help=u"Pattern (wildcard) to be used to find acceptance tests."),
        make_option("-b", "--browser", dest=u"browser", default=u"firefox", help=u"Browser that will be used to run the tests."),
        make_option("-w", "--workers", dest=u"workers", default=1, help=u"Number of tests to be run in parallel."),
        make_option("-c", "--language", dest=u"language", default='en-us', help=u"Language to run the tests in. Defaults to 'en-us'."),
        make_option("-a", "--app", dest=u"apps", default=None, help=u"Only run the specified apps - comma separated."),
        make_option("-n", "--supresswarning", action="store_true", dest=u"supress_warnings", default=False, help=u"Supress EXTasy warnings."),
    )

    def locate_resource_dirs(self, complement, pattern="*.*", recursive=True, apps=[]):
        dirs = []

        for app in settings.INSTALLED_APPS:
            fromlist = ""

            if len(app.split("."))>1:
                fromlist = ".".join(app.split(".")[1:])

            if app.startswith('django'):
                continue

            if apps and not app in apps:
                continue

            module = __import__(app, fromlist=fromlist)
            app_dir = abspath("/" + "/".join(module.__file__.split("/")[1:-1]))

            resource_dir = join(app_dir, complement)

            if exists(resource_dir) and locate(pattern, resource_dir, recursive):
                dirs.append(resource_dir)

        return dirs

    def handle(self, *args, **options):
        warnings.filterwarnings('ignore', '.*',)

        if args:
            selenium_host_and_port = args[0].split(':')
            if len(selenium_host_and_port) > 1:
                (seleniumn_host, selenium_port) = selenium_host_and_port
            else:
                selenium_host = selenium_host_and_port[0]
                selenium_port = 4444
        else:
            selenium_host = "localhost"
            selenium_port = 4444

        apps_to_look_for_tests = []
        if options['apps']:
            apps_to_look_for_tests = options['apps'].replace(' ', '').split(',')

        dir_template = "-d %s"
        action_template = "-A %s"
        page_template = "-P %s"

        pattern = options['pattern']

        testfolder = options['testfolder']

        dirs = self.locate_resource_dirs(testfolder, pattern, apps=apps_to_look_for_tests)

        action_pages_dirs = self.locate_resource_dirs(testfolder, "__init__.py")
        pages_templates = " ".join([page_template % dirname for dirname in action_pages_dirs])
        actions_templates = " ".join([action_template % dirname for dirname in action_pages_dirs])

        dir_templates = " ".join([dir_template % dirname for dirname in dirs])

        extasy_arguments = []

        extasy_arguments.append("-u")
        extasy_arguments.append(options["baseurl"])
        extasy_arguments.extend(dir_templates.split(" "))
        extasy_arguments.extend(actions_templates.split(" "))
        extasy_arguments.extend(pages_templates.split(" "))
        extasy_arguments.append("-p")
        extasy_arguments.append(options["pattern"])
        extasy_arguments.append("-l")
        extasy_arguments.append(options["language"])
        extasy_arguments.append("-w")
        extasy_arguments.append(options["workers"])
        extasy_arguments.append("-v")
        extasy_arguments.append(options["loglevel"])

        if options["supress_warnings"]:
            extasy_arguments.append("--suppresswarnings")

        if options["scenario"]:
            extasy_arguments.append("-s")
            extasy_arguments.append(options["scenario"])

        extasy_arguments.append("-b")
        extasy_arguments.append(options["browser"])
        extasy_arguments.append("selenium.server=%s" % selenium_host)
        extasy_arguments.append("selenium.port=%s" % selenium_port)

        print u'***********************'
        print u'Running EXTasy Tests'
        print u'***********************'

        extasy_arguments = [argument for argument in extasy_arguments if argument != '' and argument is not None]

        ret_code = run_extasy(extasy_arguments)
        raise SystemExit(ret_code)
