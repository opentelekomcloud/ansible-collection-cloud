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
module: vpn_services_info
short_description: Query VPN services.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.2.0"
author: "Irina Pereiaslavskaia (@irina-pereiaslavskaia)"
description:
  - This module is used to query VPN services.
options:
  admin_state_up:
    description: Specifies the administrative status.
    type: bool
  description:
    description: Provides supplementary information about the VPN service.
    type: str
  external_v4_ip:
    description: Specifies the IPv4 address of the VPN service external gateway.
    type: str
  external_v6_ip:
    description: Specifies the IPv6 address of the VPN service external gateway.
    type: str
  router_id:
    description: Specifies the router ID.
    type: str
  status:
    description: Specifies whether the VPN service is currently operational.
    choices: [active, down, build, error, pending_create, pending_update, pending_delete]
    type: str
  subnet_id:
    description: Specifies the subnet ID
    type: str
  tenant_id:
    description: Specifies the project ID
    type: str
  vpn_service:
    description: Name or ID of VPN service.
    type: str
'''

RETURN = '''
vpnservices:
  description: Specifies the VPN service object
  type: complex
  returned: On Success
  contains:
    admin_state_up:
      description: Specifies the administrative status.
      type: bool
      sample: true
    description:
      description: Provides supplementary information about the VPN service.
      type: str
      sample: "This is description"
    external_v4_ip:
      description: Specifies the IPv4 address of the VPN service external gateway.
      type: str
      sample: "172.32.1.11"
    external_v6_ip:
      description: Specifies the IPv6 address of the VPN service external gateway.
      type: str
      sample: "2001:db8::1"
    id:
      description: Specifies the VPN service ID.
      type: str
      sample: "5c561d9d-eaea-45f6-ae3e-08d1a7080828"
    name:
      description: Specifies the VPN service name.
      type: str
      sample: "test_vpn_service"
    router_id:
      description: Specifies the router ID.
      type: str
      sample: "66e3b16c-8ce5-40fb-bb49-ab6d8dc3f2aa"
    status:
      description: Specifies whether the VPN service is currently operational.
      choices: [active, down, build, error, pending_create, pending_update, pending_delete]
      type: str
      sample: "PENDING_CREATE"
    subnet_id:
      description: Specifies the subnet ID
      type: str
    tenant_id:
      description: Specifies the project ID
      type: str
      sample: "10039663455a446d8ba2cbb058b0f578"
'''

EXAMPLES = '''
# Get VPN Services (all parameters are specified)
- opentelekomcloud.cloud.vpn_services_info:
    admin_state_up: true
    description: "This is description"
    external_v4_ip: "172.32.1.11"
    external_v6_ip: "2001:db8::1"
    router_id: "66e3b16c-8ce5-40fb-bb49-ab6d8dc3f2aa"
    status: "PENDING_CREATE"
    subnet_id: "14067794-975d-461e-b502-dd40c0383d26"
    tenant_id: "959db9b6000d4a1fa1c6fd17b6820f00"
    vpn_service: "test_vpn"
  register: vpn_services
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VpnServicesInfoModule(OTCModule):
    argument_spec = dict(
        admin_state_up=dict(type='bool', required=False),
        description=dict(type='str', required=False),
        external_v4_ip=dict(type='str', required=False),
        external_v6_ip=dict(type='str', required=False),
        router_id=dict(type='str', requiered=False),
        status=dict(type='str', required=False),
        subnet_id=dict(type='str', required=False),
        tenant_id=dict(type='str', required=False),
        vpn_service=dict(type='str', required=False)
    )

    def run(self):
        admin_state_up = self.params['admin_state_up']
        description = self.params['description']
        external_v4_ip = self.params['external_v4_ip']
        external_v6_ip = self.params['external_v6_ip']
        router_id = self.params['router_id']
        status = self.params['status']
        subnet_id = self.params['subnet_id']
        tenant_id = self.params['tenant_id']
        vpn_service = self.params['vpn_service']

        data = []
        query = {}
        if vpn_service:
            vpn = self.conn.network.find_vpn(name_or_id=vpn_service)
            if vpn:
                query['vpn_service'] = vpn
        if subnet_id:
            subnet = self.conn.network.find_subnet(name_or_id=subnet_id)
            if subnet:
                query['subnet_id'] = subnet.id
        if router_id:
            router = self.conn.network.find_router(name_or_id=router_id)
            if router:
                query['router_id'] = router.id
        if admin_state_up:
            query['admin_state_up'] = admin_state_up
        if description:
            query['description'] = description
        if external_v4_ip:
            query['external_v4_ip'] = external_v4_ip
        if external_v6_ip:
            query['external_v6_ip'] = external_v6_ip
        if tenant_id:
            query['tenant_id'] = tenant_id
        if status:
            query['status'] = status.upper()

        for raw in self.conn.network.vpn_services(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            vpn_services=data
        )


def main():
    module = VpnServicesInfoModule()
    module()


if __name__ == '__main__':
    main()
