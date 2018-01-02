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

def _set_up_library():
    try:
        import _extra_search_dir
        extra_dirs = _extra_search_dir._other_dirs
    except Exception:
        extra_dirs = []

    from ecdaa.wrapper import set_functions_from_library
    set_functions_from_library(extra_dirs)

_set_up_library()

from ecdaa.wrapper import *
