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
module: router_info
short_description: Get router info from the OTC
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Polina Gubina (@Polina-Gubina)"
description:
  - Get router info from the OTC Router service.
options:
  description:
    description:
      - The description of a router.
    type: str
  flavor_id:
    description:
      - The ID of the flavor.
    type: str
  is_admin_state_up:
    description:
      - Router administrative state is up or not
    type: bool
  is_distributed:
    description:
      - The distributed state of a router.
    type: bool
  is_ha:
    description:
      - The highly-available state of a router.
    type: bool
  project_id:
    description:
      - The ID of the project this router is associated with.
    type: str
  status:
    description:
      - The status of the router.
    type: str
    choices: ["active", "down", "error"]
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
routers:
    description: List of router objects
    type: complex
    returned: On Success.
    contains:
        availability_zone_hints:
            description:  Availability zone hints to use when scheduling the router.
            type: list
        availability_zones:
            description: Availability zones for the router.
            type: list
        created_at:
            description: Timestamp when the router was created.
            type: str
        description:
            description: The router description.
            type: str
        external_gateway_info:
            description: The ``network_id``, for the external gateway.
            type: dict
        flavor_id:
            description: The ID of the flavor.
            type: str
        is_admin_state_up:
            description: The administrative state of the router.
            type: bool
        is_distributed:
            description: The distributed state of the router.
            type: bool
        is_ha:
            description: The highly-available state of the router.
            type: bool
        name:
            description: The router name.
            type: str
        project_id:
            description: The ID of the project this router is associated with.
            type: str
        revision_number:
            description: Revision number of the router.
            type: int
        routes:
            description: The extra routes configuration for the router.
            type: list
        status:
            description: The router status.
            type: str
        updated_at:
            description: Timestamp when the router was created.
            type: str
'''

EXAMPLES = '''
# Get a list of existing routers.
- router_info:
  register: router_info
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class RouteInfoModule(OTCModule):
    argument_spec = dict(
        description=dict(required=False),
        flavor_id=dict(required=False),
        is_admin_state_up=dict(required=False, type='bool'),
        is_distributed=dict(required=False, type='bool'),
        is_ha=dict(required=False, type='bool'),
        project_id=dict(required=False),
        status=dict(required=False, choices=["active", "down", "error"]),
    )

    def run(self):

        description_filter = self.params['description']
        flavor_id_filter = self.params['flavor_id']
        is_admin_state_up_filter = self.params['is_admin_state_up']
        is_distributed_filter = self.params['is_distributed']
        is_ha_filter = self.params['is_ha']
        project_id_filter = self.params['project_id']
        status_filter = self.params['status']

        data = []
        query = {}
        if description_filter:
            query['description'] = description_filter
        if flavor_id_filter:
            query['flavor_id'] = flavor_id_filter
        if is_admin_state_up_filter:
            query['is_admin_state_up'] = is_admin_state_up_filter
        if is_distributed_filter:
            query['is_distributed'] = is_distributed_filter
        if is_ha_filter:
            query['is_ha'] = is_ha_filter
        if project_id_filter:
            query['project_id'] = project_id_filter
        if status_filter:
            query['status'] = status_filter.upper()

        for raw in self.conn.network.routers(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit_json(
            changed=False,
            routers=data
        )


def main():
    module = RouteInfoModule()
    module()


if __name__ == '__main__':
    main()
