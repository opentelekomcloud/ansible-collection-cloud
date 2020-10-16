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
module: subnet
short_description: Create/Remove subnet from the OTC
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.4"
author: "Polina Gubina (@polina-gubina)"
description:
  - Create/Remove subnet from the OTC
options:
  allocation_pools:
    description:
      - Specifies the available IP address pool. For details, see the allocation_pool objects.
    type: list
    elements: str
  cidr:
    description:
      - Subnet cidr.
    type: str
    required: true
  description:
    description:
      - The subnet_info description.
    type: str
  gateway_ip:
    description:
      - Subnet gateway ip address.
    type: str
  dns_publish_fixed_ip:
    description:
      - Whether to publish DNS records for fixed IPs.
    type: bool
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
    required: true
  project_id:
    description:
      - Owner tenant ID.
    type: str
  segment_id:
    description:
      -  The subnet_info pool ID from which to obtain a CIDR.
    type: str
  subnet_pool_id:
    description:
      -  The subnet_info pool ID from which to obtain a CIDR.
    type: str
  use_default_pool_id:
    description:
      -  Whether to use the default subnet pool to obtain a CIDR.
    type: bool
  state:
    description:
      - Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
subnets:
  description: The subnet_info object list.
  type: complex
  returned: On Success.
  contains:
    id:
      description: Specifies the subnet_info ID.
      type: str
      sample: "4dae5bac-0925-4d5b-add8-cb6667b8"
    name:
      description: Specifies the subnet_info name.
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
      description: Specifies the ID of the network to which the subnet_info belongs.
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
      description: Specifies the time (UTC) when the subnet_info is created.
      type: str
    updated_at:
      description: Specifies the time (UTC) when the subnet_info is updated.
      type: str
'''

EXAMPLES = '''
# Get configs versions.
- subnet_info:
  register: subnets
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SubnetModule(OTCModule):
    argument_spec = dict(
        allocation_pools=dict(required=False, type='list', elements='str'),
        cidr=dict(required=True),
        description=dict(required=False),
        gateway_ip=dict(required=False),
        dns_publish_fixed_ip=dict(required=False, type='bool'),
        ip_version=dict(required=False, type='bool'),
        ipv6_address_mode=dict(required=False, type='bool'),
        ipv6_ra_mode=dict(required=False),
        is_dhcp_enabled=dict(required=False),
        name=dict(required=False),
        network_id=dict(required=True),
        project_id=dict(required=False),
        segment_id=dict(required=False),
        subnet_pool_id=dict(required=False),
        use_default_pool_id=dict(required=False, type='bool'),
        state=dict(required=False, default='present', choices=['present', 'absent'])
    )

    def run(self):

        allocation_pools = self.params['allocation_pools']
        cidr = self.params['cidr']
        description = self.params['description']
        gateway_ip = self.params['gateway_ip']
        dns_publish_fixed_ip = self.params['dns_publish_fixed_ip']
        ip_version = self.params['ip_version']
        ipv6_address_mode = self.params['ipv6_address_mode']
        ipv6_ra_mode = self.params['ipv6_ra_mode']
        is_dhcp_enabled = self.params['is_dhcp_enabled']
        name = self.params['name']
        network_id = self.params['network_id']
        segment_id = self.params['segment_id']
        subnet_pool_id = self.params['subnet_pool_id']
        use_default_pool_id = self.params['use_default_pool_id']
        state = self.params['state']

        changed = False

        subnet = self.conn.network.find_subnet(name, ignore_missing=True)

        if self.params['state'] == 'present':

            attrs = {}

            attrs['network_id'] = self.params['network_id']
            attrs['cidr'] = self.params['cidr']

            if allocation_pools:
                attrs['allocation_pools'] = self.params['allocation_pools']
            if description:
                attrs['description'] = self.params['description']
            if gateway_ip:
                attrs['gateway_ip'] = self.params['gateway_ip']
            if dns_publish_fixed_ip:
                attrs['dns_publish_fixed_ip'] = self.params['dns_publish_fixed_ip']
            if ip_version:
                attrs['ip_version'] = self.params['ip_version']
            if ipv6_address_mode:
                attrs['ipv6_address_mode'] = self.params['ipv6_address_mode']
            if ipv6_ra_mode:
                attrs['ipv6_ra_mode'] = self.params['ipv6_ra_mode']
            if name:
                attrs['name'] = self.params['name']
            if is_dhcp_enabled:
                attrs['is_dhcp_enabled'] = self.params['is_dhcp_enabled']
            if segment_id:
                attrs['segment_id'] = self.params['segment_id']
            if subnet_pool_id:
                attrs['subnet_pool_id'] = self.params['subnet_pool_id']
            if use_default_pool_id:
                attrs['use_default_pool_id'] = self.params['use_default_pool_id']

            subnet = self.conn.network.create_subnet(**attrs)
            changed = True
            self.exit_json(
                changed=changed,
                subnet=subnet
            )

        elif self.params['state'] == 'absent':
            subnet = self.conn.network.delete_subnet(subnet)
            changed = True
            self.exit_json(
                changed=changed
            )



def main():
    module = SubnetModule()
    module()


if __name__ == '__main__':
    main()
