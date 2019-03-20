# Copyright 2019 Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
import logging
import logging.handlers

from dss.api import dss_error

class Logger:

    levels = {'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.error}

    DEST_CONSOLE = 1
    DEST_SYSLOG = 2
    dests = {'console': DEST_CONSOLE,
            'syslog': DEST_SYSLOG}

    def __init__(self, dest, verbose, level):
        self.verbose = verbose
        self.dest = Logger.str_to_dest(dest)
        self.level = Logger.str_to_level(level)
        self.init()

    def init(self):
        args = {}

        if self.level not in Logger.levels.values():
            raise dss_error.Error('Invalid level value, possible values are %s' % str(Logger.levels))

        if self.dest not in Logger.dests.values():
            raise dss_error.Error('Invalid destination value, possible values are %s' % str(Logger.dests))

        if self.verbose:
            if self.dest is Logger.DEST_CONSOLE:
                args['format'] = '[%(asctime)s %(levelname)7s %(module)s(%(lineno)3s)] %(message)s'
            else:
                args['format'] = '[%(module)s(%(lineno)3s)] %(message)s'
        else:
            args['format'] = '%(message)s'

        if self.dest is Logger.DEST_CONSOLE:
            args['stream'] = sys.stdout
        elif self.dest is Logger.DEST_SYSLOG:
            logging.getLogger('').addHandler(logging.handlers.SysLogHandler(address='/dev/log'))

        args['level'] = self.level
        logging.basicConfig(**args)

    def set_level(self, level):
        self.level = Logger.str_to_level(level)
        self.init()

    def set_dest(self, dest):
        self.dest = Logger.str_to_dest(dest)
        self.init()

    @staticmethod
    def str_to_level(level):
        ret = None
        try:
            ret = Logger.levels[level]
        except KeyError as exp:
            raise dss_error.Error('Invalid log level, possible values %s' % str(Logger.levels.keys()))
        return ret

    @staticmethod
    def str_to_dest(dest):
        ret = None
        try:
            ret = Logger.dests[dest]
        except KeyError as exp:
            raise dss_error.Error('Invalid destination, possible values %s' % str(Logger.dests.keys()))
        return ret

    @staticmethod
    def level_to_str(level):
        for key, value in Logger.levels.iteritems():
            if value is level:
                return key
        return None

    @staticmethod
    def dest_to_str(dest):
        for key, value in Logger.dests.iteritems():
            if value is dest:
                return key
        return None

if __name__ == '__main__':
    dest = Logger.str_to_dest('console')
    level = Logger.str_to_level('debug')
    logger = Logger(dest, True, level)
    world='world'
    logging.error('hello %s!' % world)
    logging.warn('hello %s!' % world)
    logging.info('hello %s!' % world)
    logging.debug('hello %s!' % world)
