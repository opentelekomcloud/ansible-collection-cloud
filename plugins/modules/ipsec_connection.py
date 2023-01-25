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
module: ipsec_connection
short_description: Manage VPN IPsec connection
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.12.4"
author: "Gubina Polina (@Polina-Gubina)"
description: Manage VPN ipsec connection from the OTC.
options:
  name:
    description:
     - Specifies the IPsec VPN connection name or id.
    type: str
    required: true
  dpd:
    description: Specifies the DPD protocol control.
    type: dict
  local_id:
    description:
        - Specifies the ID of the external gateway address of a virtual router.
    type: str
  psk:
    description:
     - Specifies the pre-shared key.
    type: str
  initiator:
    description:
        - Specifies whether this VPN can only respond to connections or\
         both respond to and initiate connections.
    type: str
  ipsecpolicy_id:
    description:
     - Specifies the IPsec policy ID.
    type: str
  admin_state_up:
    description:
     - Specifies the administrative status.
    type: bool
  mtu:
    description:
     - Specifies the maximum transmission unit to address fragmentation.
    type: int
  peer_ep_group_id:
    description:
     - Specifies the endpoint group ID (tenant CIDR blocks).
    type: str
  ikepolicy_id:
    description:
     - 	Specifies the IKE policy ID.
    type: str
  vpnservice_id:
    description:
     - Specifies the VPN service ID.
    type: str
  local_ep_group_id:
    description:
     - Specifies the endpoint group ID (VPC subnets).
    type: str
  peer_address:
    description:
     - Specifies the remote gateway address.
    type: str
  peer_id:
    description:
     - Specifies the remote gateway ID.
    type: str
  description:
    description:
     - Provides supplementary information about the IPsec VPN connection.
    type: str
  auth_mode:
    description:
     - Specifies the authentication mode. The default value is psk.
    type: str
  peer_cidrs:
    description:
     - (Deprecated) Specifies the tenant's CIDR blocks.
    type: list
    elements: str
  state:
    description:
      - Whether resource should be present or absent.
    choices: [present, absent]
    type: str
    default: present
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
ipsec_connection:
  description: IPsec connection object.
  type: complex
  returned: On Success.
  contains:
    interval:
      description: Specifies the DPD interval in seconds. The default value is 30.
      type: int
    dpd:
      description: Specifies the DPD protocol control.
      type: dict
    psk:
      description: Specifies the pre-shared key.
      type: str
    initiator:
      description: Specifies whether this VPN can only respond\
       to connections or both respond to and initiate connections.
      type: str
    ipsecpolicy_id:
      description: Specifies the IPsec policy ID.
      type: str
    admin_state_up:
      description: Specifies the administrative status. The value can be true or false.
      type: bool
    mtu:
      description: Specifies the maximum transmission unit to address fragmentation.
      type: int
    peer_ep_group_id:
      description: Specifies the endpoint group ID.
      type: str
    ikepolicy_id:
      description: Specifies the IKE policy ID.
      type: str
    vpnservice_id:
      description: Specifies the VPN service ID.
      type: str
    local_ep_group_id:
      description: Specifies the endpoint group ID (VPC subnets).
      type: str
    peer_address:
      description: Specifies the remote gateway address.
      type: str
    peer_id:
      description: Specifies the remote gateway ID.
      type: str
    name:
      description: Specifies the IPsec VPN connection name.
      type: str
    description:
      description: Provides supplementary information about the IPsec VPN connection.
      type: str
    auth_mode:
      description: Specifies the authentication mode. The default value is psk.
      type: str
    id:
      description: Specifies the IPsec VPN connection ID.
      type: str
    route_mode:
      description: Specifies the route advertising mode. The default value is static.
      type: str
    status:
      description: Specifies the IPsec VPN connection status. The value can be ACTIVE, DOWN, BUILD, ERROR,\
       PENDING_CREATE, PENDING_UPDATE, or PENDING_DELETE..
      type: str
    peer_cidrs:
      description: (Deprecated) Specifies the tenant's CIDR blocks
      type: list
    tenant_id:
      description: Specifies the project ID.
      type: str
    timeout:
      description: Specifies the DPD timeout. The default value is 120 seconds.
      type: int
    action:
      description: Specifies the DPD action. The value can be clear, hold, restart, disabled, or restart-by-peer.\
       The default value is hold.
      type: str
    created_at:
      description: Specifies the time when the IPsec connection was created.
      type: str
'''

EXAMPLES = '''
# Restore backup:
- name:
  opentelekomcloud.cloud.cbr_backup:
    name: "backup-name-or-id"
    volume_id: "volume-id"

# Delete backup:
- name:
  opentelekomcloud.cloud.cbr_backup:
    name: "backup-name-or-id"
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class IPseConnectionModule(OTCModule):
    argument_spec = dict(
        dpd=dict(required=False, type='dict'),
        local_id=dict(type='str', required=False),
        psk=dict(type='str', required=False),
        initiator=dict(type='str', required=False),
        ipsecpolicy_id=dict(type='str', required=False),
        admin_state_up=dict(type='bool', required=False),
        mtu=dict(type='int', required=False),
        peer_ep_group_id=dict(type='str', required=False),
        ikepolicy_id=dict(type='str', required=False),
        vpnservice_id=dict(type='str', required=False),
        local_ep_group_id=dict(type='str', required=False),
        peer_address=dict(type='str', required=False),
        peer_id=dict(type='str', required=False),
        name=dict(type='str', required=False),
        description=dict(type='str', required=False),
        auth_mode=dict(type='str', required=False),
        peer_cidrs=dict(type='list', elements='str', required=False),
        state=dict(type='str',
                   choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['peer_address', 'peer_id'])
        ],
        supports_check_mode=True
    )

    def _system_state_change(self, ipsec_connection):
        state = self.params['state']
        if state == 'present':
            if not ipsec_connection:
                return True
        elif state == 'absent' and ipsec_connection:
            return True
        return False

    def run(self):
        query = {}
        state = self.params['state']
        ipsec_connection = self.conn.vpn.find_vpn_ipsec_site_connection(name_or_id=self.params['name'])
        query['backup'] = ipsec_connection.id

        if self.ansible.check_mode:
            if self._system_state_change(ipsec_connection):
                self.exit_json(changed=True)

        if ipsec_connection:
            if state == 'present':
                if self.params['dpd']:
                    query['dpd'] = self.params['dpd']
                if self.params['psk']:
                    query['psk'] = self.params['psk']
                if self.params['initiator']:
                    query['initiator'] = self.params['initiator']
                if self.params['admin_state_up']:
                    query['admin_state_up'] = self.params['admin_state_up']
                if self.params['mtu']:
                    query['mtu'] = self.params['mtu']
                if self.params['peer_ep_group_id']:
                    query['peer_ep_group_id'] = self.params['peer_ep_group_id']
                if self.params['local_ep_group_id']:
                    query['local_ep_group_id'] = self.params['local_ep_group_id']
                if self.params['peer_address']:
                    query['peer_address'] = self.params['peer_address']
                if self.params['peer_id']:
                    query['peer_id'] = self.params['peer_id']
                if self.params['name']:
                    query['name'] = self.params['name']
                if self.params['description']:
                    query['description'] = self.params['description']
                if self.params['peer_cidrs']:
                    query['peer_cidrs'] = self.params['peer_cidrs']
                require_update = False #self._require_update(ipsec_connection)
                if self.ansible.check_mode:
                    if require_update:
                        self.exit_json(changed=True)
                    self.exit_json(changed=False)
                if not require_update:
                    self.exit_json(changed=False)
                self.conn.vpn.update_vpn_ipsec_site_connection(ipsec_site_connection=ipsec_connection, **query)
                self.exit(changed=True)

            if state == 'absent':
                self.conn.vpn.delete_vpn_ipsec_site_connection(ipsec_site_connection=ipsec_connection)
                self.exit(changed=True)

        if state == 'absent':
            if self.ansible.check_mode:
                self.exit_json(changed=False,
                               msg="ipsec connection {0} not found".format(ipsec_connection.id))

        if state == 'absent':
            if self.ansible.check_mode:
                self.exit_json(changed=False)
            self.fail_json(
                changed=False, msg="ipsec connection {0} not found".format(ipsec_connection.id))

        if self.params['local_id']:
            query['local_id'] = self.params['local_id']
        if self.params['ipsecpolicy_id']:
            query['ipsecpolicy_id'] = self.params['ipsecpolicy_id']
        if self.params['ikepolicy_id']:
            query['ikepolicy_id'] = self.params['ikepolicy_id']
        if self.params['vpnservice_id']:
            query['vpnservice_id'] = self.params['vpnservice_id']
        if self.params['auth_mode']:
            query['auth_mode'] = self.params['auth_mode']
        else:
            query['auth_mode'] = 'psk'
        if self.ansible.check_mode:
            self.exit_json(changed=True)
        created_ipsec_connection = self.conn.vpn.create_vpn_ipsec_site_connection(**query)
        self.exit(changed=True, ipsec_connection=created_ipsec_connection)


def main():
    module = IPseConnectionModule()
    module()


if __name__ == '__main__':
    main()
