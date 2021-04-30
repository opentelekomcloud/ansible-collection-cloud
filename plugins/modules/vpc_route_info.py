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
version_added: "0.2.0"
author: "Polina Gubina (@polina-gubina)"
description:
  - Get a generator of vpc routes info from the OTC.
options:
  id:
    description:
      - Route ID.
    type: str
  project_id:
    description:
      - Project id.
    type: str
  router:
    description:
      - Router id or name.
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
    router_id:
      description:  The router of the route.
      type: dict
      sample: "4dae5bac-0725-2d5b-add8-cb6667b8"
    project_id:
      description: Project id.
      type: str
      sample: "6ysa5bac-0925-4d5b-add8-cb6667b8"
'''

EXAMPLES = '''
# Get configs versions.
- vpc_route_info:
    router: "6ysa5bac-0925-4d5b-add8-cb6667b8"
  register: vpc_routes
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VPCRouteInfoModule(OTCModule):
    argument_spec = dict(
        id=dict(required=False),
        project_id=dict(required=False),
        router=dict(required=False),
        destination=dict(required=False),
        type=dict(default='peering', required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        id_filter = self.params['id']
        project_id_filter = self.params['project_id']
        router_filter = self.params['router']
        destination_filter = self.params['destination']
        type_filter = self.params['type']

        data = []
        query = {}
        if id_filter:
            query['id'] = id_filter
        if project_id_filter:
            query['project_id'] = project_id_filter
        if router_filter:
            query['vpc_id'] = self.conn.network.find_router(router_filter, ignore_missing=True).id
            if not query['vpc_id']:
                self.fail_json(msg='Router not found')
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
    module = VPCRouteInfoModule()
    module()


if __name__ == '__main__':
    main()
