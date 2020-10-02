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
module: lb_member
short_description:  Add/Delete a member for a pool in load balancer from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Add or Remove a member for a pool for Enhanced Load Balancer from the OTC load-balancer
    service(ELB).
options:
  state:
    description:
      - Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
  pool:
    description:
      - Specifies the ID or Name of the backend server group.
    type: str
    required: true
  name:
    description:
      - Specifies the backend server group name.
    type: str
    required: true
  address:
    description:
      - Specifies the private IP address of the backend server.
    type: str
    required: true
  protocol_port:
    description:
      - Specifies the port used by the backend server.
    type: int
    required: true
  subnet:
    description:
      - Specifies the ID of the subnet where the backend server works.
    type: str
    required: true
  admin_state_up:
    description:
      - Specifies the administrative status of the backend server.
    type: bool
  weight:
    description:
      - Specifies the backend server weight.
    type: int
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
lb_member:
  description: Specifies the member.
  type: complex
  returned: On Success.
  contains:
    id:
      description: Specifies the backend server ID.
      type: str
      sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
    name:
      description: Specifies the backend server name.
      type: str
      sample: "server_test"
    address:
      description: Specifies the private IP address of the backend server.
      type: str
      sample: "192.168.0.10"
    address:
      description: Specifies the private IP address of the backend server.
      type: str
      sample: "192.168.0.10"
    protocol_port:
      description: Specifies the port used by the backend server.
      type: int
      sample: 8080
    subnet_id:
      description: Specifies the ID of the subnet where the backend server works.
      type: str
    admin_state_up:
      description: Specifies the administrative status of the backend server.
      type: bool
    weight:
      description: Specifies the backend server weight.
      type: int
    operating_status:
      description: Specifies the health check result of the backend server.
      type: int
'''

EXAMPLES = '''
# Add a server group member to load balancer.
- lb_member:
    state: present
    name: member
    pool: pool

# Delete a server group member from load balancer.
- lb_member:
    state: absent
    name: member
    pool: pool
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LoadBalancerMemberModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        pool=dict(required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        lb_member = None
        attrs = {}
        changed = False
        lb_pool = self.conn.network.find_pool(name_or_id=self.params['pool'])
        lb_member = self.conn.network.find_pool_member(pool=lb_pool, name_or_id=self.params['name'])

        if self.params['state'] == 'present':

            if lb_member:
                changed = True
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                lb_pool = self.conn.network.update_pool_member(lb_member, **attrs)
                self.exit_json(
                    changed=changed,
                    server_group=lb_pool.to_dict(),
                    id=lb_pool.id
                )

            if self.ansible.check_mode:
                self.exit_json(changed=True)

            lb_member = self.conn.network.create_pool_member(**attrs)
            changed = True
            self.exit_json(
                changed=changed,
                server_group=lb_member.to_dict(),
                id=lb_member.id
            )

        elif self.params['state'] == 'absent':
            changed = False
            if lb_member:
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                self.conn.network.delete_pool_member(lb_member)
                changed = True
            self.exit_json(changed=changed)


def main():
    module = LoadBalancerMemberModule()
    module()


if __name__ == '__main__':
    main()
