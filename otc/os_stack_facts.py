#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2018, Artem Goncharov <artem.goncharov@gmail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: os_stack_facts
short_description: Get Heat Stack Facts
extends_documentation_fragment: openstack
version_added: "2.7"
author: "Artem Goncharov (gtema)"
description:
   - Get details of the OpenStack Heat Stack
options:
    name:
      description:
        - Name of the stack that should be searched
      required: true
requirements:
    - "python >= 2.7"
    - "openstacksdk"
'''
EXAMPLES = '''
---
- name: get stack output
  ignore_errors: True
  register: stack_facts
  os_stack_facts:
    name: "{{ stack_name }}"
'''

RETURN = '''
id:
    description: Stack ID.
    type: string
    sample: "97a3f543-8136-4570-920e-fd7605c989d6"
    returned: always

stack:
    description: stack info
    type: complex
    returned: always
    contains:
        action:
            description: Action, could be Create or Update.
            type: string
            sample: "CREATE"
        creation_time:
            description: Time when the action has been made.
            type: string
            sample: "2016-07-05T17:38:12Z"
        description:
            description: Description of the Stack provided in the heat template.
            type: string
            sample: "HOT template to create a new instance and networks"
        id:
            description: Stack ID.
            type: string
            sample: "97a3f543-8136-4570-920e-fd7605c989d6"
        name:
            description: Name of the Stack
            type: string
            sample: "test-stack"
        identifier:
            description: Identifier of the current Stack action.
            type: string
            sample: "test-stack/97a3f543-8136-4570-920e-fd7605c989d6"
        links:
            description: Links to the current Stack.
            type: list of dict
            sample: "[{'href': 'http://foo:8004/v1/7f6a/stacks/test-stack/97a3f543-8136-4570-920e-fd7605c989d6']"
        outputs:
            description: Output returned by the Stack.
            type: list of dict
            sample: "{'description': 'IP address of server1 in private network',
                        'output_key': 'server1_private_ip',
                        'output_value': '10.1.10.103'}"
        parameters:
            description: Parameters of the current Stack
            type: dict
            sample: "{'OS::project_id': '7f6a3a3e01164a4eb4eecb2ab7742101',
                        'OS::stack_id': '97a3f543-8136-4570-920e-fd7605c989d6',
                        'OS::stack_name': 'test-stack',
                        'stack_status': 'CREATE_COMPLETE',
                        'stack_status_reason': 'Stack CREATE completed successfully',
                        'status': 'COMPLETE',
                        'template_description': 'HOT template to create a new instance and networks',
                        'timeout_mins': 60,
                        'updated_time': null}"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.openstack import openstack_full_argument_spec, openstack_module_kwargs, openstack_cloud_from_module
from ansible.module_utils._text import to_native


def main():

    argument_spec = openstack_full_argument_spec(
        name=dict(required=True),
    )

    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec,
                           supports_check_mode=True,
                           **module_kwargs)

    name = module.params['name']

    sdk, cloud = openstack_cloud_from_module(module)
    try:
        stack = cloud.get_stack(name)
        if stack:
            module.exit_json(changed=False,
                             stack=stack,
                             id=stack.id)
        else:
            module.exit_json(changed=False,
                             stack=None,
                             id=None)

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
