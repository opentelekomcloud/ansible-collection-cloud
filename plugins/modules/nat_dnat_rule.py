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
module: nat_dnat_rule
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
  external_service_port:
    description:
      - Specifies the port for providing external services.
      - Mandatory for DNAT rule creation
    type: int
  floating_ip:
    description:
      - ID or Name of the floating IP
      - Mandatory for DNAT rule creation
    type: str
  id:
    description:
      - ID of the DNAT rule
    type: str
  internal_service_port:
    description:
      - Specifies the port used by ECSs or BMSs to provide services for external systems
      - Mandatory for DNAT rule creation
    type: int
  nat_gateway:
    description:
      - ID or Name of the NAT gateway
      - Mandatory for DNAT rule creation
    type: str
  port:
    description:
      - Specifies the port ID of an ECS or a BMS. This parameter and private_ip are alternative
    type: str
  private_ip:
    description:
      - Specifies the private IP address, for example, the IP address of a Direct Connect connection. This parameter and port are alternative
    type: str
  protocol:
    description:
      - Specifies the protocol type. Currently, TCP, UDP, and ANY are supported.
      - Mandatory for DNAT rule creation
    type: str
    default: tcp
    choices: [tcp, udp, any]
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
dnat_rule:
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
        external_service_port:
            description: Specifies the port for providing external services.
            type: int
            sample: 80
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
            type: int
            sample: 80
        nat_gateway_id:
            description: ID or name of the assigned Nat gateway.
            type: str
            sample: "2aa32feb-f0b7-4dcc-a7b4-e0233686702b"
        port:
            description: Specifies the port ID of an ECS or a BMS. This parameter and private_ip are alternative
            type: str
            sample: "736abea5-aaf8-40b9-bf17-cc081a785d67"
        private_ip:
            description: Specifies the private IP address, e.g. the IP address of a Direct Connect connection. This parameter and port are alternative
            type: str
            sample: "192.168.2.1"
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
    nat_gateway: 2b725feb-f0b7-4dcc-a7b4-e02336867123
    internal_service_port: 80
    external_service_port: 80
    port: 840bbea5-aaf8-40b9-bf17-cc081a785123
    floating_ip: f39ef6e6-a4b3-42be-a501-b7dfe251b123
    protocol: tcp
    state: present

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class NatDnatModule(OTCModule):
    argument_spec = dict(
        admin_state_up=dict(required=False, type='bool'),
        external_service_port=dict(required=False, type='int'),
        floating_ip=dict(required=False),
        id=dict(required=False),
        internal_service_port=dict(required=False, type='int'),
        nat_gateway=dict(required=False),
        port=dict(required=False),
        private_ip=dict(required=False),
        protocol=dict(required=False, choices=['tcp', 'udp', 'any'],
                      default='tcp'),
        project_id=dict(required=False),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        changed = False

        if self.params['state'] == 'absent':
            changed = False
            if self.ansible.check_mode:
                self.exit_json(changed=True)
            if self.params['id']:
                dnat_rule = self.conn.nat.get_dnat_rule(
                    dnat_rule=self.params['id']
                )
                if dnat_rule:
                    self.conn.nat.delete_dnat_rule(dnat_rule)
                    changed = True
                else:
                    self.exit(
                        changed=False,
                        message=('No DNAT rule found with name or id: %s' %
                                 self.params['id'])
                    )
            else:
                self.exit(
                    changed=False,
                    message=('Parameter id is missing to delete DNAT '
                             'rule.'),
                    failed=True
                )

        elif self.params['state'] == 'present':
            attrs = {}
            if self.ansible.check_mode:
                self.exit_json(changed=True)
            if self.params['admin_state_up']:
                attrs['admin_state_up'] = self.params['admin_state_up']
            if self.params['floating_ip']:
                fip = self.conn.network.find_ip(
                    name_or_id=self.params['floating_ip'],
                    ignore_missing=True
                )
                if fip:
                    attrs['floating_ip_id'] = fip.id
                else:
                    self.exit(
                        changed=False,
                        message=('No floating IP found with name or id: %s' %
                                 self.params['floating_ip'])
                    )
            else:
                self.exit(
                    changed=False,
                    message=('floating_ip parameter is required to create '
                             'a DNAT rule.'),
                    failed=True
                )
            if self.params['internal_service_port']:
                attrs['internal_service_port'] = self.params['internal_service_port']
            else:
                self.exit(
                    changed=False,
                    message=('Parameter internal_service_port is required to '
                             'create a DNAT rule.'),
                    failed=True
                )
            if self.params['external_service_port']:
                attrs['external_service_port'] = self.params['external_service_port']
            else:
                self.exit(
                    changed=False,
                    message=('Parameter external_service_port is required to '
                             'create a DNAT rule.'),
                    failed=True
                )
            if self.params['project_id']:
                attrs['project_id'] = self.params['project_id']
            if self.params['nat_gateway']:
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
            else:
                self.exit(
                    changed=False,
                    message=('nat_gateway parameter is required to create'
                             'DNAT rule.')
                )
            if self.params['private_ip']:
                attrs['private_ip'] = self.params['private_ip']

            if self.params['port']:
                if self.params['private_ip']:
                    self.exit(
                        changed=False,
                        message=('Either specify port OR private_ip')
                    )
                else:
                    p = self.conn.network.find_port(
                        name_or_id=self.params['port'],
                        ignore_missing=True
                    )
                    if not p:
                        self.exit(
                            changed=False,
                            message=('No port found with name or id: %s' %
                                     self.params['port']),
                            failed=True
                        )
                    attrs['port_id'] = p.id
            if self.params['private_ip']:
                if self.params['port']:
                    self.exit(
                        changed=False,
                        message=('Either specify port OR private_ip'),
                        failed=True
                    )
                else:
                    attrs['private_ip'] = self.params['private_ip']

            if self.params['protocol']:
                attrs['protocol'] = self.params['protocol']
            else:
                self.exit(
                    changed=False,
                    message=('protocol parameter is required to create '
                             'a DNAT rule.'),
                    failed=True
                )

            for rule in self.conn.nat.dnat_rules(**attrs):
                if rule.id:
                    self.exit(
                        changed=False,
                        snat_rule=rule.to_dict()
                    )

            dnat_rule = self.conn.nat.create_dnat_rule(**attrs)
            self.exit(changed=True, dnat_rule=dnat_rule.to_dict())

        self.exit(changed=changed)


def main():
    module = NatDnatModule()
    module()


if __name__ == "__main__":
    main()
