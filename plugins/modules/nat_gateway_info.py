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
version_added: "0.0.1"
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
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        internal_network_id:
            description: Network ID where the NAT gateway is attached to.
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        name:
            description: Name of the gateway.
            type: str
            sample: "nat-1234"
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
    name: "my_gateway"
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
        name=dict(required=False),
        id=dict(required=False),
        admin_state_up=dict(required=False, type='bool'),
        created_at=dict(required=False),
        description=dict(required=False),
        internal_network_id=dict(required=False),
        router_id=dict(required=False),
        spec=dict(required=False, choices=["1", "2", "3", "4"]),
        status=dict(required=False),
        project_id=dict(required=False)
    )

    def run(self):
        name_filter = self.params['name']
        id_filter = self.params['id']
        admin_state_up_filter = self.params['admin_state_up']
        created_at_filter = self.params['created_at']
        description_filter = self.params['description']
        internal_network_id_filter = self.params['internal_network_id']
        router_id_filter = self.params['router_id']
        spec_filter = self.params['spec']
        status_filter = self.params['status']
        project_id_filter = self.params['project_id']

        data = []

        for raw in self.conn.nat.gateways():
            if (name_filter and raw.name != name_filter):
                continue
            if (id_filter and raw.id != id_filter):
                continue
            if (admin_state_up_filter is None):
                pass
            elif ((admin_state_up_filter and not raw.admin_state_up) or
                    (not admin_state_up_filter and raw.admin_state_up)):
                continue
            if (created_at_filter and raw.created_at != created_at_filter):
                continue
            if (description_filter and raw.description
                    != description_filter):
                continue
            if (internal_network_id_filter and raw.internal_network_id
                    != internal_network_id_filter):
                continue
            if (router_id_filter and raw.router_id != router_id_filter):
                continue
            if (spec_filter and raw.spec != spec_filter):
                continue
            if (status_filter and raw.status != status_filter):
                continue
            if (project_id_filter and raw.project_id != project_id_filter):
                continue
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
