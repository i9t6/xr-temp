#
# Copyright 2020 Cisco Systems, Inc.
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

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'supported_by': 'community',
    'status': ['preview']
}

DOCUMENTATION = """
---
module: demo_module

"""

EXAMPLES = """
- demo_module
"""

RETURN = """
demo module retur
"""

from ansible.module_utils.basic import AnsibleModule
import re

def main():
    """Ansible module to verify IP reachability using Ping RPC over NETCONF."""
    module = AnsibleModule(
        argument_spec=dict(
            var1=dict(type='list', required=True),
        ),
        supports_check_mode=True
    )

    dic_temp = {}
    for d in module.params['var1']:
        try:
            dic_temp[d['key']]
        except:
            dic_temp[d['key']] = [d]
        else:
            dic_temp[d['key']].append(d)

    for key, list in dic_temp.items():
        l=[]
        for dic in list:
            d = {}
            for i,j in dic.items():
                if (('[' in j) or ('{' in j)):
                    d[i]=eval(j)
                    continue
                d[i]=j
            l.append(d)
        dic_temp[key]=l

    module.exit_json(meta=dic_temp)


if __name__ == '__main__':
    """Execute main program."""
    main()

# End of module
