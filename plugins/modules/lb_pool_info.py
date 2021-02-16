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
module: lb_pool_info
short_description: Get load balancer backend server group info from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Get Enhanced Load Balancer backend server group from the OTC.
options:
  name:
    description:
      - Optional name or id of the pool
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
lb_pool_info:
  description: Dictionary describing backend server groups.
  type: complex
  returned: On Success.
  contains:
    id:
      description: Specifies the ID of the backend server group.
      type: str
      sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
    name:
      description: Specifies the backend server group name.
      type: str
      sample: "elb_test_pool"
    description:
      description: Provides supplementary information about the backend server group.
      type: str
    protocol:
      description: Specifies the protocol that the backend server group uses to receive requests.
      type: str
      sample: "TCP"
    lb_algorithm:
      description: Specifies the load balancing algorithm of the backend server group.
      type: int
      sample: "ROUND_ROBIN"
    members:
      description: Lists the IDs of backend servers in the backend server group.
      type: list
    healthmonitor_id:
      description: Specifies the ID of the health check configured for the backend server group.
      type: int
    admin_state_up:
      description: Specifies the administrative status of the backend server group.
      type: bool
    listeners:
      description: Lists the IDs of listeners associated with the backend server group.
      type: list
    loadbalancers:
      description: Lists the IDs of load baancers associated with the backend server group.
      type: list
    session_persistence:
      description: Specifies whether to enable the sticky session feature.
      type: dict
'''

EXAMPLES = '''
# Get a lb pool info.
- lb_pool_info:
    state: present
    name: pool-test
  register: lb_pool_info
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LoadBalancerPoolInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )


    def run(self):
        data = []

        if self.params['name']:
            raw = self.conn.network.find_pool(name_or_id=self.params['name'])
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)
        else:
            for raw in self.conn.network.pools():
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit_json(
            changed=False,
            server_groups=data
        )


def main():
    module = LoadBalancerPoolInfoModule()
    module()


if __name__ == '__main__':
    main()
