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
module: vpn_service
short_description: Manage VPN
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.0"
author: "Polina Gubina (@Polina-Gubina)"
description:
    - Manage VPN from the OTC.
options:
  subnet:
    description:
      - Specifies the subnet name or ID.
    type: str
  router:
    description:
      - Specifies the router name or ID.
    type: str
    required: false
  name_or_id:
    description:
      - Specifies the VPN service name or id. Name can be updated.
    type: str
    required: false
  admin_state_up:
    description:
      - Specifies the administrative status.
    type: str
  project_id:
    description:
      - Specifies the project ID.
    type: str
  description:
    description:
      - Provides supplementary information about the VPN service. Can be changed for existing vpn service.
    type: str
  state:
    description:
      - Should resource be present or absent.
    type: str
    choices: [present, absent]
    default: present

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
vpn:
  description: Information about created vpn service.
  type: complex
  returned: On Success.
  contains:
    router_id:
      description: Specifies the router ID.
      type: str
      sample: "5d9910d4-e04b-49db-9699-ab3bd368bc04"
    status:
      description: Specifies whether the VPN service is currently operational.\
        The value can be ACTIVE, DOWN, BUILD, ERROR, PENDING_CREATE, PENDING_UPDATE, or PENDING_DELETE.
      type: str
      sample: "ACTIVE"
    name:
      description: Specifies the VPN service name.
      type: str
      sample: "new-vpn"
    external_v6_ip:
      description: Specifies the IPv6 address of the VPN service external gateway.
      type: str
      sample: "2001:db8::1"
    admin_state_up:
      description: Specifies the administrative status. The value can be true or false.
      type: bool
      sample: "true"
    subnet_id:
      description: Specifies the subnet ID.
      type: str
      sample: "df9910d4-e04b-49db-9699-ab3bd368bc04"
    project_id:
      description: Specifies the project ID.
      type: str
      sample: "5d9910d4-e04b-49db-9699-ab3bd368bc04"
    external_v4_ip:
      description: Specifies the IPv4 address of the VPN service external gateway.
      type: str
      sample: "80.158.3.5"
    id:
      description: Specifies the VPN service ID.
      type: str
      sample: "5d9910d4-e04b-49db-9699-ab3bd368bc04"
    description:
      description: Provides supplementary information about the VPN service.
      type: str
      sample: "description of vpn"
'''

EXAMPLES = '''
- name: Create a new vpn
  opentelekomcloud.cloud.vpn_service:
    router: "my-router"
    name: "my-vpn"
    subnet: "my-subnet"

- name: Update vpn
  opentelekomcloud.cloud.vpn_service:
    router: "my-router"
    name: "new_name_for_vpn"
    service_id: "5d9910d4-e04b-49db-9699-ab3bd368bc04"
    description: "new description"

- name: Delete vpn by name
  opentelekomcloud.cloud.vpn_service:
    name: "my-vpn"
    state: absent

- name: Delete vpn by id
  opentelekomcloud.cloud.vpn_service:
    service_id: "5d9910d4-e04b-49db-9699-ab3bd368bc04"
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VPNModule(OTCModule):
    argument_spec = dict(
        subnet=dict(required=False),
        router=dict(required=False),
        name_or_id=dict(required=False),
        admin_state_up=dict(required=False),
        project_id=dict(required=False),
        description=dict(required=False),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        query = {}

        name_or_id = self.params['name_or_id']
        subnet = self.params['subnet']
        router = self.params['router']
        project_id = self.params['project_id']
        description = self.params['description']
        state = self.params['state']

        existing_vpn = None
        updated_vpn = None
        created_vpn = None

        if project_id:
            query['project_id'] = project_id

        if description:
            query['description'] = description

        if name_or_id:
            existing_vpn = self.conn.network.find_vpn_service(name_or_id=name_or_id)

        if state == 'present':

            if existing_vpn:
                if not self.ansible.check_mode:
                    updated_vpn = self.conn.network.update_vpn_service(existing_vpn, **query)
                self.exit(changed=True, vpn=updated_vpn)

            if name_or_id:
                query['name'] = name_or_id

            if subnet:
                try:
                    subnet_id = self.conn.network.find_subnet(name_or_id=subnet, ignore_missing=False).id
                    query['subnet_id'] = subnet_id
                except self.sdk.exceptions.ResourceNotFound:
                    self.fail_json("Subnet not found")

            if router:
                try:
                    router_id = self.conn.vpc.find_vpc(name_or_id=router, ignore_missing=False).id
                    query['router_id'] = router_id
                except self.sdk.exceptions.ResourceNotFound:
                    self.fail_json("Router not found")
            else:
                self.fail_json(msg='Router is mandatory for creation')

            if not self.ansible.check_mode:
                created_vpn = self.conn.network.create_vpn_service(**query)
            self.exit(changed=True, vpn=created_vpn)

        else:
            if existing_vpn:
                if not self.ansible.check_mode:
                    self.conn.network.delete_vpn_service(existing_vpn, ignore_missing=False)
                    self.exit_json(changed=True)
            self.exit_json(changed=False)


def main():
    module = VPNModule()
    module()


if __name__ == '__main__':
    main()
