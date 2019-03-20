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
import argparse

from dss.cli import dss_clihandlers

class CLIProcessor:
    def __init__(self, prog):
        self.prog = prog

    def __call__(self, args):
        parser = argparse.ArgumentParser(description='dss CLI', prog=self.prog)
        parser.add_argument('--server', 
                dest='server',
                metavar='SERVER',
                default='/var/run/.dss-server',
                type=str, 
                action='store')

        parser.add_argument('--verbose',
                required=False,
                default=False,
                action='store_true')

        subparsers = parser.add_subparsers()
        handlers = dss_clihandlers.get_handlers_list()
        for handler in handlers:
            handler.init_subparser(subparsers)

        parse_result = parser.parse_args(args)

        parse_result.handler(parse_result)


if __name__ == '__main__':
    processor = CLIProcessor('dsscli')
    args = sys.argv[1:]
    try:
        processor(args)
    except Exception as error:
        print('Got error %s' % str(error))
        sys.exit(1)

