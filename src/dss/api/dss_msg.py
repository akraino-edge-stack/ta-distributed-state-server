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

import json
from collections import OrderedDict

from dss.api import dss_error

'''
{
    "name": <msg name>,
    "id": <id>,
    "result": <description>,
    "payload": <data>
}
'''
class Msg(object):
    def __init__(self, name=None, id=None, payload={}, result='OK'):
        self.name = name
        self.id = id
        self.payload = payload
        self.result = result

    def serialize(self):
        msg = OrderedDict([('name', self.name), ('id', self.id), ('result', self.result), ('payload', self.payload) ])
        #msg = {}
        #msg['name'] = self.name
        #msg['id'] = self.id
        #msg['result'] = self.result
        #msg['payload'] = self.payload

        return json.dumps(msg, separators=(',', ':'))

    def deserialize(self, msg):
        data = json.loads(msg, object_pairs_hook=OrderedDict)
        self.name = data['name']
        self.id = data['id']
        self.result = data['result']
        self.payload = data['payload']

        if self.result != 'OK':
            raise dss_error.Error('Request failed with error %s' % self.result)

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_result(self):
        return self.result

    def get_payload(self):
        return self.payload

