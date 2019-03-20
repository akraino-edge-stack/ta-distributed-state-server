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

import socket
import logging
import select
import errno
import os

from dss.server import dss_connection
from dss.server import dss_config
from dss.server import dss_rpc_processor

class Server(object):
    def __init__(self, conf, rpc_processor):
        self.uds = conf.get_listening_uds()
        self.rpc_processor = rpc_processor
        self.transport_type = conf.get_transport_type()
        self.stopped = False
        if (self.transport_type == 'stream'):
            self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        else:
            self.server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server.setblocking(0)
        self.remove_uds()

    def start(self):
        logging.info("Server listening at %s" % self.uds)
        self.server.bind(self.uds)
        if self.transport_type == 'stream':
            self.server.listen(1)
        inputs = [self.server]
        while not self.stopped:
            try:
                readable, writable, errored = select.select(inputs, [], [])
                for s in readable:
                    if s is self.server:
                        if self.transport_type == 'stream':
                            client, address = self.server.accept()
                            client.setblocking(0) #pylint: disable=no-member
                            conn = dss_connection.Connection(client, address, self.rpc_processor)
                            inputs.append(conn)
                            logging.info("Accepted connection from %r" % address)
                        else:
                            data, address = self.server.recvfrom(4096)
                            dss_connection.Connection.recv_dgram(self.server, data, address, self.rpc_processor)
                    else:
                        result = s.recv()
                        if not result:
                            inputs.remove(s)
            except (SystemExit, KeyboardInterrupt):
                break
            except select.error as e:
                if e.args[0] == errno.EINTR:
                    break
        logging.info("Server stopping")
        self.remove_uds()

    def remove_uds(self):
        try:
            os.unlink(self.uds)
        except OSError:
            pass

    def shutdown(self):
        logging.info("Shutting down tcp server")
        self.stopped = True
