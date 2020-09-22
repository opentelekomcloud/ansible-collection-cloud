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
module: loadbalancer_info
short_description: Get load balancer info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Artem Goncharov (@gtema)"
description:
  - Get Enhanced Load Balancer from the OTC load-balancer service(ELB).
options:
  name:
    description:
      - Optional name of the loadbalancer.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
loadbalancers:
    description: Dictionary describing load balancers
    type: complex
    returned: On Success.
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        name:
            description: Name given to the load balancer.
            type: str
            sample: "elb_test"
        vip_network_id:
            description: Network ID the load balancer virutal IP port belongs
                to.
            type: str
            sample: "f171db43-56fd-41cf-82d7-4e91d741762e"
        vip_subnet_id:
            description: Subnet ID the load balancer virutal IP port belongs
                to.
            type: str
            sample: "c53e3c70-9d62-409a-9f71-db148e7aa853"
        vip_port_id:
            description: The load balancer virutal IP port ID.
            type: str
            sample: "2061395c-1c01-47ab-b925-c91b93df9c1d"
        vip_address:
            description: The load balancer virutal IP address.
            type: str
            sample: "192.168.2.88"
        public_vip_address:
            description: The load balancer public VIP address.
            type: str
            sample: "10.17.8.254"
        provisioning_status:
            description: The provisioning status of the load balancer.
            type: str
            sample: "ACTIVE"
        operating_status:
            description: The operating status of the load balancer.
            type: str
            sample: "ONLINE"
        is_admin_state_up:
            description: The administrative state of the load balancer.
            type: bool
            sample: true
        listeners:
            description: The associated listener IDs, if any.
            type: list
            sample: [{"id": "7aa1b380-beec-459c-a8a7-3a4fb6d30645"}, {"id": "692d06b8-c4f8-4bdb-b2a3-5a263cc23ba6"}]
        pools:
            description: The associated pool IDs, if any.
            type: list
            sample: [{"id": "27b78d92-cee1-4646-b831-e3b90a7fa714"}, {"id": "befc1fb5-1992-4697-bdb9-eee330989344"}]
'''

EXAMPLES = '''
# Get a load balancer by specifying the VIP subnet.
- loadbalancer_info:
    auth:
      auth_url: https://identity.example.com
      username: admin
      password: passme
      project_name: admin
    state: present
    name: my_lb
  register: lb_info
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LoadBalancerInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False)
    )

    def run(self):
        if self.params['name']:
            lb = self.conn.network.find_load_balancer(
                name_or_id=self.params['name'])
        else:
            lb = list(self.conn.network.load_balancers())

        self.exit_json(
            changed=False,
            loadbalancers=lb
        )


def main():
    module = LoadBalancerInfoModule()
    module()


if __name__ == "__main__":
    main()
