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
  name:
    description:
      - Specifies the backend server name.
    type: str
    required: true
  address:
    description:
      - Specifies the private IP address of the backend server.
    type: str
  protocol_port:
    description:
      - Specifies the port used by the backend server.
    type: int
  subnet:
    description:
      - Specifies the ID or Name of the subnet where the backend server works.
    type: str
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
member:
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
    pool: "{{ pool }}"
    address: "{{ server_address }}"
    subnet: "{{ subnet_name_id }}"
    protocol_port: 8080

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
        state=dict(default='present', choices=['absent', 'present']),
        pool=dict(required=False),
        address=dict(required=False, type='str'),
        protocol_port=dict(required=False, type='int'),
        subnet=dict(required=False, type='str'),
        admin_state_up=dict(required=False, type='bool'),
        weight=dict(required=False, type='int')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        name_filter = self.params['name']
        address_filter = self.params['address']
        protocol_port_filter = self.params['protocol_port']
        subnet_filter = self.params['subnet']
        admin_state_filter = self.params['admin_state_up']
        weight_filter = self.params['weight']
        pool_filter = self.params['pool']

        lb_pool = None
        lb_member = None
        attrs = {}
        changed = False
        if pool_filter:
            lb_pool = self.conn.network.find_pool(name_or_id=pool_filter)
        if lb_pool:
            lb_member = self.conn.network.find_pool_member(pool=lb_pool, name_or_id=self.params['name'])

        if self.params['state'] == 'present':
            if name_filter:
                attrs['name'] = name_filter
            if admin_state_filter:
                attrs['admin_state_up'] = admin_state_filter
            if weight_filter:
                attrs['weight'] = weight_filter
            if address_filter:
                attrs['address'] = address_filter
            if protocol_port_filter:
                attrs['protocol_port'] = protocol_port_filter
            if subnet_filter:
                subnet = self.conn.network.find_subnet(name_or_id=subnet_filter)
                attrs['subnet_id'] = subnet.id

            if lb_member and lb_pool:
                mattrs = {}
                changed = False
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                if admin_state_filter:
                    if lb_member.is_admin_state_up != admin_state_filter:
                        mattrs['admin_state_up'] = admin_state_filter
                        changed = True
                if weight_filter:
                    if lb_member.weight != weight_filter:
                        mattrs['weight'] = weight_filter
                        changed = True
                lb_member = self.conn.network.update_pool_member(pool_member=lb_member, pool=lb_pool, **mattrs)
                self.exit_json(
                    changed=changed,
                    member=lb_member.to_dict(),
                    id=lb_member.id
                )

            if not address_filter and not protocol_port_filter and not subnet_filter:
                self.fail_json(msg='Address, protocol port and subnet must be specified.')
            if not lb_pool:
                self.fail_json(msg='Pool must be specified.')
            if self.ansible.check_mode:
                self.exit_json(changed=True)

            lb_member = self.conn.network.create_pool_member(pool=lb_pool, **attrs)
            changed = True
            self.exit_json(
                changed=changed,
                member=lb_member.to_dict(),
                id=lb_member.id
            )

        elif self.params['state'] == 'absent':
            changed = False
            if lb_member and lb_pool:
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                self.conn.network.delete_pool_member(pool_member=lb_member, pool=lb_pool)
                changed = True
            self.exit_json(changed=changed)


def main():
    module = LoadBalancerMemberModule()
    module()


if __name__ == '__main__':
    main()
