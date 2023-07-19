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
module: vlb_loadbalancer_info
short_description: Add/Delete load balancer from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.14.0"
author: "Polina Gubina (@polina-gubina)"
description:
  - Get info about Dedicated Load Balancer from the OTC service(VLB).
options:
  name_or_id:
    description:
      - Specifies the load balancer name or ID.
    type: str
  description:
    description:
      - Provides supplementary information about the load balancer.
    type: str
  provisioning_status:
    description:
      - Specifies the provisioning status of the load balancer. The value can
      only be ACTIVE, indicating that the load balancer is provisioned
      successfully.
    type: str
  operating_status:
    description:
      - Specifies the operating status of the load balancer. The value can only
      be ONLINE, indicating that the load balancer is working normally.
    type: str
  vpc_id:
    description:
      - Specifies the ID of the VPC where the load balancer works.
    type: str
  vip_port_id:
    description:
      - Specifies the ID of the port bound to the virtual IP
      address of the load balancer.
    type: str
  vip_address:
    description:
      - Specifies the virtual IP address bound to the load balancer.
    type: str
  vip_subnet_cidr_id:
    description:
      - Specifies the ID of the subnet where the load balancer works.
    type: str
  l4_flavor_id:
    description:
      - Specifies the ID of the flavor at Layer 4.
    type: str
  l4_scale_flavor_id:
    description:
      - Specifies the elastic flavor that is reserved for now.
    type: str
  availability_zone_list:
    description:
      - Specifies the list of AZs where the load balancer is created.
      You can query the AZs by calling the API (/v3/{project_id}/elb/availability-zones).
    type: list
    elements: str
  eips:
    description:
      - Specifies the EIP bound to the load balancer.
    type: list
    elements: str
  l7_flavor_id:
    description:
      - Specifies the ID of the flavor at Layer 7.
    type: str
  l7_scale_flavor_id:
    description:
      - Specifies the elastic flavor that is reserved for now.
    type: str
  member_device_id:
    description:
      - Specifies the ID of the cloud server that serves as a backend server.
      This parameter is used only as a query condition and is not included in
      the response.
    type: str
  member_address:
    description:
      - Specifies the private IP address of the backend server.
    type: str
  publicips:
    description:
      - Specifies the public IP address bound to the load balancer.
    type: list
    elements: str
  ip_version:
    description:
      - Specifies the IP version. The value can be only 4 (IPv4).
    type: int
  elb_virsubnet_type:
    description:
      - Specifies the type of the subnet on the downstream plane.
      - ipv4 IPv4 subnets.
      - dualstack subnets that support IPv4/IPv6 dual stack.
      - IPv6 is unsupported. The value cannot be 6.
    type: str
  marker:
    description:
      - Specifies the ID of the last record on the previous page.
      - This parameter must be used together with limit.
      - If this parameter is not specified, the first page will be queried.
      - This parameter cannot be left blank or set to an invalid ID.
    type: str
  limit:
    description:
      - Specifies the number of records on each page. Minimum 0. Maximum: 2000.
    type: int
  page_reverse:
    description:
      - Specifies the page direction.
      - Default is false.
      - This parameter must be used together with limit.
      - The last page in the list requested with page_reverse set to false
      will not contain the "next" link, and the last page in the list
      requested with page_reverse set to true will not contain the
      "previous" link.
    type: bool
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
loadbalancer:
  description: Dictionary describing the load balancer.
  returned: On success when C(state=present)
  type: complex
  contains:
    id:
      description: Unique UUID.
      type: str
    name:
      description: Specifies the name of the load balancer.
      type: str
    description:
      description: Provides supplementary information about the load balancer.
      type: str
    provisioning_status:
      description:
        - Specifies the provisioning status of the load balancer.
        - The value can only be ACTIVE.
      type: str
    provider:
      description:
        - Specifies the provider of the load balancer.
        The value can only be vlb.
      type: str
    pools:
      description:
        - Lists the IDs of backend server groups associated with
        the load balancer.
      type: list
      elements: dict
      contains:
        id:
          description: ID of the pool.
          type: str
    listeners:
      description: Lists the IDs of listeners added to the load balancer.
      type: list
      elements: dict
      contains:
        id:
          description: ID of the listener.
          type: str
    operating_status:
      description:
        - Specifies the operating status of the load balancer.
        The value can only be ONLINE.
      type: str
    vip_address:
      description:
        - Specifies the private IPv4 address bound to the load balancer.
      type: str
    vip_subnet_cidr_id:
      description:
        - Specifies the ID of the IPv4 subnet where the load balancer works.
      type: str
    project_id:
      description: Specifies the project ID of the load balancer.
      type: str
    vip_port_id:
      description:
        - Specifies the ID of the port bound to the virtual IP address
        (the value of vip_address) of the load balancer.
      type: str
    tags:
      description: Lists the tags added to the load balancer.
      type: list
      elements: dict
      contains:
        key:
          description: Key of the tag.
          type: str
        value:
          description: Value of the tag.
          type: str
    created_at:
      description: Specifies the time when the load balancer was created.
      type: str
    updated_at:
      description: Specifies the time when the load balancer was updated.
      type: str
    guaranteed:
      description:
        - Specifies whether the load balancer is a dedicated load balancer.
        - The value can be true or false. true indicates a dedicated load
        balancer, and false indicates a shared load balancer. When dedicated
        load balancers are launched in the eu-de region, either true or false
        will be returned when you use the API to query or update
        a load balancer.
      type: bool
    vpc_id:
      description: Specifies the ID of the VPC where the load balancer works.
      type: str
    availability_zone_list:
      description:
        - Specifies the list of AZs where the load balancer is created.
      type: list
    eips:
      description: Specifies the EIP bound to the load balancer.
      type: list
      elements: dict
      contains:
        eip_id:
          description: Specifies the EIP ID.
          type: str
        eip_address:
          description: Specifies the specific IP address.
          type: str
        ip_version:
          description:
            - Specifies the IP version. 4 indicates IPv4,
            and 6 indicates IPv6.
          type: int
    l4_flavor_id:
      description:
        - Specifies the Layer-4 flavor.
      type: str
    l4_scale_flavor_id:
      description:
        - Specifies the reserved Layer 4 flavor.
      type: str
    l7_flavor_id:
      description:
        - Specifies the Layer-7 flavor.
      type: str
    l7_scale_flavor_id:
      description:
        - Specifies the reserved Layer 7 flavor.
      type: str
    publicips:
      description:
        - Specifies the EIP bound to the load balancer.
      type: list
      elements: dict
      contains:
        publicip_id:
          description: Specifies the EIP ID.
          type: str
        publicip_address:
          description: Specifies the IP address.
          type: str
        ip_version:
          description:
            - Specifies the IP version. The value can be 4 (IPv4) or 6 (IPv6).
          type: int
    elb_virsubnet_ids:
      description:
        - Specifies the ID of the subnet on the downstream plane.
        - The ports used by the load balancer dynamically occupy IP addresses.
        in the subnet.
      type: list
    elb_virsubnet_type:
      description:
        - Specifies the type of the subnet on the downstream plane.
        - ipv4 IPv4 subnets.
        - dualstack: subnets that support IPv4/IPv6 dual stack.
      type: str

'''

EXAMPLES = '''
# Get all loadbalancers
- opentelekomcloud.cloud.vlb_loadbalancer_info:
  register: loadbalancers

# Get filtered loadbalancers
- opentelekomcloud.cloud.loadbalancer:
    vpc_id: 16dbd25d-c55c-405b-9e56-11b03e7e7dc1
    eips: []

# Get one loadbalancer by name or id
- opentelekomcloud.cloud.loadbalancer:
    name_or_id: 16dbd25d-c55c-405b-9e56-11b03e7e7dc1
  register: loadbalancer
'''

import time

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VLBLoadbalancerInfoModule(OTCModule):
    argument_spec = dict(
        name_or_id=dict(required=False),
        name=dict(required=False),
        description=dict(required=False),
        provisioning_status=dict(required=False),
        operating_status=dict(required=False),
        vpc_id=dict(required=False),
        vip_port_id=dict(required=False),
        vip_address=dict(required=False),
        vip_subnet_cidr_id=dict(required=False),
        l4_flavor_id=dict(required=False),
        l4_scale_flavor_id=dict(required=False),
        availability_zone_list=dict(required=False, type='list'),
        eips=dict(required=False, type='list'),
        l7_flavor_id=dict(required=False),
        l7_scale_flavor_id=dict(required=False),
        member_device_id=dict(required=False),
        member_address=dict(required=False),
        publicips=dict(required=False, type='list'),
        ip_version=dict(required=False, type='int'),
        elb_virsubnet_type=dict(required=False),
        marker=dict(required=False),
        limit=dict(required=False, type='int'),
        page_reverse=dict(required=False, type='bool')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        data = []

        if self.params['name_or_id']:
            raw = self.conn.vlb.find_load_balancer(
                name_or_id=self.params['name_or_id'])
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)
        else:
            kwargs = dict((k, self.params[k])
                          for k in ['description', 'provisioning_status',
                                    'operating_status', 'vpc_id',
                                    'vip_port_id', 'vip_address',
                                    'vip_subnet_cidr_id', 'l4_flavor_id',
                                    'l4_scale_flavor_id',
                                    'availability_zone_list', 'eips',
                                    'l7_flavor_id', 'l7_scale_flavor_id',
                                    'member_device_id', 'member_address',
                                    'publicips', 'ip_version',
                                    'elb_virsubnet_type', 'marker', 'limit',
                                    'page_reverse']
                          if self.params[k] is not None)
            for raw in self.conn.vlb.load_balancers(**kwargs):
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit_json(
            changed=False,
            loadbalancers=data
        )


def main():
    module = VLBLoadbalancerInfoModule()
    module()


if __name__ == '__main__':
    main()
