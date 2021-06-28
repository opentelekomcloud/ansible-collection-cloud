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
module: rds_instance_info
short_description: Get RDS Instance info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.2"
author: "Artem Goncharov (@gtema)"
description:
  - Get RDS instance info from the OTC or list all instances.
options:
  datastore_type:
    choices: [mysql, postgresql, sqlserver]
    description: Datastore type
    type: str
  instance_type:
    description:
      - Instance type.
    choices: [single, ha, replica]
    type: str
  name:
    description:
      - Name or ID of the RDS instance.
    type: str
  network:
    description: Name or ID of the neutron network
    type: str
  router:
    description: Name or ID of the Neutron router (VPC)
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
rds_instance_info:
    description: List of dictionaries describing RDS instances matching query.
    type: complex
    returned: On Success.
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
'''

EXAMPLES = '''
# Get Instances.
- rds_instance_info:
  register: rds

- rds_instance_info:
    name: my_fake_instance
  register: inst
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class RdsInstanceInfoModule(OTCModule):
    argument_spec = dict(
        datastore_type=dict(type='str',
                            choices=['postgresql', 'mysql', 'sqlserver']),
        name=dict(required=False),
        network=dict(type='str'),
        router=dict(type='str'),
        instance_type=dict(type='str', choices=['single', 'ha', 'replica'])
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        data = []
        query = {}
        ds_t = self.params['datastore_type']
        inst_type = self.params['instance_type']
        if ds_t:
            if ds_t == 'postgresql':
                query['datastore_type'] = 'PostgreSQL'
            elif ds_t == 'mysql':
                query['datastore_type'] = 'MySQL'
            elif ds_t == 'sqlserver':
                query['datastore_type'] = 'SQLServer'
        if self.params['name']:
            query['name'] = self.params['name']
        if inst_type:
            if inst_type == 'single':
                query['type'] = 'Single'
            elif inst_type == 'ha':
                query['type'] = 'Ha'
            elif inst_type == 'replica':
                query['type'] = 'Replica'
        if self.params['network']:
            net = self.conn.network.find_network(
                name_or_id=self.params['network'],
                ignore_missing=True
            )
            if net:
                query['network_id'] = net.id
            else:
                self.exit(
                    changed=False,
                    rds_instances=[],
                    message=('No network with name or id %s found' %
                             self.params['network']))
        if self.params['router']:
            router = self.conn.network.find_router(
                name_or_id=self.params['router'],
                ignore_missing=True
            )
            if router:
                query['router_id'] = router.id
            else:
                self.exit(
                    changed=False,
                    rds_instances=[],
                    message=('No router with name or id %s found' %
                             self.params['router']))
        for raw in self.conn.rds.instances(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            rds_instances=data
        )


def main():
    module = RdsInstanceInfoModule()
    module()


if __name__ == '__main__':
    main()
