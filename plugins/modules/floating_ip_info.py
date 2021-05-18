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
module: floating_ip_info
short_description: Get information about floating ips
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.1"
author: "Yustina Kvrivishvili (@)"
description:
  - Get a generator of floating ips info from the OTC.
options:
  description:
    description:
      - The description of a floating IP.
    type: str
  fixed_ip_address:
    description:
      - The fixed IP address associated with a floating IP address.
    type: str
  floating_ip_address:
    description:
      -  The IP address of a floating IP.
    type: str
  floating_network_id:
    description:
      - The ID of the network associated with a floating IP.
    type: str
  port_id:
    description:
      - The ID of the port to which a floating IP is associated.
    type: str
  project_id:
    description:
      - The ID of the project a floating IP is associated with.
    type: str
  router_id:
    description:
      - The ID of an associated router.
    type: str
  status:
    description:
      - The status of a floating IP, which can be ``ACTIVE``or ``DOWN``.
    choices: ['ACTIVE', 'DOWN']
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
floating_ips:
  description: The VPC peering connection object list.
  type: complex
  returned: On Success.
  contains:
    id:
      description: The VPC peering connection ID.
      type: str
      sample: "4dae5bac-0925-4d5b-add8-cb6667b8"
    name:
      description: The VPC peering connection name.
      type: str
      sample: "vpc-peering1"
    status:
      description: The VPC peering connection status.
      type: str
      sample: "ACTIVE"
    request_vpc_info:
      description: Information about the local VPC.
      type: dict
      sample: "{tenant_id: 76889f64a23945ab887012be95acf, vpc_id: 4dae5bac-0925-4d5b-add8-cb6667b8}"
    accept_vpc_info:
      description: Information about the peer VPC.
      type: dict
      sample: "{tenant_id: 968u64a23945ab887012be95acf, vpc_id: 7dau5bac-0925-4d5b-add8-cb6667b8}"
    description:
      description: Provides supplementary information about the VPC peering connection.
      type: str
      sample: ""
    created_at:
      description: The time (UTC) when the VPC peering connection is created.
      type: str
      sample: "2020-09-13T20:37:01"
    updated_at:
      description: Specifies the time (UTC) when the VPC peering connection is updated.
      type: str
      sample: "2020-09-13T20:38:02"
'''

EXAMPLES = '''
# 
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class FloatingIPInfoModule(OTCModule):
    argument_spec = dict(
        description=dict(required=False),
        fixed_ip_address=dict(required=False),
        floating_ip_address=dict(required=False),
        floating_network_id=dict(required=False),
        port_id=dict(required=False),
        project_id=dict(required=False),
        router_id=dict(required=False),
        status=dict(required=False, choices=['ACTIVE', 'DOWN']),
    )

    def run(self):

        description = self.params['description']
        fixed_ip_address = self.params['fixed_ip_address']
        floating_ip_address = self.params['floating_ip_address']
        floating_network_id = self.params['floating_network_id']
        port_id = self.params['port_id']
        project_id = self.params['project_id']
        router_id = self.params['router_id']
        status = self.params['status']

        data = []
        query = {}
        if description:
            query['description'] = description
        if fixed_ip_address:
            query['fixed_ip_address'] = fixed_ip_address
        if floating_ip_address:
            query['floating_ip_address'] = floating_ip_address
        if floating_network_id:
            floating_network_id = floating_network_id
        if port_id:
            query['port_id'] = port_id
        if project_id:
            query['project_id'] = project_id
        if router_id:
            query['router_id'] = router_id
        if status:
            status = status

        for raw in self.conn.network.ips(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit_json(
            changed=False,
            vpc_peerings=data
        )


def main():
    module = FloatingIPInfoModule()
    module()


if __name__ == '__main__':
    main()
