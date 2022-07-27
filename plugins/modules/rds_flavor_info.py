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

DOCUMENTATION = '''
---
module: rds_flavor_info
short_description: Get RDS flavor info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Artem Goncharov (@gtema)"
description:
  - Get RDS flavor info from the OTC.
options:
  name:
    description: flavor name
    type: str
  datastore:
    description:
      - Name of the database (datastore type).
    choices: [mysql, postgresql, sqlserver]
    type: str
  version:
    description:
      - Datastore version
    type: str
  instance_mode:
    description:
      - Instance mode to filter results
    choices: [single, replica, ha]
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

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
            sample: "10"
        ram:
            description: Quantity of RAM Gigabytes
            type: int
            sample: 128
        spec_code:
            description: Name of the flavor specification
            type: str
            sample: "rds.mysql.c3.15xlarge.2.ha"
        vcpus:
            description: Quantity of available virtual CPUs
            type: str
            sample: "60"
'''

EXAMPLES = '''
# Get a flavor.
- rds_flavor_info:
    datastore: "postgresql"
    version: "10"
  register: rds_flavor_info
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class RdsFlavorModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
        datastore=dict(choices=['mysql', 'postgresql', 'sqlserver']),
        version=dict(required=False),
        instance_mode=dict(choices=['single', 'replica', 'ha'])
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        datastore = self.params['datastore']
        version = self.params['version']
        instance_mode_filter = self.params['instance_mode']

        data = []
        for raw in self.conn.rds.flavors(datastore_name=datastore,
                                         version_name=version):
            if (instance_mode_filter
                    and raw.instance_mode != instance_mode_filter):
                # Skip result
                continue
            dt = raw.to_dict()
            dt.pop('location')
            dt.pop('id')
            data.append(dt)

        self.exit_json(
            changed=False,
            rds_flavors=data
        )


def main():
    module = RdsFlavorModule()
    module()


if __name__ == "__main__":
    main()
