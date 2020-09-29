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
module: NatDnatModule
short_description: Manage NAT DNAT rules
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.6"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Manage NAT DNAT rules
options:
  admin_state_up:
    description:
      - DNAT rule state.
    type: bool
  description:
    description:
      - Description of the DNAT rule
    type: str
  external_service_port:
    description:
      - Specifies the port for providing external services.
    type: str
  floating_ip:
    description:
      - ID or Name of the floating IP
    type: str
    required: true
  id:
    description:
      - ID of the DNAT rule
    type: str
  internal_service_port:
    description:
      - Specifies the port used by ECSs or BMSs to provide services for external systems
    type: str
    required: true
  nat_gateway:
    description:
      - ID or Name of the NAT gateway
    type: str
    required: true
  port_id:
    description:
      - Specifies the port ID of an ECS or a BMS. This parameter and private_ip are alternative
    type: str
  private_ip:
    description:
      - Specifies the private IP address, for example, the IP address of a Direct Connect connection. This parameter and port_id are alternative
    type: str
  protocol:
    description:
      - Specifies the protocol type. Currently, TCP, UDP, and ANY are supported.
    type: str
    required: true
  project_id:
    description:
      - Specifies the project ID
    type: str
  state:
    choices: [present, absent]
    default: present
    description: Instance state
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
nat_gateways:
    description: List of dictionaries describing DNAT rules.
    type: complex
    returned: On Success.
    contains:
        admin_state_up:
            description: Specifies whether the rule is active or down.
            type: bool
            sample: True
        created_at:
            description: Creation time of the DNAT rule
            type: str
            sample: "yyyy-mm-dd hh:mm:ss"
        description:
            description: Description of the DNAT rule
            type: str
            sample: "My Rule"
        external_service_port:
            description: Specifies the port for providing external services.
            type: str
            sample: "88"
        floating_ip:
            description: IP / ID of the floating IP Address assigned to the rule.
            type: str
            sample: "123.12.1.12"
        id:
            description: ID of the DNAT rule
            type: str
            sample: "5acab424-69fb-4408-93d1-b2801b306827"
        internal_service_port:
            description: Specifies the port used by ECSs or BMSs to provide services for external systems
            type: str
            sample: "88"
        nat_gateway_id:
            description: Id of the assigned Nat gateway.
            type: str
            sample: "2aa32feb-f0b7-4dcc-a7b4-e0233686702b"
        port_id:
            description: Specifies the port ID of an ECS or a BMS. This parameter and private_ip are alternative
            type: str
            sample: "736abea5-aaf8-40b9-bf17-cc081a785d67"
        private_ip:
            description: Specifies the private IP address, e.g. the IP address of a Direct Connect connection. This parameter and port_id are alternative
            type: str
            sample: "192.168.2.1"
        project_id:
            description: Project ID where the DNAT rule is located in.
            type: str
            sample: "25dc3fc8-d019-4a34-9fff-0a09fde6a567"
        protocol:
            description: Used protocol
            type: str
            sample: "tcp"
        status:
            description: Specifies the status of the NAT gateway.
            type: str
            sample: "ACTIVE"
'''

EXAMPLES = '''
# create DNAT rule
nat_dnat:
    cloud: otc
    description: miau
    nat_gateway: 2b725feb-f0b7-4dcc-a7b4-e0233686702b
    internal_service_port: 88
    external_service_port: 88
    port_id: 840bbea5-aaf8-40b9-bf17-cc081a785d67
    floating_ip: f39ef6e6-a4b3-42be-a501-b7dfe251bfae
    protocol: tcp
    state: present

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class NATDNATModule(OTCModule):
    argument_spec = dict(
        admin_state_up=dict(required=False, type='bool'),
        description=dict(required=False),
        external_service_port=dict(required=False),
        floating_ip=dict(required=True),
        id=dict(required=False),
        internal_service_port=dict(required=True),
        nat_gateway=dict(required=True),
        port_id=dict(required=False),
        private_ip=dict(required=False),
        protocol=dict(required=True),
        project_id=dict(required=False),
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
        changed = False
        if self.params['id']:
            name = self.params['id']
            dnat_rule = self.conn.nat.get_dnat_rule(
                id=name,
                ignore_missing=True)

        if self.ansible.check_mode:
            self.exit(changed=self._system_state_change(dnat_rule))

        if self.params['state'] == 'absent':
            changed = False

            if dnat_rule:
                self.conn.nat.delete_dnat_rule(dnat_rule)
                changed = True

        elif self.params['state'] == 'present':
            attrs = {}

            if self.params['admin_state_up']:
                attrs['admin_state_up'] = self.params['admin_state_up']
            if self.params['description']:
                attrs['description'] = self.params['description']

            nw = self.conn.network.find_ip(
                name_or_id=self.params['floating_ip'],
                ignore_missing=True)
            if nw:
                attrs['floating_ip_id'] = nw.id
            else:
                self.exit(
                    changed=False,
                    message=('No floating IP found with name or id: %s' %
                             self.params['floating_ip'])
                )

            if self.params['internal_service_port']:
                attrs['internal_service_port'] = self.params['internal_service_port']
            if self.params['external_service_port']:
                attrs['external_service_port'] = self.params['external_service_port']
            if self.params['project_id']:
                attrs['project_id'] = self.params['project_id']
            gw = self.conn.nat.find_gateway(
                name_or_id=self.params['nat_gateway'],
                ignore_missing=True
            )
            if gw:
                attrs['nat_gateway_id'] = gw.id
            else:
                self.exit(
                    changed=False,
                    message=('No gateway found with name or id: %s' %
                             self.params['nat_gateway'])
                )
            if self.params['private_ip']:
                attrs['private_ip'] = self.params['private_ip']

            if self.params['port_id']:
                if self.params['private_ip']:
                    self.exit(
                        changed=False,
                        message=('Either specify port_id OR private_ip')
                    )
                else:
                    attrs['port_id'] = self.params['port_id']
            if self.params['private_ip']:
                if self.params['port_id']:
                    self.exit(
                        changed=False,
                        message=('Either specify port_id OR private_ip')
                    )
                else:
                    attrs['private_ip'] = self.params['private_ip']

            if self.params['protocol']:
                attrs['protocol'] = self.params['protocol']

            dnat_rule = self.conn.nat.create_dnat_rule(**attrs)
            self.exit(changed=True, dnat_rule=dnat_rule.to_dict())

        self.exit(changed=changed)


def main():
    module = NATDNATModule()
    module()


if __name__ == "__main__":
    main()
