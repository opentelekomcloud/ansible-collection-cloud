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
  id:
    description:
      - Route ID.
    type: str
  tenant_id:
    description:
      - Tenant id.
    type: str
  vpc_id:
    description:
      - VPC ID.
    type: str
  destination:
    description:
      -  Route destination address (CIDR).
    type: str
  type:
    description:
      -  Type of a route.
    default: peering
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
vpc_routes:
  description: The VPC route object list.
  type: complex
  returned: On Success.
  contains:
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
# Get configs versions.
- vpc_route_info:
    vpc_id: "6ysa5bac-0925-4d5b-add8-cb6667b8"
  register: vpc_routes
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VPCPeeringInfoModule(OTCModule):
    argument_spec = dict(
        id=dict(required=False),
        tenant_id=dict(required=False),
        vpc_id=dict(required=False),
        destination=dict(required=False),
        type=dict(required=False)
    )

    def run(self):

        id_filter = self.params['id']
        tenant_id_filter = self.params['tenant_id']
        vpc_id_filter = self.params['vpc_id']
        destination_filter = self.params['destination']
        type_filter = self.params['type']

        data = []
        query = {}
        if id_filter:
            query['id'] = id_filter
        if tenant_id_filter:
            query['status'] = tenant_id_filter
        if vpc_id_filter:
            query['project_id'] = vpc_id_filter
        if destination_filter:
            query['destination'] = destination_filter
        if type_filter:
            query['type'] = type_filter

        for raw in self.conn.vpc.routes(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit_json(
            changed=False,
            vpc_routes=data
        )


def main():
    module = VPCPeeringInfoModule()
    module()


if __name__ == '__main__':
    main()
