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
module: vpc_route_info
short_description: Get information about vpc routes info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.2"
author: "Polina Gubina (@polina-gubina)"
description:
  - Get a generator of vpc routes info from the OTC.
options:
  route_id:
    description:
      - Route ID.
    type: str
  destination:
    description:
      -  Route destination address (CIDR).
    required: true
    type: str
  nexthop:
    description: 
      -  The next hop. If type is peering, it is the VPC peering connection ID
    required: true
    type: str
  type:
    description:
      -  Type of a route.
    required: true
    default: peering
    type: str
  vpc_id:
    description:
      -  ID of the VPC ID requesting for creating a route.
    required: true
    type: str
  state:
    description:
      -  ID of the VPC ID requesting for creating a route.
    choices: [present, absent]
    default: present
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''


RETURN = '''
id:
  description:  Route ID.
  type: str
  sample: "4dae5bac-0925-4d5b-add8-cb6667b8"
destination:
  description:  Destination address in the CIDR notation format.
  type: str
  sample: "192.168.200.0/24"
nexthop:
  description: The next hop. If type is peering, it is the VPC peering connection ID
  type: str
  sample: "7375f1cd-6fe1-4d47-8888-c5c5a64298d8"
type:
  description: The route type.
  type: str
  sample: "peering"
vpc_id:
  description:  The VPC of the route.
  type: dict
  sample: "4dae5bac-0725-2d5b-add8-cb6667b8"
tenant_id:
  description: Project id.
  type: str
  sample: "6ysa5bac-0925-4d5b-add8-cb6667b8"
'''

EXAMPLES = '''
# Create a vpc route.
- vpc_route:
    destination: "6ysa5bac-0925-6d5b-add8-cb6667b8"
    nexthop: "67sa5bac-0925-4p5b-add8-cb6667b8"
    type: "peering"
    vpc_id: "89sa5bac-0925-9h7b-add8-cb6667b8"
  register: vpc_route
  
# Delete vpc route 
- vpc_route:
    name: "peering2"
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VPCRoute(OTCModule):
    argument_spec = dict(
        name=dict(required=True, type='str'),
        state=dict(default='present', choices=['absent', 'present']),
        local_router=dict(type='str'),
        project_id_local=dict(type='str'),
        peer_router=dict(type='str'),
        project_id_peer=dict(type='str'),
        new_name=dict(type='str'),
        description=dict(type='str', default="")
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['local_router', 'project_id_local', 'peer_router', 'project_id_peer'])
        ],
        supports_check_mode=True
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
        name = self.params['name']
        local_router = self.params['local_router']
        project_id_local = self.params['project_id_local']
        peer_router = self.params['peer_router']
        project_id_peer = self.params['project_id_peer']
        new_name = self.params['new_name']
        description = self.params['description']

        changed = False
        vpc_peering = None

        vpc_peering = self.conn.vpc.find_peering(name, ignore_missing=True)

        if self.ansible.check_mode:
            self.exit_json(changed=self._system_state_change(vpc_peering))

        if new_name:
            attrs = {'name': new_name}
            if vpc_peering:
                if self.ansible.check_mode:
                    self.exit_json(changed=False)
                else:
                    updated_vpc_peering = self.conn.vpc.update_peering(vpc_peering, **attrs)
                    changed = True
                    self.exit_json(
                        changed=changed,
                        vpc_peering=updated_vpc_peering
                    )
            else:
                self.fail_json(
                    msg="A VPC peering with this name doesn't exist"
                )

        if self.params['state'] == 'present':

            local_vpc = self.conn.network.find_router(local_router)
            peer_vpc = self.conn.network.find_router(peer_router)

            local_vpc_id = local_vpc['id']
            peer_vpc_id = peer_vpc['id']

            if not vpc_peering:

                attrs = {
                    'name': name
                }

                local_vpc = {'vpc_id': local_vpc_id, 'project_id': project_id_local}
                attrs['local_vpc_info'] = local_vpc
                peer_vpc = {'vpc_id': peer_vpc_id, 'project_id': project_id_peer}
                attrs['peer_vpc_info'] = peer_vpc

                if description:
                    attrs['description'] = self.params['description']

                if self._check_peering(local_vpc_id, peer_vpc_id):
                    vpc_peering = self.conn.vpc.create_peering(**attrs)
                    changed = True

                    self.exit_json(
                        changed=changed,
                        vpc_peering=vpc_peering
                    )
                else:
                    self.fail_json(
                        msg="A VPC peering connection already exists between the two VPCs."
                    )
            else:
                self.fail_json(
                    msg="VPC peering with this name already exists"
                )

        elif self.params['state'] == 'absent':
            if vpc_peering:
                self.conn.vpc.delete_peering(vpc_peering)
                changed = True
                self.exit_json(
                    changed=changed,
                    result="Resource was deleted"
                )

            else:
                self.fail_json(
                    msg="Resource with this name doesn't exist"
                )


def main():
    module = VPCPeeringModule()
    module()


if __name__ == '__main__':
    main()
