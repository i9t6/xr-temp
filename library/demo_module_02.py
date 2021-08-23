"""
Copyright (c) {{current_year}} Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

AUTHOR(s): Francisco Quiroz <frquiroz@cisco.com>
"""

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'supported_by': 'community',
    'status': ['preview']
}

from ansible.module_utils.basic import AnsibleModule


def main():
    """Ansible module to integrate a summary of the rollback changes in a json dictionary."""
    module = AnsibleModule(
        argument_spec=dict(
            var1=dict(type='dict', required=True)
        ),
        supports_check_mode=True
    )

    dic_temp = module.params['var1']
    for i in dic_temp.keys():
        in_new = module.params['var1'][i]['in_new']
        in_old = module.params['var1'][i]['in_old']
        dic_temp[i]['in_old'] = in_new
        dic_temp[i]['in_new'] = in_old
        out_new = module.params['var1'][i]['out_new']
        out_old = module.params['var1'][i]['out_old']
        dic_temp[i]['out_old'] = out_new
        dic_temp[i]['out_new'] = out_old


    if module.check_mode:
        module.exit_json(changed=False)

    module.exit_json(meta=dic_temp)


if __name__ == '__main__':
    """Execute main program."""
    main()

# End of module
