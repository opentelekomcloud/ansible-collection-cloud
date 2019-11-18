#!/usr/bin/python
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
module: rds_datastore_info
short_description: Get supported RDS datastore versions
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
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
rds_datastore_versions:
    description: List of dictionaries describing RDS datastore version.
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
# Get datastore versions.
- rds_datastore_info:
    datastore: "postgresql"
  register: rds
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
    )
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(
        argument_spec=argument_spec,
        **module_kwargs)
    sdk, cloud = openstack_cloud_from_module(module)

    datastore = module.params['datastore']

    try:
        data = []
        for raw in cloud.rds.datastores(database_name=datastore):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        module.exit_json(
            changed=False,
            rds_datastores=data
        )

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)


if __name__ == "__main__":
    main()
