# vim: set fileencoding=utf-8 :
#
# Copyright (c) 2013 Daniel Truemper <truemped at googlemail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
from __future__ import absolute_import, division, print_function, with_statement

import sys
if sys.version_info > (2, 7):
    from unittest import TestCase
else:
    from unittest2 import TestCase

from tornado.web import Application, RequestHandler

from supercell.api.environment import Environment


class EnvironmentTest(TestCase):

    def test_simple_app_creation(self):
        env = Environment()
        app = env.application
        self.assertIsInstance(app, Application)
        self.assertEqual(len(app.handlers), 0)

    def test_config_file_paths(self):
        env = Environment()
        self.assertEqual(len(env.config_file_paths), 0)

    def test_add_handler(self):
        env = Environment()
        self.assertEqual(len(env._handlers), 0)

        class MyHandler(RequestHandler):
            def get(self):
                self.write({'ok': True})

        env.add_handler('/test', MyHandler, {})

        self.assertEqual(len(env._handlers), 1)

        app = env.application
        self.assertEqual(len(app.handlers), 1)
        (host_pattern, [spec]) = app.handlers[0]
        self.assertEqual(host_pattern.pattern, '.*$')
        self.assertEqual(spec.regex.pattern, '/test$')
        self.assertEqual(spec.handler_class, MyHandler)