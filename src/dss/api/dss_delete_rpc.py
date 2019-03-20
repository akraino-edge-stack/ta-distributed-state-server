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

'''
Delete RPC
Req:
    {
        "domain": <domain name>,
        "name": <the attribute name>
    }

Reply:
{}
'''
class DeleteRPC(object):
    @staticmethod
    def get_name():
        return "delete"

    @staticmethod
    def create_req_payload(domain, name):
        payload = {}
        payload['domain'] = domain
        payload['name'] = name
        return payload

    @staticmethod
    def get_domain_from_req_payload(payload):
        return payload['domain']

    @staticmethod
    def get_name_from_req_payload(payload):
        return payload['name']
