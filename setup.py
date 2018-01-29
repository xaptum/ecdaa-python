# Copyright 2017 Xaptum, Inc.
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License

from setuptools import setup
import subprocess
import os
from glob import glob
import distutils.cmd
import setuptools

class AddLibraryPathCommand(distutils.cmd.Command):
    description = 'add path to ecdaa library search path'
    user_options = [('ecdaa-lib=', None, 'library search path for ECDAA library'),]

    def initialize_options(self):
        self.ecdaa_lib = None

    def finalize_options(self):
        self.ecdaa_lib = os.path.abspath(self.ecdaa_lib)

    def run(self):
        if self.ecdaa_lib:
            with open('ecdaa/_extra_search_dir.py', 'w') as out_file:
                init = out_file.write('_other_dirs = [\'' + self.ecdaa_lib + '\']')

setup(
        name = 'ecdaa-python',
        version = '0.6.1',
        description = 'Python wrapper for Elliptic-curve Direct Anonymous Attestation',
        author = 'Xaptum, Inc.',
        author_email = 'sales@xaptum.com',
        license = 'Apache 2.0',
        url = 'https://github.com/xaptum/ecdaa-python',
        packages = ['ecdaa'],
        test_suite = 'nose.collector',
        cmdclass={
            'addlibpath': AddLibraryPathCommand,
        },
        )
