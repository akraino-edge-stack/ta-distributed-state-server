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

class DSSPlugin(object):
    def __init__(self, config_file):
        self.config_file = config_file


    def get(self, domain, name):
        """get the value associated with an attribute

           Arguments:

           domain: The domain name.

           name: The attribute name.

           Return:

           The value 

           Raise:

           dss_error.Error can be raised in-case of an error.
        """
        raise dss_error.Error('Not implemented')

    def set(self, domain, name, value):
        """set an attribute to some value

           Arguments:

           domain: The domain name.

           name: The attribute name.

           value: The value.

           Raise:

           dss_error.Error can be raised in-case of an error.
        """
        raise dss_error.Error('Not implemented')

    def get_domain(self, domain):
        """Get all the attributes in a domain

           Arguments:
            
           Return: A dictionary.

           Raise:

           dss_error.Error can raised in case of an error
        """
        raise dss_error.Error('Not implemented')

    def get_domains(self):
        """Get the domains list

           Arguments:
            
           Return: A list containing domain names

           Raise:

           dss_error.Error can raised in case of an error
        """
        raise dss_error.Error('Not implemented')

