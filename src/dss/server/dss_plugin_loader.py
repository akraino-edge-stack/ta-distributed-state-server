# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#
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

import os
import imp
import sys
import logging
from dss.api import dss_error
from dss.server import dss_config

class DSSPluginLoader(object):
    def __init__(self, config):
        try:
            plugin_file = config.get_plugin()
            location = os.path.dirname(plugin_file)
            pluginname = os.path.basename(plugin_file).replace(".py", "")
            sys.path.append(location)
            self.plugin = None
            self._load_plugin(pluginname, config.get_plugin_config())
        except Exception as exp:
            raise dss_error.Error(str(exp))

    def _load_plugin(self, pluginname, configfile):
        logging.info('Loading plugin %s' % pluginname)
        fp, pathname, description = imp.find_module(pluginname)
        try:
            pluginmodule = imp.load_module(pluginname, fp, pathname, description)
            class_name = getattr(pluginmodule, pluginname)
            self.plugin = class_name(configfile)
        except Exception as exp:
            logging.error('Failed to load plugin %s, got exp %s' % (pluginname, str(exp)))
            raise
        finally:
            if fp:
                fp.close()

    def set(self, domain, name, value):
        logging.info("Setting %s/%s to %s" % (domain, name, value))
        self.plugin.set(domain, name, value)

    def get(self, domain, name):
        logging.info("Getting attribute %s/%s" % (domain, name))
        value = self.plugin.get(domain, name)
        logging.info("Value of %s/%s is %s" % (domain, name, value))
        return value

    def get_domain(self, domain):
        logging.info("Getting the attributes of domain %s" % domain)
        attrs = self.plugin.get_domain(domain)
        return attrs

    def get_domains(self):
        logging.info("Getting the domains")
        domains = self.plugin.get_domains()
        return domains

    def delete(self, domain, name):
        logging.info("Deleting %s/%s" % (domain, name))
        self.plugin.delete(domain, name)

    def delete_domain(self, domain):
        logging.info("Delete domain %s" % domain)
        self.plugin.delete_domain(domain)

if __name__ == '__main__':
    pl = DSSPluginLoader("configfile")
    pl.set("domain1", "name1", "value1")
