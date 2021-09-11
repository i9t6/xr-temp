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
import re

def main():
    """Ansible module to verify create a text file with configuration for a XR router."""
    module = AnsibleModule(
        argument_spec = dict(
            var1 = dict(type ='dict', required=True),
            var2 = dict(type ='str', required=True)
        ),
        supports_check_mode=True
    )

    f= open( f"{module.params['var2']}.cfg", "w")
    for old_map, new_map in module.params['var1'].items():
        if not "tbd" in old_map:
            speed = re.findall(r'([0-9]+)',new_map)[0]
            speed_var = re.findall(r'[0-9]+(.)bps',new_map)[0].lower()
            pm_var = f"""policy-map {new_map}
 class class-default
  police rate {speed} {speed_var}bps
   conform-action set precedence 0
   exceed-action drop
  !
!
 end-policy-map
!
"""
            f.write(pm_var)
    f.close()
    if module.check_mode:
        module.exit_json(changed=False)

    module.exit_json(meta=f"{module.params['var2']}.cfg")


if __name__ == '__main__':
    """Execute main program."""
    main()

# End of module
