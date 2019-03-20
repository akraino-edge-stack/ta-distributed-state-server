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

class dssfile(dss_plugin.DSSPlugin):
    """
    Read the ini file. The structure is as follows
    [default]
    directory = <directory>
    """
    def __init__(self, config_file):
        super(dssfile, self).__init__(config_file)
        self.directory = None
        try:
            config = ConfigParser.ConfigParser()
            config.read([config_file])
            self.directory = config.get('default', 'directory')
        except Exception as exp:
            raise dss_error.Error('Failed to parse configuration, got error %s' % exp)

        if not os.path.isdir(self.directory):
            raise dss_error.Error('%s is not a valid directory name' % self.directory)

    def read_file(self, domain):
        filename = self.directory + '/' + domain
        if not os.path.isfile(filename):
            raise dss_error.Error('Key not found %s' % domain)

        try:
            with open(filename) as f:
                return f.read().splitlines()
        except Exception as exp:
            raise dss_error.Error('Failed with error %s' % exp)

    def write_file(self, domain, lines):
        filename = self.directory + '/' + domain
        try:
            with open(filename, 'w') as f:
                for line in lines:
                    f.write(line+'\n')
        except Exception as exp:
            raise dss_error.Error('Failed with error %s' % exp)

    def get(self, domain, name):
        lines = self.read_file(domain)
        try:
            for line in lines:
                index=line.find('=')
                part0 = line[:index]
                part1 = line[index+1:]
                if name == part0:
                    return part1
        except Exception as exp:
            raise dss_error.Error('Failed with error %s' % exp)

        raise dss_error.Error('Key not found %s/%s' % (domain, name))

    def get_domain(self, domain):
        lines = self.read_file(domain)
        ret = {}
        for line in lines:
            index=line.find('=')
            part0 = line[:index]
            part1 = line[index+1:]
            ret[part0] = part1
        return ret

    def get_domains(self):
        ret = []
        try:
            entries = os.listdir(self.directory)
            for entry in entries:
                filename = self.directory + '/' + entry
                if os.path.isfile(filename):
                    ret.append(entry)
            if not ret:
                raise dss_error.Error('No domains found')

            return ret
        except Exception as exp:
            raise dss_error.Error('Failed with error %s' % exp)

    def set(self, domain, name, value):
        filename = self.directory + '/' + domain
        lines = []
        if os.path.isfile(filename):
            lines = self.read_file(domain)
        try:
            found = False
            for index, line in enumerate(lines):
                i=line.find('=')
                part0 = line[:i]
                part1 = line[i+1:]
                if part0 == name:
                    found = True
                    lines[index] = name+'='+value
                    break
            if not found:
                lines.append(name+'='+value)
            self.write_file(domain, lines)
        except Exception as exp:
            raise dss_error.Error('Failed with error %s' % exp)

    def delete(self, domain, name):
        lines = self.read_file(domain)
        found_index = -1
        try:
            for index, line in enumerate(lines):
                i=line.find('=')
                part0 = line[:i]
                part1 = line[i+1:]
                if part0 == name:
                    found_index = index
                    break
            if found_index != -1:
                del lines[found_index]
                self.write_file(domain, lines)
        except Exception as exp:
            raise dss_error.Error('Failed with error %s' % exp)

        if found_index == -1:
            raise dss_error.Error('%s/%s not found' % (domain, name))

    def delete_domain(self, domain):
        filename = self.directory + '/' + domain
        if os.path.isfile(filename):
            os.remove(filename)
        else:
            raise dss_error.Error('Invalid domain %s' % domain)
