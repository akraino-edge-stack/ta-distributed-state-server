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
from dss.server import dss_rpc_handler
from dss.server import dss_plugin_loader
from dss.api import dss_get_domain_rpc

class GetDomainHandler(dss_rpc_handler.RPCHandler):
    def __init__(self, plugin):
        super(GetDomainHandler, self).__init__(dss_get_domain_rpc.GetDomainRPC.get_name())
        self.plugin = plugin

    def handle(self, reqpayload):
        domain = dss_get_domain_rpc.GetDomainRPC.get_domain_from_req_payload(reqpayload)
        logging.info("Handling getting domain %s" % domain)
        attrs = self.plugin.get_domain(domain)
        logging.info("attrs = %r" % attrs)
        reppayload = dss_get_domain_rpc.GetDomainRPC.create_rep_payload(attrs)
        return reppayload
