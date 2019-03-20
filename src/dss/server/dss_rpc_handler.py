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

from dss.api import dss_error

class RPCHandler(object):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    '''
    handle request
    Arguments:
    req: request payload

    return reply payload
    raise oha_error.Error in-case of error
    '''
    def handle(self, reqmsg):
        raise dss_error.Error('Not implemented')

