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
import json
import Queue
import socket
import errno
import time

from dss.server import dss_rpc_processor

class Connection(object):
    def __init__(self, sock, address, rpc_processor):
        self.rpc_processor = rpc_processor
        self.address = address
        self.sock = sock
        self.fd = self.sock.makefile('rw', bufsize=0)
        self.recvbuffer = ""
        logging.info("Received connection from %r %r" % (address, self))

    def fileno(self):
        return self.sock.fileno()

    def send_all(self, rep):
        totalsent = 0
        msglen = len(rep)
        while True:
            try:
                logging.info("Sending %s %r" % (rep, self))
                total = self.sock.send(rep[totalsent:])
                if total == 0:
                    raise RuntimeError('connection closed!')
                totalsent += total
                if totalsent == msglen:
                    logging.info("Sent successfully %r" % self)
                    return
            except socket.error as e:
                if e.argus[0] == errno.EWOULDBLOCK:
                    time.sleep(1)
                else:
                    raise

    def process_recv_buffer(self, data):
        self.recvbuffer += data
        #check for '\n'
        c = self.recvbuffer.count('\n')
        parts = None
        if c:
            parts = self.recvbuffer.split('\n')
            if self.recvbuffer.endswith('\n'):
                self.recvbuffer = ""
            else:
                self.recvbuffer = parts[c]

        for i in range(0, c):
            msg = parts[i]
            logging.debug("Received %s %r" % (msg, self))
            # strip the req
            msg = msg.lstrip('\x00').rstrip('\x00')
            rep = self.rpc_processor.process(msg)
            self.send_all(rep+'\n')




    def recv(self):
	data = None
        try:
            data = self.sock.recv(1024)
            if not data:
                logging.info("Client %r %r disconnected" % (self.address, self))
                return False
            self.process_recv_buffer(data)
        except socket.error as e:
            if e.args[0] == errno.EWOULDBLOCK:
                return True
        except Exception as exp:
            logging.warning('Failed when processing %s got exp %s' % (data, exp))
            return False

        return True

    @staticmethod
    def recv_dgram(sock, req, address, rpc_processor):
        logging.debug("Received %s address is %r" % (req, address))
        try:
            # convert to json structure
            rep = rpc_processor.process(req)
            # add '/n'
            sock.sendto(rep+'\n', address)
        except Exception as exp:
            logging.warning('Failed when processing %s got exp %s' % (req, exp))
