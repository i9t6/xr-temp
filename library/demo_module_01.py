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
            var2=dict(type='list', required=True),
            var3=dict(type='dict', required=True)
        ),
        supports_check_mode=True
    )

    dic_temp = {}
    for i in module.params['var1']:
        flag = 0
        dic_temp[i['item']]={}
        for l in i["stdout_lines"][0]:
            if not "No policy-map" in l:
                for n in ["Mbps-IN","Mbps-OUT","Gbps-IN","Gbps-OUT"]:
                    if n in l:
                        dic_temp[i['item']]['in_old']=re.findall(rf"[0-9]+{n}",l)[0]
            elif 'input' in l:
                dic_temp[i['item']]['in_old']='tbd'
                flag += 1
            elif 'output' in l:
                dic_temp[i['item']]['out_old']='tbd'
                flag += 1
        #dic_temp[i['item']]['flag'] = flag
        if flag == 2:
            dic_temp[i['item']] = 'NA'
    
    for i in module.params['var2']:
        try:
            int=re.findall(r'BE([0-9]+\.[0-9]+)',i)[0]
            #int = re.sub("\s+", ",", i).split(',')[0]
        except:
            continue
        if not dic_temp['Bundle-Ether'+int] == 'NA':
            try:
                dic_temp['Bundle-Ether'+int]['description'] = re.findall(r"\*\*\*\*\* ([\w_\.\s]+)",i)[0]
            except:
                dic_temp['Bundle-Ether'+int]['description'] = "Sin descripcion"
        else:
            dic_temp.pop('Bundle-Ether'+int)

    for key,value in dic_temp.items():
        value['in_new']=module.params['var3'][value['in_old']]
        value['out_new']=module.params['var3'][value['out_old']]

    if module.check_mode:
        module.exit_json(changed=False)

    module.exit_json(meta=dic_temp)

if __name__ == '__main__':
    """Execute main program."""
    main()

# End of module
