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


class Error(Exception):
    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def __str__(self):
        return '%s' % self.description

def handle_exceptions(func):
    def wrapper(self, *arg, **kwargs):
        try:
            return func(self, *arg, **kwargs)
        except Error as exp:
            raise
        except Exception as exp:
            raise Error(str(exp))
    return wrapper


if __name__ == '__main__':
    class Test:
        @handle_exceptions
        def test_raise(self):
            raise Exception('Some error')

    try:
        test = Test()
        test.test_raise()
    except Error as exp:
        print('Got exception %s' % exp)

    try:
        raise Error(sys.argv[1])
    except Error as error:
        print('Got exception %s' % str(error))
    except Exception as exp:
        print('Got exception %s' % str(exp))
