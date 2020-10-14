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
module: nat_snat_rule
short_description: Manage NAT SNAT rule instances
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Tino Schreiber (@tischrei)"
description:
  - Manage NAT SNAT rule instances
options:
  cidr:
    description:
      - Specifies a subset of the VPC subnet CIDR block or
      - a CIDR block of Direct Connect connection.
    type: str
  floating_ip:
    description:
      - Address or ID of the floating IP where the SNAT rule is attached to.
    type: str
  id:
    description: ID of the NAT SNAT rule
    type: str
  nat_gateway:
    description:
      - Name or ID of the NAT gateway
    type: str
  network:
    description:
      - ID or Name of the network for the SNAT rule.
    type: str
  source_type:
    description:
      - 0 Either network_id or cidr can be specified in VPC
      - 1 only cidr can be specified over a Direct Connect connection.
    type: int
    default: 0
    choices: [0, 1]
  state:
    choices: [present, absent]
    default: present
    description: Instance state
    type: str

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
snat_rule:
    description: Dictionary describing the SNAT rule.
    type: complex
    returned: On Success.
    contains:
        admin_state_up:
            description: Specifies whether gateway is up or down.
            type: bool
            sample: True
        cidr:
            description:
              - Specifies a subset of the VPC subnet CIDR block or
              - a CIDR block of Direct Connect connection.
            type: str
            sample: "192.168.1.10/32"
        created_at:
            description: Creation time of the NAT SNAT rule
            type: str
            sample: "yyyy-mm-dd hh:mm:ss"
        floating_ip_address:
            description: Address of the floating IP
            type: str
            sample: e1029c97-639e-4481-9254-f30c5632b123"
        floating_ip_id:
            description: ID of the floating IP address
            type: str
            sample: "e1029c97-639e-4481-9254-f30c5632b123"
        id:
            description: ID of the NAT SNAT rule
            type: str
            sample: "3fea684b-50f1-4613-967a-a7bed5e59123"
        nat_gateway_id:
            description: ID of the attached NAT gateway
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        tenant_id:
            description: Project ID where the NAT SNAT rule is located in.
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a567"
        network_id:
            description:
              - Network ID of the subnet where the NAT SNAT rule
              - points to.
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a567"
        source_type:
            description:
              - 0 Either network_id or cidr can be specified in VPC
              - 1 only cidr can be specified over a Direct Connect connection.
            type: int
            sample: 0
        status:
            description: Specifies the status of the NAT gateway.
            type: str
            sample: "ACTIVE"
'''

EXAMPLES = '''
# Create snat_rule with cidr
- nat_snat_rule:
    cloud: otc
    nat_gateway: 0035136a-9b29-4232-b456-1059ca11a123
    floating_ip: '80.158.47.5'
    cidr: '192.168.0.0/32'
    state: present
  register: snat

# Create SNAT rule with network
- nat_snat_rule:
    cloud: otc
    nat_gateway: 0035136a-9b29-4232-b456-1059ca11a123
    floating_ip: '80.158.47.5'
    network: c6b2dbc9-ca80-4b49-bbbb-85ea9b96f123
    state: present
  register: snat
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class NatSnatModule(OTCModule):
    argument_spec = dict(
        cidr=dict(required=False),
        floating_ip=dict(required=False),
        id=dict(required=False),
        nat_gateway=dict(required=False),
        network=dict(required=False),
        source_type=dict(required=False, type='int', choices=[0, 1]),
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

        # pre flight checks
        if self.params['network'] and self.params['cidr']:
            self.exit(
                changed=False,
                message=('Network and cidr parameter cannot be used at '
                         'the same time.'),
                failed=True
            )

        # gathering main facts for creation and deletion
        attrs = {}

        if self.params['cidr']:
            attrs['cidr'] = self.params['cidr']
        if self.params['network']:
            nw = self.conn.network.find_network(
                self.params['network'],
                ignore_missing=True
            )
            if not nw:
                self.exit(
                    changed=False,
                    message=('Given network %s not found.' %
                             self.params['network']),
                    failed=True
                )
            attrs['network_id'] = nw.id
        if self.params['floating_ip']:
            ip = self.conn.network.find_ip(
                self.params['floating_ip'],
                ignore_missing=True
            )
            if not ip:
                self.exit(
                    changed=False,
                    message=('Given Floating IP %s not found.' %
                             self.params['floating_ip']),
                    failed=True
                )
            attrs['floating_ip_id'] = ip.id

        # if self.ansible.check_mode:
        #    self.exit(changed=self._system_state_change(gateway))

        # SNAT rule deletion
        if self.params['state'] == 'absent':
            changed = False

            if self.params['id']:
                snat_rule = self.conn.nat.get_snat_rule(self.params['id'])
                if snat_rule:
                    self.conn.nat.delete_snat_rule(snat_rule.id)
                    self.exit(changed=True)
                else:
                    self.exit(
                        changed=False,
                        message=('id %s not found' % self.params['id']),
                        failed=True
                    )

            for rule in self.conn.nat.snat_rules(**attrs):
                if rule.id:
                    self.conn.nat.delete_snat_rule(rule.id)
                    changed = True
                    break

        # SNAT rule creation
        elif self.params['state'] == 'present':

            gateway = self.conn.nat.find_gateway(
                name_or_id=self.params['nat_gateway'],
                ignore_missing=True)
            if not gateway:
                self.exit(
                    changed=False,
                    message=('NAT gateway %s does not exist.'
                             % self.params['nat_gateway']),
                    failed=True
                )
            attrs['nat_gateway_id'] = gateway.id

            if self.params['source_type']:
                attrs['source_type'] = self.params['source_type']

            for rule in self.conn.nat.snat_rules(**attrs):
                if rule.id:
                    self.exit(
                        changed=False,
                        snat_rule=rule.to_dict()
                    )

            snat_rule = self.conn.nat.create_snat_rule(**attrs)
            self.exit(changed=True, snat_rule=snat_rule.to_dict())

        self.exit(changed=changed)


def main():
    module = NatSnatModule()
    module()


if __name__ == "__main__":
    main()
