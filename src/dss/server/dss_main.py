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

from dss.server import dss_config
from dss.server import dss_server
from dss.server import dss_logger
from dss.server import dss_rpc_processor
from dss.server import dss_get_handler
from dss.server import dss_get_domain_handler
from dss.server import dss_get_domains_handler
from dss.server import dss_set_handler
from dss.server import dss_delete_handler
from dss.server import dss_delete_domain_handler
from dss.server import dss_plugin_loader

import logging


def _main(config):
    #initialize config
    conf = dss_config.Config(config)

    #initialize logger
    logger = dss_logger.Logger(conf.get_logging_destination(),
            conf.get_verbose(),
            conf.get_logging_level())

    #initialize plugin 
    logging.info('Initializing dss plugin')
    plugin = dss_plugin_loader.DSSPluginLoader(conf)

    #initialize rpc processor
    logging.info('Initializing rpc processor')
    rpcprocessor = dss_rpc_processor.RPCProcessor()

    #adding rpc handlers
    logging.info('Adding RPC handlers')
    gethandler = dss_get_handler.GetHandler(plugin)
    rpcprocessor.add_handler(gethandler)
    getdomainhandler = dss_get_domain_handler.GetDomainHandler(plugin)
    rpcprocessor.add_handler(getdomainhandler)
    getdomainshandler = dss_get_domains_handler.GetDomainsHandler(plugin)
    rpcprocessor.add_handler(getdomainshandler)
    sethandler = dss_set_handler.SetHandler(plugin)
    rpcprocessor.add_handler(sethandler)
    deletehandler = dss_delete_handler.DeleteHandler(plugin)
    rpcprocessor.add_handler(deletehandler)
    deletedomainhandler = dss_delete_domain_handler.DeleteDomainHandler(plugin)
    rpcprocessor.add_handler(deletedomainhandler)

    #initialize tcp server
    logging.info("Initializing tcp server")
    server = dss_server.Server(conf, rpcprocessor)

    logging.info('Waiting for TCP requests')
    server.start()

    logging.info('TCP server stopped')

    logging.info('Exiting, bye bye...')


def main():
    import sys
    import traceback
    import argparse

    parser = argparse.ArgumentParser(description='dss-server',
            prog=sys.argv[0])

    parser.add_argument('--config',
            required=False,
            dest='config',
            metavar='CONFIG',
            default='/etc/dss-server/config.ini',
            help='The dss server configuration file',
            type=str,
            action='store')

    try:
        result = parser.parse_args(sys.argv[1:])
        _main(result.config)
    except Exception as exp:
        print("Failed with error %s" % exp)
        traceback.print_exc()
        sys.exit(1)

    print("Exiting...")
    sys.exit(0)

if __name__ == '__main__':
    main()
