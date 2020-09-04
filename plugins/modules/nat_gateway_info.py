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
module: nat_gateway_info
short_description: Get NAT gateways
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.4"
author: "Tino Schreiber (@tischrei)"
description:
  - Get NAT gateway info from the OTC.
options:
  admin_state_up:
    description:
      - NAT gateway state.
    type: bool
  created_at:
    description:
      - Creation time of the NAT gateway
    type: str
  description:
    description:
      - Description of the NAT gateway
    type: str
  id:
    description:
      - ID of the NAT gateway.
    type: str
  internal_network_id:
    description:
      - Network ID where the NAT gateway is attached to.
    type: str
  name:
    description:
      - Name of the NAT gateway.
    type: str
  project_id:
    description:
      - Filters NAT gateways of the project ID.
    type: str
  router_id:
    description:
      - ID of the router where the NAT gateway is attached.
    type: str
  spec:
    description:
      - Specifies the type of the NAT gateway. 1 (small 10.000 connections),
        2 (medium 50.000 connections), 3 (large 200.000 connections), 4
        (extra-large 1.000.000 connections)
    type: str
    choices: ["1", "2", "3", "4"]
  status:
    description:
      - Specifies the status of the NAT gateway
    type: str

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
nat_gateways:
    description: List of dictionaries describing NAT gateways.
    type: complex
    returned: On Success.
    contains:
        admin_state_up:
            description: Specifies whether gateway is up or down.
            type: bool
            sample: True
        created_at:
            description: Creation time of the NAT gateway
            type: str
            sample: "yyyy-mm-dd hh:mm:ss"
        description:
            description: Description of the NAT gateway
            type: str
            sample: "My Gateway"
        gateway:
            description: Name or ID of the NAT gateway
            type: str
            sample: "my-gateway"
        internal_network_id:
            description: Network ID where the NAT gateway is attached to.
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        project_id:
            description: Project ID where the NAT gateway is located in.
            type: str
            sample: "16d53a84a13b49529d2e2c3646612345"
        router_id:
            description: VPC / Router ID where the NAT gateway is attached to.
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        spec:
            description: Specifies the type of the NAT gateway.
            type: str
            sample: "1"
        status:
            description: Specifies the status of the NAT gateway.
            type: str
            sample: "ACTIVE"
'''

EXAMPLES = '''
# Get configs versions.
- nat_gateway_info:
  register: gw

- nat_gateway_info:
    gateway: "my_gateway"
  register: gw

- nat_gateway_info:
    spec: "1"
  register: gw

- nat_gateway_info:
    status: "ACTIVE"
    spec: "1"
  register: gw

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class NATGatewayInfoModule(OTCModule):
    argument_spec = dict(
        admin_state_up=dict(required=False, type='bool'),
        created_at=dict(required=False),
        description=dict(required=False),
        gateway=dict(required=False),
        internal_network_id=dict(required=False),
        project_id=dict(required=False),
        router_id=dict(required=False),
        spec=dict(required=False, choices=["1", "2", "3", "4"]),
        status=dict(required=False)
    )

    def run(self):

        data = []
        query = {}

        if self.params['gateway']:
            gw = self.conn.nat.find_gateway(
                     name_or_id=self.params['gateway'],
                     ignore_missing=True)
            if gw:
                query['id'] = gw.id
            else:
                self.exit(
                    changed=False,
                    nat_gateways=[],
                    message=('No gateway found with name or id: %s' %
                             self.params['gateway'])
                )

        if self.params['admin_state_up']:
            query['admin_state_up'] = self.params['admin_state_up']
        if self.params['created_at']:
            query['created_at'] = self.params['created_at']
        if self.params['description']:
            query['description'] = self.params['description']
        if self.params['internal_network_id']:
            query['internal_network_id'] = self.params[
                                               'internal_network_id']
        if self.params['project_id']:
            query['project_id'] = self.params['project_id']
        if self.params['router_id']:
            query['router_id'] = self.params['router_id']
        if self.params['spec']:
            query['spec'] = self.params['spec']
        if self.params['status']:
            query['status'] = self.params['status']

        for raw in self.conn.nat.gateways(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            nat_gateways=data
        )


def main():
    module = NATGatewayInfoModule()
    module()


if __name__ == '__main__':
    main()
