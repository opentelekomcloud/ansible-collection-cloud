#!/usr/bin/python
# Copyright: T-Systems International GmbH, Open Telekom Cloud
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
module: os_security_group_facts
short_description: Retrieve facts about OpenStack security group
version_added: "1.0"
author: "T. Schreiber"
description:
    - Retrieve facts about OpenStack security group.
notes:
    - Return value: security_group variable
requirements:
    - "python >= 2.7"
    - "openstacksdk"
options:
   security_group:
     description:
        - Name or ID of the security group
     required: false
extends_documentation_fragment: openstack
'''

EXAMPLES = '''
# Show specific security group
- name: Show specific security group
  os_security_group_facts:
    auth:
      auth_url: https://identity.example.com
      username: user
      password: password
      project_name: project
    security_group: my-security_group

- name: Show openstack facts
  debug:
    var: openstack_security_group

# Show all available Openstack security groups
- name: Show all available Openstack security groups
  os_security_group_facts:

- name: Show security groups
  debug:
    var: openstack_security_group
'''

RETURN = '''
openstack_security_group:
    description: lists security group facts
    returned: always, can be null
    type: complex
    contains:
        created_at:
            description: Timestamp when security grouphas been created
            returned: success
            type: str
        description:
            description: Description regarding the security group
            returned: success
            type: str
        location:
            description: Details about security group location
            returned: success
            type: dict
        name:
            description: Name of the security group
            returned: success
            type: str
        project_id:
            description: ID of the associated project
            returned: success
            type: str
        properties:
            description: Timestamps of creation and update
            returned: success
            type: dict
        security_group_rules:
            description: List of associated sg rules
            returned: success
            type: array
        updated_at:
            description: Timestamp of latest update
            returned: success
            type: str
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.openstack import openstack_full_argument_spec, openstack_module_kwargs, openstack_cloud_from_module


def main():

    argument_spec = openstack_full_argument_spec(
        security_group=dict(required=False),
    )
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)

    sdk, cloud = openstack_cloud_from_module(module)
    try:
        if module.params['security_group']:
            security_group = cloud.get_security_group(module.params['security_group'])
            module.exit_json(changed=False, ansible_facts=dict(
                openstack_security_group=security_group))
        else:
            security_groups = cloud.list_security_groups()
            module.exit_json(changed=False, ansible_facts=dict(
                openstack_security_group=security_groups))

    except sdk.exceptions.OpenStackCloudException as exception:
        module.fail_json(msg=str(exception))


if __name__ == '__main__':
    main()
