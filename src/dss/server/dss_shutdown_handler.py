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

import signal
import logging
from dss.api import dss_error

class ShutdownHandlerBase(object):
    def __init__(self):
        pass

    def shutdown(self):
        raise dss_error.Error('Not implemented')

class ShutdownHandler(object):
    def __init__(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        self.handlers = []

    def add_handler(self, handler):
        logging.info("Added handler %r" % handler)
        self.handlers.append(handler)

    def stop(self, signum, frame):
        for handler in self.handlers:
            logging.info("Calling shutdown on %r" % handler)
            handler.shutdown()
            logging.info("shutdown of %r returned" % handler)
