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
module: nat_dnat_rule_info
short_description: Get DNAT rule details
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.4"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get DNAT Rule Details.
requirements: ["openstacksdk", "otcextensions"]
options:
  admin_state_up:
    description:
      - NAT rule state.
    type: bool
  created_at:
    description:
      - Creation time of the rule
    type: str
  external_service_port:
    description:
      - Specifies the port for providing external services.
    type: int
  floating_ip:
    description:
      - IP or ID of floating IP address.
    type: str
  internal_service_port:
    description:
      - Specifies port used by ECS/BMS to provide services to external systems
    type: int
  gateway:
    description:
      - Name or ID of the NAT gateway
    type: str
  port:
    description:
      - Name or ID of a network port of an ECS or BMS
    type: str
  private_ip:
    description:
      - Specifies the IP adress of a Direct Connect connection
    type: str
  project_id:
    description:
      - Filters SNAT rules for the project ID
    type: str
  protocol:
    description:
      - Specifies the protocol type. Currently TCP(6), UDP(17) and ANY(0)
    type: str
  rule:
    description:
      - ID the rule
    type: str
  status:
    description:
      - rule enabled or disabled
    type: str

'''

RETURN = '''
---
dnat_rules:
    description: List of DNAT rules.
    type: complex
    returned: On Success.
    contains:
        admin_state_up:
            description: NAT rule state
            type: bool
            sample: True
        created_at:
            description: Creation time
            type: str
            sample: "yyyy-mm-dd hh:mm:ss"
        external_service_port:
            description: Specifies the port for providing external services
            type: int
            sample: 8080
        floating_ip:
            description: IP or ID of Floating IP address.
            type: str
            sample: "123.1.2.3"
        id:
            description: ID of the DNAT rule
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        internal_service_port:
            description: Specifies the port used by ECS/BMS
            type: int
            sample: 8081
        gateway:
            description: Name or ID of the NAT gateway
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        port:
            description: Name or ID of a network port of an ECS or BMS
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        private_ip:
            description: Specifies the private IP
            type: str
            sample: "10.1.2.3"
        protocol:
            description: Specifies the protocol type. Currently TCP(6), UDP(17) and ANY(0)
            type: str
            sample: "6"
        project_id:
            description: ID of the Project where the DNAT rule is located in
            type: str
            sample: "16d53a84a13b49529d2e2c3646612345"
        source_type:
            description: 0 Either network id or cidr can be specified in VPC ... 1 only cidr can be specified over Direct Connect
            type: str
            sample: "0"
        status:
            description: NAT rule status
            type: str
            sample: "ACTIVE"
'''

EXAMPLES = '''
# Get configs versions.
- nat_dnat_rule_info:
  register: dn

- nat_dnat_rule_info:
    rule: "2f561c37-277e-412a-8f76-0d430b596de5"
  register: dn

- nat_dnat_rule_info:
    admin_state_up: "true"
    status: "ACTIVE"
  register: dn
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNATRuleInfoModule(OTCModule):
    argument_spec = dict(
        admin_state_up=dict(required=False, type='bool'),
        created_at=dict(required=False),
        external_service_port=dict(required=False, type='int'),
        floating_ip=dict(required=False),
        internal_service_port=dict(required=False, type='int'),
        gateway=dict(required=False),
        port=dict(required=False),
        private_ip=dict(required=False),
        protocol=dict(required=False),
        rule=dict(required=False),
        status=dict(required=False),
        project_id=dict(required=False)
    )

    def run(self):
        data = []
        query = {}

        if self.params['rule']:
            dnat = self.conn.nat.get_dnat_rule(dnat_rule=self.params['rule'])
            if dnat:
                query['id'] = dnat.id
            else:
                self.exit(
                    changed=False,
                    dnat_rules=[],
                    message=('No DNAT rule found with id: %s' %
                             self.params['rule'])
                )

        if self.params['admin_state_up']:
            query['admin_state_up'] = self.params['admin_state_up']
        if self.params['created_at']:
            query['created_at'] = self.params['created_at']
        if self.params['external_service_port']:
            query['external_service_port'] = self.params[
                'external_service_port']
        if self.params['floating_ip']:
            rs = self.conn.network.find_ip(
                name_or_id=self.params['floating_ip'],
                ignore_missing=True)
            if rs:
                query['floating_ip_id'] = rs.id
            else:
                self.exit(
                    changed=False,
                    dnat_rules=[],
                    message=('No Floating IP found with name or id: %s' %
                             self.params['floating_ip'])
                )
        if self.params['internal_service_port']:
            query['internal_service_port'] = self.params[
                'internal_service_port']
        if self.params['gateway']:
            gw = self.conn.nat.find_gateway(
                name_or_id=self.params['gateway'],
                ignore_missing=True)
            if gw:
                query['nat_gateway_id'] = gw.id
            else:
                self.exit(
                    changed=False,
                    dnat_rules=[],
                    message=('No NAT gateway found with name or id: %s' %
                             self.params['gateway'])
                )
        if self.params['port']:
            rs = self.conn.network.find_port(
                name_or_id=self.params['port'],
                ignore_missing=True)
            if rs:
                query['port_id'] = rs.id
            else:
                self.exit(
                    changed=False,
                    dnat_rules=[],
                    message=('No port found with name or id: %s' %
                             self.params['port'])
                )
        if self.params['private_ip']:
            query['private_ip'] = self.params['private_ip']
        if self.params['project_id']:
            query['project_id'] = self.params['project_id']
        if self.params['protocol']:
            query['protocol'] = self.params['protocol']
        if self.params['status']:
            query['status'] = self.params['status']

        for raw in self.conn.nat.dnat_rules(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            dnat_rules=data
        )


def main():
    module = DNATRuleInfoModule()
    module()


if __name__ == '__main__':
    main()
