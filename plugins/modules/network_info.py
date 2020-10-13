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
module: network_info
short_description: Get information about networks
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.4"
author: "Polina Gubina (@polina-gubina)"
description:
  - Get networks info from the OTC.
options:
  description:
    description:
      - The network description.
    type: str
  ipv4_address_scope_id:
    description:
      - The ID of the IPv4 address scope for the network
    type: str
  ipv6_address_scope_id:
    description:
      - The ID of the IPv6 address scope for the network.
    type: str
  is_admin_state_up:
    description:
      -  Network administrative state.
    type: str
  is_port_security_enabled:
    description:
      - The port security status.
    type: bool
  is_router_external:
    description:
      - Network is external or not.
    type: bool
  is_shared:
    description:
      - Whether the network is shared across projects.
    type: bool
  name:
    description:
      - The name of the network.
    type: str
  status:
    description:
      - Network status
    type: str
  project_id:
    description:
      - Owner tenant ID.
    type: str
  provider_network_type:
    description:
      - Network physical mechanism.
    type: str
  provider_physical_network:
    description:
      - Physical network.
    type: str
  provider_segmentation_id:
    description:
      - VLAN ID for VLAN networks or Tunnel ID for GENEVE/GRE/VXLAN networks.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
networks:
  description: The networks object list.
  type: complex
  returned: On Success.
  contains:
    availability_zone_hints:
      description: Specifies the availability zones available to this network.
      type: list
      sample: ""
    availability_zones:
      description: Specifies the availability zone of this network.
      type: list
      sample: ""
    created_at:
      description: Specifies the time (UTC) when the network is created.
      type: str
      sample: "2020-09-13T20:37:01"
    description:
      description: Description of network.
      type: str
      sample: ""
    dns_domain:
      description: Specifies the default private network DNS domain address.
      type: str
      sample: "eu-de.compute.internal."
    id:
      description: Specifies the network ID.
      type: str
      sample: "45007a7e-ee4f-7u53-8283-b4da2e037c69"
    ipv4_address_scope_id:
      description: The ID of the IPv4 address scope for the network.
      type: str
      sample: ""
    ipv6_address_scope_id:
      description: The ID of the IPv6 address scope for the network.
      type: str
      sample: ""
    is_admin_state_up:
      description:  The administrative status.
      type: bool
      sample: "true"
    is_default:
      description:
      type: str
      sample: "null"
    is_port_security_enabled:
      description: Specifies whether the security option is enabled for the port.
      type: bool
      sample: "true"
    is_router_external:
      description: Specifies whether the network is an external network.
      type: bool
      sample: "true"
    is_shared:
      description: Specifies whether the firewall rule can be shared by different tenants.
      type: bool
      sample: "true"
    is_vlan_transparent:
      description: 
      type: str
      sample: "null"
    mtu:
      description: 
      type: str
      sample: "null"
    name:
      description: Network name.
      type: str
      sample: "network_1"
    project_id:
      description: Project ID.
      type: str
      sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
    provider_network_type:
      description: Network physical mechanism.
      type: str
      sample: "vxlan"
    provider_physical_network:
      description: Physical network.
      type: str
      sample: "vxlan"
    provider_segmentation_id:
      description:
      type: str
      sample: "null"
    qos_policy_id:
      description:
      type: str
      sample: "null"
    revision_number:
      description: Network status.
      type: str
      sample: "null"
    segments:
      description:
      type: str
      sample: "null"
    status:
      description: Network status.
      type: str
      sample: "null"
    subnet_ids:
      description: IDs of the subnets aasociated with this network.
      type: list
      sample: "["20447648-718a-4ec1-8476-9db0f49828ee"]"
    tags:
      description:
      type: list
      sample:""
    updated_at:
      description: Specifies the time (UTC) when the network is updated.
      type: str
      sample: "2020-09-13T20:37:01"
'''

EXAMPLES = '''
# Get configs versions.
- network_info:
    name: my_network
  register: networks
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VPCNetworkInfoModule(OTCModule):
    argument_spec = dict(
        description=dict(required=False),
        ipv4_address_scope_id=dict(required=False),
        ipv6_address_scope_id=dict(required=False),
        is_admin_state_up=dict(required=False),
        is_port_security_enabled=dict(required=False),
        is_router_external=dict(required=False),
        is_shared=dict(required=False),
        name=dict(required=False),
        status=dict(required=False),
        project_id=dict(required=False),
        provider_network_type=dict(required=False),
        provider_physical_network=dict(required=False),
        provider_segmentation_id=dict(required=False),
    )

    def run(self):

        description_filter = self.params['description']
        ipv4_address_scope_id_filter = self.params['ipv4_address_scope_id']
        ipv6_address_scope_id_filter = self.params['ipv6_address_scope_id']
        is_admin_state_up_filter = self.params['is_admin_state_up']
        is_port_security_enabled_filter = self.params['is_port_security_enabled']
        is_router_external_filter = self.params['is_router_external']
        is_shared_filter = self.params['is_shared']
        name_filter = self.params['name']
        status_filter = self.params['status']
        project_id_filter= self.params['project_id']
        provider_network_type_filter = self.params['provider_network_type']
        provider_physical_network_filter = self.params['provider_physical_network']
        provider_segmentation_id_filter = self.params['provider_segmentation_id']


        data = []
        query = {}
        if description_filter:
            query['description'] = description_filter
        if ipv4_address_scope_id_filter:
            query['ipv4_address_scope_id'] = ipv4_address_scope_id_filter
        if ipv6_address_scope_id_filter:
            query['ipv6_address_scope_id'] = ipv6_address_scope_id_filter
        if is_admin_state_up_filter:
            query['is_admin_state_up'] = is_admin_state_up_filter
        if is_port_security_enabled_filter:
            query['is_port_security_enabled'] = is_port_security_enabled_filter
        if is_router_external_filter:
            query['is_router_external'] = is_router_external_filter
        if is_shared_filter:
            query['is_shared'] = is_shared_filter
        if name_filter:
            query['name'] = name_filter
        if status_filter:
            query['status'] = status_filter
        if project_id_filter:
            query['project_id'] = project_id_filter
        if provider_network_type_filter:
            query['provider_network_type'] = provider_network_type_filter
        if provider_physical_network_filter:
            query['provider_physical_network'] = provider_physical_network_filter
        if provider_segmentation_id_filter:
            query['provider_segmentation_id'] = provider_segmentation_id_filter

        for raw in self.conn.network.networks(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit_json(
            changed=False,
            networks=data
        )


def main():
    module = VPCNetworkInfoModule()
    module()


if __name__ == '__main__':
    main()
