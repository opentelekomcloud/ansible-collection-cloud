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
module: lb_listener_info
short_description: Get listener info from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Get Enhanced Load Balancer listener from the OTC.
options:
  name:
    description:
      - Optional name or id of the listener
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
lb_listener_info:
  description: Dictionary describing listeners.
  type: complex
  returned: On Success.
  contains:
    id:
      description: Specifies the listener ID.
      type: str
      sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
    name:
      description: Specifies the listener name.
      type: str
      sample: "elb_test"
    description:
      description: Provides supplementary information about the listener.
      type: str
    protocol:
      description: Specifies the load balancer protocol.
      type: str
      sample: "TCP"
    protocol_port:
      description: Specifies the port used by the load balancer.
      type: int
      sample: "80"
    load_balancer_ids:
      description: Specifies the IDs of the associated load balancer.
      type: list
    connection_limit:
      description: Specifies the maximum number of connections.
      type: int
    is_admin_state_up:
      description: Specifies the administrative status of the listener.
      type: bool
    default_pool_id:
      description: Specifies the ID of the associated backend server group.
      type: str
    default_tls_container_ref:
      description: Specifies the ID of the server certificate used by the listener.
      type: str
    sni_container_refs:
      description: Lists the IDs of SNI certificates (server certificates with a domain name) used by the listener.
      type: list
'''

EXAMPLES = '''
# Get a lb listener info.
- lb_listener_info:
    name: listener-test
  register: lb_lstnr_info
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LoadBalancerListenerInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False)
    )

    def run(self):
        data = []

        if self.params['name']:
            raw = self.conn.network.find_listener(name_or_id=self.params['name'])
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)
        else:
            for raw in self.conn.network.listeners():
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit_json(
            changed=False,
            listeners=data
        )


def main():
    module = LoadBalancerListenerInfoModule()
    module()


if __name__ == '__main__':
    main()
