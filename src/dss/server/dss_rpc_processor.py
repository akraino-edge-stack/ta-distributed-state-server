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

import logging
from dss.api import dss_msg
from dss.server import dss_rpc_handler

class RPCProcessor(object):
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    def get_handler(self, name):
        for handler in self.handlers:
            if handler.get_name() == name:
                return handler
        return None

    '''
    process the request
    Arguments:
    reqstring the request string
    Return:
    repstring the reply string
    '''
    def process(self, reqstring):
        reppayload = {}
        result = 'OK'
        id = None
        name = None
        try:
            # deserialize req string
            reqmsg = dss_msg.Msg()
            reqmsg.deserialize(reqstring)
            name = reqmsg.get_name()

            logging.info("Processing %s" % name)

            id = reqmsg.get_id()

            # find suitable handler
            handler = self.get_handler(name)

            # process message
            reppayload = handler.handle(reqmsg.get_payload())
        except Exception as exp:
            logging.warning('Failed when processing %s' % reqstring)
            result = str(exp)

        repmsg = dss_msg.Msg(name, id, reppayload, result)

        return repmsg.serialize()
