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
module: lb_pool
short_description: Add/Delete backend server group for load balancer from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.4"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Add or Remove a backend server group for Enhanced Load Balancer from the OTC load-balancer
    service(ELB).
options:
  name:
    description:
      - Specifies the backend server group name.
    type: str
    required: true
  state:
    description:
      - Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
  description:
    description:
      - Provides supplementary information about the backend server group.
    type: str
  protocol:
    description:
      - Specifies the protocol that the backend server group uses to receive requests.
      Should be same as load balancer listener protocol
    choices: [tcp, http, udp, terminated_https]
    type: str
  lb_algorithm:
    description:
      - Specifies the load balancing algorithm of the backend server group.
    choices: [round_robin, least_connections, source_ip]
    type: str
  admin_state_up:
    description:
      - Specifies the administrative status of the backend server group.
    default: true
    type: bool
  listener:
    description:
      - Specifies the ID or Name of the listener associated with the backend server group.
    type: str
  loadbalancer:
    description:
      - Specifies the ID or Name of the load balancer associated with the backend server group.
    type: bool
  session_persistence:
    description:
      - Specifies the sticky session timeout duration in minutes.
    type: dict
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
lb_pool:
  description: Specifies the pool.
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
      sample: "servers_test"
    description:
      description: Provides supplementary information about the backend server group.
      type: str
    protocol:
      description: Specifies the protocol that the backend server group uses to receive requests.
      type: str
      sample: "TCP"
    lb_algorithm:
      description: Specifies the load balancing algorithm of the backend server group.
      type: str
      sample: "ROUND_ROBIN"
    members:
      description: Lists the IDs of backend servers in the backend server group.
      type: list
    healthmonitor_id:
      description: Specifies the ID of the health check configured for the backend server group.
      type: str
    admin_state_up:
      description: Specifies the administrative status of the backend server group.
      type: bool
    listeners:
      description: Lists the IDs of listeners associated with the backend server group.
      type: list
    loadbalancers:
      description: Lists the IDs of load balancers associated with the backend server group.
      type: list
    session_persistence:
      description: Specifies whether to enable the sticky session feature.
      type: str
'''

EXAMPLES = '''
# Create a lb server group.
- lb_pool:
    state: present
    name: pool-test
    protocol: tcp
    lb_algorithm: round_robin
    listener: "5896b6f1-698f-4a81-989e-978b3f045643"
    loadbalancer: "0416b6f1-877f-4a51-987e-978b3f084253"

# Create a lb server group with session_persistence.
- lb_pool:
    state: present
    name: pool-test
    protocol: tcp
    lb_algorithm: round_robin
    listener: "5896b6f1-698f-4a81-989e-978b3f045643"
    loadbalancer: "0416b6f1-877f-4a51-987e-978b3f084253"
    session_persistence:
      - type: http_cookie
      - persistence_timeout: 60

# Delete a load balancer(and all its related resources)
- lb_pool:
    state: absent
    name: pool-test
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LoadBalancerPoolModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        state=dict(default='present', choices=['absent', 'present']),
        description=dict(required=False, type='str'),
        lb_algorithm=dict(required=False, choices=['round_robin', 'least_connections', 'source_ip']),
        protocol=dict(required=False, choices=['tcp', 'http', 'udp', 'terminated_https']),
        listener=dict(required=False, type='str'),
        loadbalancer=dict(required=False, type='str'),
        admin_state_up=dict(required=False, type='bool'),
        session_persistence=dict(required=False, type='dict'),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        name_filter = self.params['name']
        description_filter = self.params['description']
        lb_algorithm_filter = self.params['lb_algorithm']
        protocol_filter = self.params['protocol']
        listener_filter = self.params['listener']
        loadbalancer_filter = self.params['loadbalancer']
        admin_state_up_filter = self.params['admin_state_up']
        session_persistence_filter = self.params['session_persistence']

        lb_pool = None
        attrs = {}
        changed = False
        lb_pool = self.conn.network.find_pool(name_or_id=name_filter)

        if self.params['state'] == 'present':
            if name_filter:
                attrs['name'] = name_filter
            if description_filter:
                attrs['description'] = description_filter
            if lb_algorithm_filter:
                attrs['lb_algorithm'] = lb_algorithm_filter.upper()
            if protocol_filter:
                attrs['protocol'] = protocol_filter.upper()
            if listener_filter:
                lstnr = self.conn.network.find_listener(name_or_id=listener_filter)
                if lstnr:
                    attrs['listener_id'] = lstnr.id
            if loadbalancer_filter:
                lb = self.conn.network.find_load_balancer(name_or_id=loadbalancer_filter)
                if lb:
                    attrs['loadbalancer_id'] = lb.id
            if admin_state_up_filter:
                attrs['admin_state_up'] = admin_state_up_filter
            if session_persistence_filter:
                session_persistence_filter['type'] = session_persistence_filter['type'].upper()
                attrs['session_persistence'] = session_persistence_filter

            if lb_pool:
                changed = True
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                lb_pool = self.conn.network.update_pool(lb_pool, **attrs)
                self.exit_json(
                    changed=changed,
                    server_group=lb_pool.to_dict(),
                    id=lb_pool.id
                )

            if not protocol_filter and not listener_filter\
                    and not loadbalancer_filter and not lb_algorithm_filter:
                self.fail_json(msg='Protocol, Listener, Loadbalancer and LB Algorithm must be specified.')
            if self.ansible.check_mode:
                self.exit_json(changed=True)

            lb_pool = self.conn.network.create_pool(**attrs)
            changed = True
            self.exit_json(
                changed=changed,
                server_group=lb_pool.to_dict(),
                id=lb_pool.id
            )

        elif self.params['state'] == 'absent':
            changed = False
            if lb_pool:
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                self.conn.network.delete_pool(lb_pool)
                changed = True
            self.exit_json(changed=changed)


def main():
    module = LoadBalancerPoolModule()
    module()


if __name__ == '__main__':
    main()
