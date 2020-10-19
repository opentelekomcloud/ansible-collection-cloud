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
module: router
short_description: Add/Update/Delete vpc peering connection from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Polina Gubina (@polina-gubina)"
description:
  - Add or Remove router from the OTC.
options:
  availability_zone_hints:
    description:
      - Availability zone hints to use when scheduling the router.
    type: list
    elements: str
  router_id:
    description:
      - The router id.
    type: str
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
      - Router administrative state is up or not.
    type: bool
  is_distributed:
    description:
      - The distributed state of a router.
    type: bool
  is_ha:
    description:
      - The highly-available state of a router.
    type: bool
  name:
    description:
      - The router name.
    type: str
  project_id:
    description:
      - The ID of the project this router is associated with.
    type: str
  state:
    description:
      - Whether resource should be present or absent.
    choices: ['present', 'absent']
    default: 'present'
    type: str
  external_gateway_info:
    description:
      - Specifies the external gateway.
    type: dict
    elements: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
router:
    description: Dictionary describing the router.
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
# Create a router.
- router:
    name: "test-router"
    is_admin_state_up: "true
    flavor_id: "959db9b6017d4a1fa1c6fd17b6820f55"

# Change name of the router
- router:
    router_id: "563db9b60564r4a1fa1c6fd17b6820f45"
    name: "test-router-2"

# Delete a router
- router:
    name: "test-router-2"
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class RouterModule(OTCModule):
    argument_spec = dict(
        availability_zone_hints=dict(required=False),
        availability_zones=dict(required=False),
        name=dict(required=False),
        router_id=dict(required=False),
        description=dict(required=False),
        flavor_id=dict(required=False),
        is_admin_state_up=dict(required=False, type='bool'),
        is_distributed=dict(required=False, type='bool'),
        is_ha=dict(required=False, type='bool'),
        project_id=dict(required=False),
        external_gateway_info=dict(required=False, type='dict', elements='str'),
        state=dict(required=False, default='present', choices=['present', 'absent'])
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        router_id = self.params['router_id']
        availability_zone_hints = self.params['availability_zone_hints']
        name = self.params['name']
        description = self.params['description']
        is_admin_state_up = self.params['is_admin_state_up']
        is_distributed = self.params['is_distributed']
        flavor_id = self.params['flavor_id']
        is_ha = self.params['is_ha']
        project_id = self.params['project_id']
        external_gateway_info = self.params['external_gateway_info']

        changed = False
        router = None

        if router_id:
            router = self.conn.network.find_router(router_id, ignore_missing=True)
        else:
            router = self.conn.network.find_router(name, ignore_missing=True)

        if self.params['state'] == 'present':

            attrs = {}

            if availability_zone_hints:
                attrs['availability_zone_hints'] = self.params['availability_zone_hints']
            if router_id:
                attrs['router_id'] = self.params['router_id']
            if description:
                attrs['description'] = self.params['description']
            if flavor_id:
                attrs['flavor_id'] = self.params['flavor_id']
            if is_admin_state_up:
                attrs['is_admin_state_up'] = self.params['is_admin_state_up']
            if is_distributed:
                attrs['ipv6_ra_mode'] = self.params['is_distributed']
            if is_ha:
                attrs['is_ha'] = self.params['is_ha']
            if name:
                attrs['name'] = self.params['name']
            if project_id:
                attrs['project_id'] = self.params['project_id']
            if external_gateway_info:
                attrs['external_gateway_info'] = self.params['external_gateway_info']

            if not router:
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                router = self.conn.network.create_router(**attrs)
                changed = True
                self.exit_json(
                    changed=changed,
                    router=router
                )

            else:
                changed = True
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                self.conn.network.update_router(router, **attrs)
                self.exit_json(
                    changed=changed,
                    router=router
                )

        elif self.params['state'] == 'absent':
            if router:
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                self.conn.network.delete_router(router)
                changed = True
                self.exit_json(
                    changed=changed,
                    result="Resource was deleted"
                )

            else:
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                self.fail_json(
                    msg="Resource with this name doesn't exist"
                )


def main():
    module = RouterModule()
    module()


if __name__ == '__main__':
    main()