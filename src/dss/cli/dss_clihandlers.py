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
import sys
import json

from dss.api import dss_error
from dss.client import dss_client

class VerboseLogger:
    def __call__(self, msg):
        print(msg)

class CLIHandler:
    def __init__(self):
        self.sock = None
        self.verbose_logger = VerboseLogger()

    def _init_api(self, server, verbose):
        logger = None
        if verbose:
            logger = self.verbose_logger

        self.client = dss_client.Client(server)

    def set_handler(self, subparser):
        subparser.set_defaults(handler=self)

    def init_subparser(self, subparsers):
        raise dss_error.Error('Not implemented')

    def __call__(self, args):
        raise dss_error.Error('Not implemented')
    

class CLIGetHandler(CLIHandler):
    def init_subparser(self, subparsers):
        subparser = subparsers.add_parser('get', help='Get the value of an attribute')
        subparser.add_argument('--domain',
                required=True,
                dest='domain',
                metavar='DOMAIN',
                action='store')

        subparser.add_argument('--name',
                required=True,
                dest='name',
                metavar='NAME',
                action='store')

        self.set_handler(subparser)
    
    def __call__(self, args):
        self._init_api(args.server, args.verbose)
        value = self.client.get(args.domain, args.name)
        print('%s' % value)

class CLIGetDomainHandler(CLIHandler):
    def init_subparser(self, subparsers):
        subparser = subparsers.add_parser('get-domain', help='Get the domain attributes')
        subparser.add_argument('--domain',
                required=True,
                dest='domain',
                metavar='DOMAIN',
                action='store')

        self.set_handler(subparser)

    def __call__(self, args):
        self._init_api(args.server, args.verbose)
        attrs = self.client.get_domain(args.domain)
        for name, value in attrs.iteritems():
            print('%s = %s' % (name, value))

class CLIGetDomainsHandler(CLIHandler):
    def init_subparser(self, subparsers):
        subparser = subparsers.add_parser('get-domains', help='Get the domains')
        self.set_handler(subparser)

    def __call__(self, args):
        self._init_api(args.server, args.verbose)
        domains = self.client.get_domains()
        for domain in domains:
            print('%s' % domain)

class CLISetHandler(CLIHandler):
    def init_subparser(self, subparsers):
        subparser = subparsers.add_parser('set', help='Set an attribute to some value')
        subparser.add_argument('--domain',
                required=True,
                dest='domain',
                metavar='DOMAIN',
                action='store')
        subparser.add_argument('--name',
                required=True,
                dest='name',
                metavar='NAME',
                action='store')
        subparser.add_argument('--value',
                required=True,
                dest='value',
                metavar='VALUE',
                action='store')

        self.set_handler(subparser)

    def __call__(self, args):
        self._init_api(args.server, args.verbose)
        self.client.set(args.domain, args.name, args.value)

class CLIDeleteHandler(CLIHandler):
    def init_subparser(self, subparsers):
        subparser = subparsers.add_parser('delete', help='Delete an attribute')
        subparser.add_argument('--domain',
                required=True,
                dest='domain',
                metavar='DOMAIN',
                action='store')
        subparser.add_argument('--name',
                required=True,
                dest='name',
                metavar='NAME',
                action='store')

        self.set_handler(subparser)

    def __call__(self, args):
        self._init_api(args.server, args.verbose)
        self.client.delete(args.domain, args.name)

class CLIDeleteDomainHandler(CLIHandler):
    def init_subparser(self, subparsers):
        subparser = subparsers.add_parser('delete-domain', help='Delete a domain')
        subparser.add_argument('--domain',
                required=True,
                dest='domain',
                metavar='DOMAIN',
                action='store')

        self.set_handler(subparser)

    def __call__(self, args):
        self._init_api(args.server, args.verbose)
        self.client.delete_domain(args.domain)

import sys
import inspect

def get_handlers_list():
    handlers = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if name is not 'CLIHandler':
                if issubclass(obj, CLIHandler):
                    handlers.append(obj())
    return handlers

if __name__ == '__main__':
    handlers = get_handlers_list()
    for handler in handlers:
        print('handler is ', handler)
