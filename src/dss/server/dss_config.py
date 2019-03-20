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

import ConfigParser
from dss.api import dss_error

SERVER_SECTION = "server"
PLUGIN_SECTION = "plugin"
DEFAULT_CONFIG_FILE="/etc/dss/dss-server/config.ini"

class Config(object):
    """
    Read the ini file. The structure of the file is as follows:
    [server]
    logging_level = info
    logging_destination = console
    verbose = true
    listening_uds = /var/run/.dss-server
    transport_type = dgram
    [plugin]
    plugin = /opt/dss-server/etcd.py
    config = /etc/dss-server/etcd.ini
    """
    
    def __init__(self, config_file = DEFAULT_CONFIG_FILE):
        try:
            # server
            self.logging_level = None
            self.logging_destination = None
            self.verbose = None
            self.listening_uds = None
            self.transport_type = None

            # plugin
            self.plugin = None
            self.plugin_config = None

            config = ConfigParser.ConfigParser()
            config.read([config_file])

            self.logging_level = config.get(SERVER_SECTION, "logging_level")
            self.logging_destination = config.get(SERVER_SECTION, "logging_destination")
            self.verbose = config.get(SERVER_SECTION, "verbose")
            self.listening_uds = config.get(SERVER_SECTION, "listening_uds")
            self.transport_type = config.get(SERVER_SECTION, "transport_type")

            self.plugin = config.get(PLUGIN_SECTION, "plugin")
            self.plugin_config = config.get(PLUGIN_SECTION, "config")


        except Exception as exp:
            raise dss_error.Error(str(exp))

    def get_logging_level(self):
        return self.logging_level

    def get_logging_destination(self):
        return self.logging_destination

    def get_verbose(self):
        return self.verbose

    def get_listening_uds(self):
        return self.listening_uds

    def get_plugin(self):
        return self.plugin

    def get_plugin_config(self):
        return self.plugin_config

    def get_transport_type(self):
        return self.transport_type


if __name__ == "__main__":
    import sys
    try:
        config = Config(sys.argv[1])
    except dss_error.Error as exp:
        print("Got exception %s" % exp)
