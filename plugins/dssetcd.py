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

from dss.api import dss_plugin
from dss.api import dss_error

import ConfigParser
import logging
import os
import etcd

class dssetcd(dss_plugin.DSSPlugin):
    """
    Read the ini file. The structure is as follows
    [etcd]
    host = controller-1
    port = 2380
    """
    def __init__(self, config_file):
        super(dssetcd, self).__init__(config_file)
        self.host = None
        self.port = None
        self.connected = False
        try:
            config = ConfigParser.ConfigParser()
            config.read([config_file])
            self.host = config.get('etcd', 'host')
            self.port = int(config.get('etcd', 'port'))
            self._connect()
        except Exception as exp:
            pass


    def _connect(self):
        try:
            self.client = etcd.Client(self.host, self.port)
            self.connected = True
        except Exception as exp:
            self.connected = False
            raise dss_error.Error(exp)

    def get(self, domain, name):
        if not self.connected:
            self._connect()

        try:
            value = self.client.read('/'+domain+'/'+name)
            return value.value
        except Exception as exp:
            raise dss_error.Error(exp)

    def get_domain(self, domain):
        if not self.connected:
            self._connect()

        ret = {}
        try:
            values = self.client.read('/'+domain)
            for value in values._children:
                if 'dir' not in value and 'key' in value:
                    k = value['key']
                    n = k.split('/')[2]
                    v = value['value']
                    ret[n] = v
            return ret
        except Exception as exp:
            raise dss_error.Error(exp)

    def get_domains(self):
        if not self.connected:
            self._connect()
        ret = []
        try:
            domains = self.client.read('/')
            for domain in domains._children:
                if 'dir' in domain and domain['dir'] and 'key' in domain:
                    d = domain['key']
                    v = d.split('/')[1]
                    ret.append(v)
            return ret
        except Exception as exp:
            raise dss_error.Error(exp)

    def set(self, domain, name, value):
        if not self.connected:
            self._connect()

        try:
            self.client.write('/'+domain+'/'+name, value)
        except Exception as exp:
            raise dss_error.Error(exp)

    def delete(self, domain, name):
        if not self.connected:
            self._connect()

        try:
            self.client.delete('/'+domain+'/'+name)
        except Exception as exp:
            raise dss_error.Error(exp)

    def delete_domain(self, domain):
        if not self.connected:
            self._connect()

        try:
            self.client.delete('/'+domain, recursive=True, dir=True)
        except Exception as exp:
            raise dss_error.Error(exp)
