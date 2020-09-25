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
module: nat_gateway
short_description: Manage NAT gateway instances
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Tino Schreiber (@tischrei)"
description:
  - Manage NAT gateway instances
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
  gateway:
    description:
      - Name or ID of the NAT gateway.
    type: str
  internal_network_id:
    description:
      - Network ID where the NAT gateway is attached to.
      - Mandatory for creating gateway instance.
    type: str
  project_id:
    description:
      - Filters NAT gateways of the project ID.
    type: str
  router_id:
    description:
      - ID of the router where the NAT gateway is attached.
      - Mandatory for creating gateway instance.
    type: str
  spec:
    description:
      - Specifies the type of the NAT gateway. 1 (small 10.000 connections),
        2 (medium 50.000 connections), 3 (large 200.000 connections), 4
        (extra-large 1.000.000 connections)
    type: str
    default: 1
    choices: ["1", "2", "3", "4"]
  state:
    choices: [present, absent]
    default: present
    description: Instance state
    type: str
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
            description: ID of the NAT gateway
            type: str
            sample: "my-gateway"
        internal_network_id:
            description: Network ID where the NAT gateway is attached to.
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        name:
            description: Name of the NAT gateway.
            type: str
            sample: "my-gateway"
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
    internal_network:id "1234f0c7-82e3-478d-8433-dc5984859e3b"
    name: "my_gateway"
    router_id: "1234f70c-6d1d-471e-a911-6924b7ec6ea9"
    state: present
  register: gw

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class NATGatewayModule(OTCModule):
    argument_spec = dict(
        admin_state_up=dict(required=False, type='bool'),
        description=dict(required=False),
        internal_network=dict(required=True),
        name=dict(required=True),
        project=dict(required=False),
        router=dict(required=True),
        spec=dict(required=True, default='1', choices=["1", "2", "3", "4"]),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )

    def _system_state_change(self, obj):
        state = self.params['state']
        if state == 'present':
            if not obj:
                return True
        elif state == 'absent' and obj:
            return True
        return False

    def run(self):
        name = self.params['name']

        changed = False

        gateway = self.conn.nat.find_gateway(
            name_or_id=name)

        if self.ansible.check_mode:
            self.exit(changed=self._system_state_change(gateway))

        if self.params['state'] == 'absent':
            changed = False

            if gateway:
                self.conn.nat.delete_gateway(gateway)
                changed = True

        elif self.params['state'] == 'present':

            if gateway:
                self.exit(changed=False)
            
            attrs = {}

            if self.params['admin_state_up']:
                attrs['admin_state_up'] = self.params['admin_state_up']
            if self.params['description']:
                attrs['description'] = self.params['description']

            nw = self.conn.network.find_network(
                name_or_id=self.params['internal_network'],
                ignore_missing=True)
            if nw:
                attrs['internal_network_id'] = nw.id
            else:
                self.exit(
                    changed=False,
                    snat_rules=[],
                    message=('No network found with name or id: %s' %
                            self.params['internal_network'])
                )

            attrs['name'] = self.params['name']
            if self.params['project']:
                attrs['project_id'] = self.params['project']
            
            rt = self.conn.network.find_router(
                name_or_id=self.params['router'],
                ignore_missing=True)
            if rt:
                attrs['router_id'] = rt.id
            else:
                self.exit(
                    changed=False,
                    message=('No router found with name or id: %s' %
                            self.params['router'])
                )
            
            if self.params['spec']:
                attrs['spec'] = self.params['spec']

            gateway = self.conn.nat.create_gateway(**attrs)
            self.exit(changed=True, gateway=gateway.to_dict())

        self.exit(changed=changed)


def main():
    module = NATGatewayModule()
    module()


if __name__ == "__main__":
    main()
