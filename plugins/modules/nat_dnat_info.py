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
module: nat_dnat_info
short_description: Get DNAT rule details
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get DNAT Rule Details.
requirements: ["openstacksdk", "otcextensions"]
options:
  admin_state_up:
    description:
      - NAT rule state.
    type: str
  created_at:
    description:
      - Creation time of the rule
    type: str
  external_service_port:
    description:
      - Specifies the port for providing external services.
    type: str
  floating_ip_address:
    description:
      - Assigned floating IP
    type: str
  floating_ip_id:
    description:
      - ID of the floating IP
    type: str
  id:
    description:
      - ID the rule
    type: str
  internal_service_port:
    description:
      - Specifies port used by ECS/BMS to provide services to external systems
    type: str
  nat_gateway_id:
    description:
      - ID of the NAT gateway
    type: str
  port_id:
    description:
      - Specifies port ID of an ECS or BMS
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
  status:
    description:
      - rule enabled or disabled
    type: str

'''

RETURN = '''
---
dnat_list:
    description: List of DNAT rules.
    type: complex
    returned: On Success.
    contains:
        admin_state_up:
            description: NAT rule state
            type: str
            sample: "True"
        created_at:
            description: Creation time
            type: str
            sample: "yyyy-mm-dd hh:mm:ss"
        external_service_port:
            description: Specifies the port for providing external services
            type: str
            sample: "123"
        floating_ip_address:
            description: Assigned Floating IP Address
            type: str
            sample: "123.1.2.3"
        floating_ip_id:
            description: Assigned Floating IP ID
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        id:
            description: ID of the DNAT rule
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        internal_service_port:
            description: Specifies the port used by ECS/BMS
            type: str
            sample: "123"
        nat_gateway_id:
            description: NAT Gateway ID
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a123"
        port_id:
            description: Specifies the port ID of an ECS or BMS
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
- nat_dnat_info:
  register: dn

- nat_dnat_info:
    id: "2f561c37-277e-412a-8f76-0d430b596de5"
  register: dn

- nat_dnat_info:
    admin_state_up: "true"
    status: "ACTIVE"
  register: dn
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class NATGatewayInfoModule(OTCModule):
    argument_spec = dict(
        admin_state_up=dict(required=False),
        created_at=dict(required=False),
        external_service_port=dict(required=False),
        id=dict(required=False),
        floating_ip_address=dict(required=False),
        floating_ip_id=dict(required=False),
        internal_service_port=dict(required=False),
        nat_gateway_id=dict(required=False),
        port_id=dict(required=False),
        private_ip=dict(required=False),
        protocol=dict(required=False),
        status=dict(required=False),
        project_id=dict(required=False)
    )

    def run(self):
        admin_state_up_filter = self.params['admin_state_up']
        created_at_filter = self.params['created_at']
        external_service_port_filter = self.params['external_service_port']
        floating_ip_address_filter = self.params['floating_ip_address']
        floating_ip_id_filter = self.params['floating_ip_id']
        id_filter = self.params['id']
        internal_service_port_filter = self.params['internal_service_port']
        nat_gateway_id_filter = self.params['nat_gateway_id']
        port_id_filter = self.params['port_id']
        private_ip_filter = self.params['private_ip']
        protocol_filter = self.params['protocol']
        status_filter = self.params['status']
        project_id_filter = self.params['project_id']

        data = []

        for raw in self.conn.nat.dnat_rules():
            if (admin_state_up_filter is None):
                pass
            elif ((admin_state_up_filter and not raw.admin_state_up) or
                    (not admin_state_up_filter and raw.admin_state_up)):
                continue
            if (created_at_filter and raw.created_at != created_at_filter):
                continue
            if (external_service_port_filter and raw.external_service_port != external_service_port_filter):
                continue
            if (floating_ip_address_filter and raw.floating_ip_address
                    != floating_ip_address_filter):
                continue
            if (floating_ip_id_filter and raw.floating_ip_id
                    != floating_ip_id_filter):
                continue
            if (id_filter and raw.id != id_filter):
                continue
            if (internal_service_port_filter and raw.internal_service_port != internal_service_port_filter):
                continue
            if (nat_gateway_id_filter and raw.nat_gateway_id
                    != nat_gateway_id_filter):
                continue
            if (port_id_filter and raw.port_id != port_id_filter):
                continue
            if (private_ip_filter and raw.private_ip != private_ip_filter):
                continue
            if (protocol_filter and raw.created_at != protocol_filter):
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
            dnat_list=data
        )


def main():
    module = NATGatewayInfoModule()
    module()


if __name__ == '__main__':
    main()
