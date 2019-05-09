#! /usr/bin/python
#
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
import traceback

from dss.cli import dss_cliprocessors

def main():
    try:
        processor = dss_cliprocessors.CLIProcessor('dsscli')
        args = sys.argv[1:]
        processor(args)
    except Exception as exp:
        print('Failed with error: %s' % str(exp))
        #traceback.print_exc()
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
