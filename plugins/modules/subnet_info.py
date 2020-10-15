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
module: subnet_info
short_description: Get information about subnets from the OTC
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.4"
author: "Polina Gubina (@polina-gubina)"
description:
  - Get subnets info from the OTC.
options:
  cidr:
    description:
      - Subnet cidr.
    type: str
  description:
    description:
      - The subnet description.
    type: str
  gateway_ip:
    description:
      - Subnet gateway ip address.
    type: str
  ip_version:
    description:
      - Subnet ip address version.
    type: str
  ipv6_address_mode:
    description:
      - The ipv6 address mode.
    type: str
  ipv6_ra_mode:
    description:
      - The IPv6 router advertisement mode.
    type: str
  is_dhcp_enabled:
    description:
      - Subnet has DHCP enabled.
    type: bool
  name:
    description:
      - Subnet name.
    type: str
  network_id:
    description:
      - ID of network that owns the subnets.
    type: str
  project_id:
    description:
      - Owner tenant ID.
    type: str
  subnet_pool_id:
    description:
      -  The subnet pool ID from which to obtain a CIDR.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
subnets:
  description: The subnet object list.
  type: complex
  returned: On Success.
  contains:
    id:
      description: Specifies the subnet ID.
      type: str
      sample: "4dae5bac-0925-4d5b-add8-cb6667b8"
    name:
      description: Specifies the subnet name.
      type: str
      sample: "subnet1"
    ip_version:
      description: Specifies the IP address version.
      type: int
    ipv6_address_mode:
      description: Specifies the IPv6 addressing mode.
      type: str
    ipv6_ra_mode:
      description: Specifies the IPv6 route broadcast mode.
      type: str
    network_id:
      description: Specifies the ID of the network to which the subnet belongs.
      type: str
    cidr:
      description: Specifies the CIDR format.
      type: str
      sample: "10.0.0.0/8"
    gateway_ip:
      description: The gateway IP address cannot conflict with IP addresses configured for allocation_pools.
      type: str
    allocation_pools:
      description: Specifies available IP address pools.
      type: list
    dns_nameservers:
      description: Specifies the DNS server address.
      type: list
    host_routes:
      description: Specifies the static VM routes.
      type: list
    tenant_id:
      description: Specifies the project ID.
      type: str
    enable_dhcp:
      description: Specifies whether to enable the DHCP function.
      type: bool
    project_id:
      description: Specifies the project ID.
      type: str
    created_at:
      description: Specifies the time (UTC) when the subnet is created.
      type: str
    updated_at:
      description: Specifies the time (UTC) when the subnet is updated.
      type: str
'''

EXAMPLES = '''
# Get configs versions.
- subnet_info:
  register: subnets
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SubnetInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
        status=dict(required=False, choices=['pending_acceptance', 'rejected', 'expired', 'deleted', 'active']),
        project_id=dict(required=False),
        router=dict(required=False),
    )

    def run(self):

        name_filter = self.params['name']
        status_filter = self.params['status']
        project_id_filter = self.params['project_id']
        router = self.params['router']

        data = []
        query = {}
        if name_filter:
            query['name'] = name_filter
        if status_filter:
            query['status'] = status_filter.upper()
        if project_id_filter:
            query['project_id'] = project_id_filter
        if router:
            router_obj = self.conn.network.find_router(router)
            query['vpc_id'] = router_obj['id']

        for raw in self.conn.vpc.peerings(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit_json(
            changed=False,
            vpc_peerings=data
        )


def main():
    module = SubnetInfoModule()
    module()


if __name__ == '__main__':
    main()

