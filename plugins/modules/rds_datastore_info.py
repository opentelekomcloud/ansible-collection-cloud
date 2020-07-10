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
    choices: [mysql, postgresql, sqlserver]
    default: postgresql
    type: str
  name:
    description: datastore name
    type: str
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


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class RdsDatastoreInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
        datastore=dict(choices=['mysql', 'postgresql', 'sqlserver'],
                       default='postgresql'),
    )

    def run(self):
        datastore = self.params['datastore']

        data = []
        for raw in self.conn.rds.datastores(database_name=datastore):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit_json(
            changed=False,
            rds_datastores=data
        )


def main():
    module = RdsDatastoreInfoModule()
    module()


if __name__ == "__main__":
    main()
