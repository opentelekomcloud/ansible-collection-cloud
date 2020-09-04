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
module: nat_snat_rule_info
short_description: Get SNAT rule details
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get a SNAT Rule Details.
requirements: ["openstacksdk", "otcextensions"]
options:
  admin_state_up:
    description:
      - NAT rule state.
    type: str
  cidr:
    description:
      - Specifies a subset of the VPC subnet Classless Inter-Domain Routing block or a CIDR block of Direct Connect
    type: str
  created_at:
    description:
      - Creation time of the rule
    type: str
  floating_ip_address:
    description:
      - Assigned floating IP
    type: str
  floating_ip_id:
    description:
      - ID of the floating IP
    type: str
  nat_gateway_id:
    description:
      - ID of the NAT gateway
    type: str
  network_id:
    description:
      - ID of the assigned network
    type: str
  project_id:
    description:
      - Filters SNAT rules for the project ID
    type: str
  rule:
    description:
      - ID the rule
    type: str
  source_type:
    description:
      - 0 Either network id or cidr can be specified in VPC ... 1 only cidr can be specified over Direct Connect
    type: str
  status:
    description:
      - rule enabled or disable
    type: str

'''

RETURN = '''
---
snat_rules:
    description: List of SNAT rules.
    type: complex
    returned: On Success.
    contains:
        admin_state_up:
            description: NAT rule state
            type: str
            sample: "True"
        cidr:
            description: Specifies a subset of the VPC subnet Classless Inter-Domain Routing block or a CIDR block of Direct Connect
            type: str
            sample: "null"
        created_at:
            description: Creation time
            type: str
            sample: "yyyy-mm-dd hh:mm:ss"
        floating_ip_address:
            description: Assigned Floating IP Address
            type: str
            sample: "123.1.2.3"
        floating_ip_id:
            description: Assigned Floating IP ID
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        id:
            description: ID of the SNAT rule
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        nat_gateway_id:
            description: NAT Gateway ID
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        network_id:
            description: ID of the attached Network
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        project_id:
            description: ID of the Project where the SNAT rule is located in
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
- nat_snat_rule_info:
    rule: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
  register: sn

- nat_snat_rule_info:
    status: "ACTIVE"
  register: sn

- nat_snat_rule_info:
    status: "ACTIVE"
    source_type: "0"
  register: sn
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SNATRuleInfoModule(OTCModule):
    argument_spec = dict(
        admin_state_up=dict(required=False),
        cidr=dict(required=False),
        created_at=dict(required=False),
        floating_ip_address=dict(required=False),
        floating_ip_id=dict(required=False),
        nat_gateway_id=dict(required=False),
        network_id=dict(required=False),
        rule=dict(required=False),
        source_type=dict(required=False),
        status=dict(required=False),
        project_id=dict(required=False)
    )

    def run(self):
      
        data = []
        query = {}

        if self.params['rule']:
            snat = self.conn.nat.get_snat_rule(snat_rule=self.params['rule'])
            if snat:
                query['id'] = snat.id
            else:
                self.exit(
                    changed=False,
                    snat_rules=[],
                    message=('No SNAT rule found with id: %s' %
                             self.params['rule'])
                )

        if self.params['admin_state_up']:
            query['admin_state_up'] = self.params['admin_state_up']
        if self.params['cidr']:
            query['cidr'] = self.params['cidr']
        if self.params['created_at']:
            query['created_at'] = self.params['created_at']
        if self.params['floating_ip_address']:
            query['floating_ip_address'] = self.params['floating_ip_address']
        if self.params['floating_ip_id']:
            query['floating_ip_id'] = self.params['floating_ip_id']
        if self.params['nat_gateway_id']:
            query['nat_gateway_id'] = self.params['nat_gateway_id']
        if self.params['network_id']:
            query['network_id'] = self.params['network_id']
        if self.params['project_id']:
            query['project_id'] = self.params['project_id']
        if self.params['source_type']:
            query['source_type'] = self.params['source_type']
        if self.params['status']:
            query['status'] = self.params['status']

        for raw in self.conn.nat.snat_rules(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            snat_rules=data
        )


def main():
    module = SNATRuleInfoModule()
    module()


if __name__ == '__main__':
    main()
