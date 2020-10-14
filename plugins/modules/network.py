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
module: network
short_description: Create/Remove network from the OTC.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.4"
author: "Polina Gubina (@polina-gubina)"
description:
  - Create/Remove network from the OTC.
options:
  description:
    description:
      - The network description.
    type: str
  ipv4_address_scope_id:
    description:
      - The ID of the IPv4 address scope for the network.
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
  provider_network_type:
    description:
      - The type of physical network that maps to this network resource.
    type: str
  provider_physical_network:
    description:
      - The physical network where this network object must be implemented.
    type: str
  provider_segmentation_id:
    description:
      - VLAN ID for VLAN networks or Tunnel ID for GENEVE/GRE/VXLAN networks.
    type: str
  state:
    description:
      - Specifies whether the network must be created or removed.
    choices: [present, absent]
    default: present
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
      sample: ""
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
      description: Whether or not this is the default external network.
      type: str
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
      description: Indicates the VLAN transparency mode of the network.
      type: bool
    mtu:
      description: The maximum transmission unit (MTU) of the network resource.
      type: int
    name:
      description: Network name.
      type: str
      sample: "network_1"
    project_id:
      description: Project ID.
      type: str
      sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
    provider_network_type:
      description: The type of physical network that maps to this network resource.
      type: str
      sample: "vxlan"
    provider_physical_network:
      description: The physical network where this network object is implemented.
      type: str
      sample: "vxlan"
    provider_segmentation_id:
      description: An isolated segment ID on the physical network. The provider network type defines the segmentation model.
      type: str
    qos_policy_id:
      description: The ID of the QoS policy attached to the port.
      type: str
    segments:
      description: A list of provider segment objects.
      type: str
    status:
      description: Network status.
      type: str
    subnet_ids:
      description: IDs of the subnets aasociated with this network.
      type: list
      sample: "[20447648-718a-4ec1-8476-9db0f49828ee]"
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


class VPCNetworkModule(OTCModule):
    argument_spec = dict(
        description=dict(required=False),
        ipv4_address_scope_id=dict(required=False),
        ipv6_address_scope_id=dict(required=False),
        is_admin_state_up=dict(required=False),
        is_port_security_enabled=dict(required=False, type='bool'),
        is_router_external=dict(required=False, type='bool'),
        is_shared=dict(required=False, type='bool'),
        name=dict(required=False),
        provider_network_type=dict(required=False),
        provider_physical_network=dict(required=False),
        provider_segmentation_id=dict(required=False),
        state=dict(required=False, default='present', choices=['present', 'absent'])
    )

    def run(self):

        description = self.params['description']
        ipv4_address_scope_id = self.params['ipv4_address_scope_id']
        ipv6_address_scope_id = self.params['ipv6_address_scope_id']
        is_admin_state_up = self.params['is_admin_state_up']
        is_port_security_enabled = self.params['is_port_security_enabled']
        is_router_external = self.params['is_router_external']
        is_shared = self.params['is_shared']
        name = self.params['name']
        provider_network_type = self.params['provider_network_type']
        provider_physical_network = self.params['provider_physical_network']
        provider_segmentation_id = self.params['provider_segmentation_id']

        changed = False

        network = self.conn.network.find_network(name, ignore_missing=True)

        if self.params['state'] == 'present':

            if not network:

                attrs = {}

                if name:
                    attrs['name'] = self.params['name']
                if description:
                    attrs['description'] = self.params['description']
                if ipv4_address_scope_id:
                    attrs['ipv4_address_scope_id'] = self.params['ipv4_address_scope_id']
                if ipv6_address_scope_id:
                    attrs['ipv6_address_scope_id'] = self.params['ipv6_address_scope_id']
                if is_admin_state_up:
                    attrs['is_admin_state_up'] = self.params['is_admin_state_up']
                if is_port_security_enabled:
                    attrs['is_port_security_enabled'] = self.params['is_port_security_enabled']
                if is_router_external:
                    attrs['is_router_external'] = self.params['is_router_external']
                if is_shared:
                    attrs['is_shared'] = self.params['is_shared']
                if project_id:
                    attrs['project_id'] = self.params['project_id']
                if provider_network_type:
                    attrs['provider_network_type'] = self.params['provider_network_type']
                if provider_physical_network:
                    attrs['provider_physical_network'] = self.params['provider_physical_network']
                if provider_segmentation_id:
                    attrs['provider_segmentation_id'] = self.params['provider_segmentation_id']

                network = self.conn.network.create_network(**attrs)
                changed = True

                self.exit_json(
                    changed=changed,
                    network=network
                )

            else:
                self.fail_json(
                    msg="Network already exists"
                )

        elif self.params['state'] == 'absent':
            if network:
                self.conn.network.delete_network(network)
                changed = True
                self.exit_json(
                    changed=changed,
                    result="Resource was deleted"
                )

            else:
                self.fail_json(
                    msg="Resource with this name doesn't exist"
                )


def main():
    module = VPCNetworkModule()
    module()


if __name__ == '__main__':
    main()
