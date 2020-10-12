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
module: vpc_route
short_description: Creation and deleting of vpc routes
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Polina Gubina (@polina-gubina)"    `
description:
  - Creation and deleting of vpc routes.
options:
  route_id:
    description: Route ID.
    type: str
  destination:
    description:  Route destination address (CIDR).
    type: str
  nexthop:
    description: The next hop. If type is peering, it is the VPC peering connection ID
    type: str
  type:
    description: Type of a route.
    default: peering
    type: str
  vpc_id:
    description: ID of the VPC ID requesting for creating a route.
    type: str
  state:
    description: ID of the VPC ID requesting for creating a route.
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
    type: str
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


class VPCRouteModule(OTCModule):
    argument_spec = dict(
        route_id=dict(type='str'),
        destination=dict(type='str'),
        nexthop=dict(type='str'),
        type=dict(default='peering', type='str'),
        vpc_id=dict(type='str'),
        state=dict(default='present', choices=['present', 'absent']),
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['destination', 'nexthop', 'vpc_id'])
        ],
        supports_check_mode=True
    )

    def _check_route(self, destination, vpc_id):

        query = {}
        result = True

        query['destination'] = destination
        query['vpc_id'] = vpc_id
        data = []

        for raw in self.conn.vpc.routes(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        if data:
            result = False

        return result

    def _check_route_by_id(self, route_id):

        result = True

        try:
            vpc_route = self.conn.vpc.get_route(route_id)  # noqa: F841
        except self.sdk.exceptions.ResourceNotFound:
            result = False

        return result

    def run(self):

        if self.params['state'] == 'present':
            attrs = {}
            attrs['destination'] = self.params['destination']
            attrs['nexthop'] = self.params['nexthop']
            attrs['type'] = self.params['type']
            attrs['vpc_id'] = self.params['vpc_id']

            check = self._check_route(attrs['destination'], attrs['vpc_id'])

            if self.ansible.check_mode:
                self.exit_json(changed=check)

            if check:
                vpc_route = self.conn.vpc.add_route(**attrs)
                changed = True
                self.exit_json(
                    changed=changed,
                    vpc_route=vpc_route
                )

            else:
                self.fail_json(
                    msg="Resource with this destination already exists"
                )

        elif self.params['state'] == 'absent':
            route_id = self.params['route_id']

            check = self._check_route_by_id(route_id)
            if self.ansible.check_mode:
                self.exit_json(changed=check)

            if check:
                self.conn.vpc.delete_route(route_id)
            else:
                self.fail_json(
                    msg="Resource with this id doesn't exist"
                )
            changed = True
            self.exit_json(
                changed=changed,
                result="Resource was deleted"
            )


def main():
    module = VPCRouteModule()
    module()


if __name__ == '__main__':
    main()
