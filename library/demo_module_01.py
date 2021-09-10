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
            var3=dict(type='list', required=True),
            var4=dict(type='dict', required=True)
        ),
        supports_check_mode=True
    )

    dic_temp = {}
    for i in module.params['var1']:
        try:
            int_var=re.match(r'Bundle-Ether[0-9]+\.[0-9]+',i).group(0) 
        except:
            continue
        else:
            dic_temp[int_var]={}

    for i in module.params['var2']:
        for l in i["stdout_lines"][0]:
            if "Mbps-IN" in l:
                dic_temp[i['item']]['in_old']=re.findall(r"[0-9]+Mbps-IN",l)[0]
            elif "Mbps-OUT" in l:
                dic_temp[i['item']]['out_old']=re.findall(r"[0-9]+Mbps-OUT",l)[0]
            elif "Gbps-IN" in l:
                dic_temp[i['item']]['in_old']=re.findall(r"[0-9]+Gbps-IN",l)[0]
            elif "Gbps-OUT" in l:
                dic_temp[i['item']]['out_old']=re.findall(r"[0-9]+Gbps-OUT",l)[0]
            elif "No policy-map" in l:
                if 'input' in l:
                    dic_temp[i['item']]['in_old']='tbd'
                elif 'output' in l:
                    dic_temp[i['item']]['out_old']='tbd'
    
    for i in module.params['var3']:
        try:
            int=re.findall(r'BE([0-9]+\.[0-9]+)',i)[0]
            #int = re.sub("\s+", ",", i).split(',')[0]
        except:
            continue
        try:
            dic_temp['Bundle-Ether'+int]['description'] = re.findall(r"\*\*\*\*\* ([\w_\.\s]+)",i)[0]
        except:
            dic_temp['Bundle-Ether'+int]['description'] = "Sin descripcion"

    for i in dic_temp.keys():
        dic_temp[i]['in_new']=module.params['var4'][dic_temp[i]['in_old']]
        dic_temp[i]['out_new']=module.params['var4'][dic_temp[i]['out_old']]




    if module.check_mode:
        module.exit_json(changed=False)

    module.exit_json(meta=dic_temp)


if __name__ == '__main__':
    """Execute main program."""
    main()

# End of module
