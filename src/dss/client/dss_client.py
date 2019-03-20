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
from dss.api import dss_msg
from dss.api import dss_get_rpc
from dss.api import dss_set_rpc
from dss.api import dss_get_domain_rpc
from dss.api import dss_get_domains_rpc
from dss.api import dss_delete_rpc
from dss.api import dss_delete_domain_rpc

import socket

class Client(object):
    def __init__(self, uds):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        self.server_address = uds
        self.connect = True
        self.fd = None
        self.id = 0

    def _connect(self):
        if self.connect:
            self.sock.connect(self.server_address)
            self.fd = self.sock.makefile('rw')
            self.connect = False

    def _call_rpc(self, msg):
        self.id += 1
        repmsg = dss_msg.Msg()
        try:
            self._connect()
            req = msg.serialize()
            self.sock.sendall(req+'\n')
            rep = self.fd.readline()
        except Exception as exp:
            try:
                self.sock.close()
            except:
                pass
            self.connect = True
            raise dss_error.Error(str(exp))
        repmsg.deserialize(rep)
        return repmsg

    def get(self, domain, name):
        reqpayload = dss_get_rpc.GetRPC.create_req_payload(domain, name)
        reqmsg = dss_msg.Msg(dss_get_rpc.GetRPC.get_name(), self.id, reqpayload)
        repmsg = self._call_rpc(reqmsg)
        reppayload = repmsg.get_payload()
        value = dss_get_rpc.GetRPC.get_value_from_rep_payload(reppayload)
        return value
        
    def get_domain(self, domain):
        reqpayload = dss_get_domain_rpc.GetDomainRPC.create_req_payload(domain)
        reqmsg = dss_msg.Msg(dss_get_domain_rpc.GetDomainRPC.get_name(), self.id, reqpayload)
        repmsg = self._call_rpc(reqmsg)
        reppayload = repmsg.get_payload()
        attrs = dss_get_domain_rpc.GetDomainRPC.get_data_from_rep_payload(reppayload)
        return attrs


    def set(self, domain, name, value):
        reqpayload = dss_set_rpc.SetRPC.create_req_payload(domain, name, value)
        reqmsg = dss_msg.Msg(dss_set_rpc.SetRPC.get_name(), self.id, reqpayload)
        repmsg = self._call_rpc(reqmsg)

    def get_domains(self):
        reqmsg = dss_msg.Msg(dss_get_domains_rpc.GetDomainsRPC.get_name(), self.id, None)
        repmsg = self._call_rpc(reqmsg)
        reppayload = repmsg.get_payload()
        domains = dss_get_domains_rpc.GetDomainsRPC.get_data_from_rep_payload(reppayload)
        return domains

    def delete(self, domain, name):
        reqpayload = dss_delete_rpc.DeleteRPC.create_req_payload(domain, name)
        reqmsg = dss_msg.Msg(dss_delete_rpc.DeleteRPC.get_name(), self.id, reqpayload)
        repmsg = self._call_rpc(reqmsg)

    def delete_domain(self, domain):
        reqpayload = dss_delete_domain_rpc.DeleteDomainRPC.create_req_payload(domain)
        reqmsg = dss_msg.Msg(dss_delete_domain_rpc.DeleteDomainRPC.get_name(), self.id, reqpayload)
        repmsg = self._call_rpc(reqmsg)
