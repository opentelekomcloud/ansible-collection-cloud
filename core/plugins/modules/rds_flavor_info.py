#!/usr/bin/env python
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

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: rds_flavor_info
short_description: Get RDS flavor info
extends_documentation_fragment: openstack
version_added: "2.9"
author: "Artem Goncharov (@gtema)"
description:
  - Get RDS datastore info from the OTC.
options:
  datastore:
    description:
      - Name of the database (datastore type).
    required: true
    choices: [mysql, postgresql, sqlserver]
    default: postgresql
  version:
    description:
      - Datastore version
    required: true
  instance_mode:
    description:
      - Instance mode to filter results
    choices: [single, replicy, ha]
requirements: ["openstacksdk", "otcextensions"]
'''

# TODO: describe proper output
RETURN = '''
rds_flavors:
    description: List of dictionaries describing RDS flavors
    type: complex
    returned: On Success.
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        name:
            description: Name (version) of the datastore.
            type: str
            sample: "10.0"
'''

EXAMPLES = '''
# Get a flavor.
- rds_flavor_info:
    datastore: "postgresql"
    version: "10.0"
  register: rds_flavor_info
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.opentelekomcloud.core.plugins.module_utils.otc \
    import openstack_full_argument_spec, \
    openstack_module_kwargs, openstack_cloud_from_module


def main():
    argument_spec = openstack_full_argument_spec(
        name=dict(required=False),
        datastore=dict(required=True, choices=['mysql', 'postgresql',
                                               'sqlserver']),
        version=dict(required=True),
        instance_mode=dict(choices=['single', 'replica', 'ha'])
    )
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(
        argument_spec=argument_spec,
        **module_kwargs)
    sdk, cloud = openstack_cloud_from_module(module)

    datastore = module.params['datastore']
    version = module.params['version']
    instance_mode_filter = module.params['instance_mode']

    try:
        data = []
        for raw in cloud.rds.flavors(datastore_name=datastore,
                                     version_name=version):
            if (instance_mode_filter
                    and raw.instance_mode != instance_mode_filter):
                # Skip result
                continue
            dt = raw.to_dict()
            dt.pop('location')
            dt.pop('id')
            data.append(dt)

        module.exit_json(
            changed=False,
            rds_flavors=data
        )

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)


if __name__ == "__main__":
    main()
