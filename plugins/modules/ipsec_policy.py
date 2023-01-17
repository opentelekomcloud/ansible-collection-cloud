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
module: ipsec_policy
short_description: Manage VPN IPsec policy
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.12.4"
author: "Gubina Polina (@Polina-Gubina)"
description:
    - Manage cbr ipsec policy from the OTC.
options:
  name:
    description:
      - Specifies the IPsec policy name or id.
    type: str
  pfs:
    description:
      - Specifies the PFS. The value disable indicates that the PFS function is disabled.
      - The default value is group5.
    type: str
    choices: ['group1', 'group2', 'group5', 'group14', 'group15', 'group16', 'group19', 'group20', 'group21', 'disable']
  auth_algorithm:
    description:
        - Specifies the authentication hash algorithm.
    type: str
    choices: ['md5', 'sha1', 'sha2-256', 'sha2-384', 'sha2-512']
  description:
    description:
      - Provides supplementary information about the IPsec policy.
    type: str
  encapsulation_mode:
    description:
      - Specifies the encapsulation mode.
      - The default value is tunnel.
    type: str
  encryption_algorithm:
    description:
      - Specifies the encryption algorithm.
      - The default value is aes-128.
    type: str
    choices: ['3des', 'aes-128', 'aes-192', 'aes-256']
  value:
    description:
      - Specifies the lifetime value of the SA.
      - The default unit is seconds.
    type: int
  units:
    description:
      - Specifies the lifecycle unit.
      - The default value is seconds.
    type: str
  project_id:
    description:
      - Specifies the project ID.
    type: str
  transform_protocol:
    description:
      - Specifies the transform protocol used.
      - The default value is esp.
    type: str
    choices: ['esp', 'ah', 'ah-esp']
  state:
    description:
      - Whether resource should be present or absent.
    choices: ['present', 'absent']
    type: str
    default: 'present'
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
ipsec_policy:
    description: IPsec policy object.
    type: complex
    returned: On Success.
    contains:
      auth_algorithm:
        description: Specifies the authentication hash algorithm.
        type: str
      description:
        description: Provides supplementary information about the IPsec policy.
        type: str
      encryption_algorithm:
        description: Specifies the encryption algorithm.
        type: str
      id:
        description: Specifies the IPsec policy ID.
        type: str
      lifetime:
        description: Specifies the lifetime object of SA.
        type: dict
      name:
        description: Specifies the IPsec policy name.
        type: str
      pfs:
        description: Specifies the PFS.
        type: str
      project_id:
        description: Vault tags.
        type: str
'''

EXAMPLES = '''
- name: Create ipsec policy
  opentelekomcloud.cloud.ipsec_policy:
    name: "ipsecpolicy1"
    auth_algorithm: "md5"
    pfs: "group2"
    value: 7200
  register: ipsecpolicy

- name: Update ipsec policy
  opentelekomcloud.cloud.ipsec_policy:
    name: "ipsecpolicy1"
    auth_algorithm: "md5"
    transform_protocol: "ah"
    encryption_algorithm: "aes-192"
    pfs: "group5"
    value: 7200
  register: ipsecpolicy

- name: Delete CBR vault
  opentelekomcloud.cloud.ipsec_policy:
    name: "ipsecpolicy1"
    state: absent
  register: ipsecpolicy
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class IpsecPolicyModule(OTCModule):
    argument_spec = dict(
        name=dict(type='str'),
        pfs=dict(type='str', choices=['group1', 'group2', 'group5', 'group14', 'group15', 'group16', 'group19', 'group20', 'group21', 'disable']),
        auth_algorithm=dict(type='str', choices=['md5', 'sha1', 'sha2-256', 'sha2-384', 'sha2-512']),
        description=dict(required=False, type='str'),
        encapsulation_mode=dict(type='str'),
        encryption_algorithm=dict(type='str', choices=['3des', 'aes-128', 'aes-192', 'aes-256']),
        value=dict(required=False, type='int'),
        units=dict(required=False, type='str'),
        project_id=dict(type='str', required=False),
        transform_protocol=dict(required=False, type='str', choices=['esp', 'ah', 'ah-esp']),
        state=dict(type='str', required=False, choices=['present', 'absent'],
                   default='present')
    )

    def _system_state_change(self, vault):
        state = self.params['state']
        if state == 'present' and not vault:
            return True
        if state == 'absent' and vault:
            return True
        return False

    def _require_update(self, ipsec_policy):
        require_update = False
        if ipsec_policy:
            if self.params['name']:
                if self.params['name'] != ipsec_policy['name']:
                    require_update = True
            if self.params['description']:
                if self.params['description'] != ipsec_policy['description']:
                    require_update = True
            if self.params['auth_algorithm']:
                if self.params['auth_algorithm'] != ipsec_policy['auth_algorithm']:
                    require_update = True
            if self.params['encryption_algorithm']:
                if self.params['encryption_algorithm'] != ipsec_policy['encryption_algorithm']:
                    require_update = True
            if self.params['pfs']:
                if self.params['pfs'] != ipsec_policy['pfs']:
                    require_update = True
            if self.params['units']:
                if self.params['units'] != ipsec_policy['lifetime']['units']:
                    require_update = True
            if self.params['value']:
                if self.params['value'] != ipsec_policy['lifetime']['value']:
                    require_update = True
        return require_update

    def run(self):
        attrs = {}
        state = self.params['state']
        if self.params['name']:
            attrs['name'] = self.params['name']
        if self.params['pfs']:
            attrs['pfs'] = self.params['pfs']
        if self.params['auth_algorithm']:
            attrs['auth_algorithm'] = self.params['auth_algorithm']
        if self.params['description']:
            attrs['description'] = self.params['description']
        if self.params['encapsulation_mode']:
            attrs['encapsulation_mode'] = self.params['encapsulation_mode']
        if self.params['encryption_algorithm']:
            attrs['encryption_algorithm'] = self.params['encryption_algorithm']
        if self.params['units'] or self.params['value']:
            attrs['lifetime'] = {}
            if self.params['units']:
                attrs['lifetime']['units'] = self.params['units']
            if self.params['value']:
                attrs['lifetime']['value'] = self.params['value']
        if self.params['project_id']:
            attrs['project_id'] = self.params['project_id']
        if self.params['transform_protocol']:
            attrs['transform_protocol'] = self.params['transform_protocol']

        ipsec_policy = self.conn.network.find_vpn_ipsec_policy(name_or_id=self.params['name'], ignore_missing=True)

        if self.ansible.check_mode:
            if self._system_state_change(ipsec_policy):
                self.exit_json(changed=True)
        if ipsec_policy:
            if state == 'present':
                require_update = self._require_update(ipsec_policy)
                if self.ansible.check_mode:
                    if require_update:
                        self.exit_json(changed=True)
                    self.exit_json(changed=False)
                if not require_update:
                    self.exit_json(changed=False)
                updated_ipsecpolicy = self.conn.network.update_vpn_ipsec_policy(ipsec_policy=ipsec_policy, **attrs)
                self.exit(changed=True, ipsec_policy=updated_ipsecpolicy)

            if state == 'absent':
                self.conn.network.delete_vpn_ipsec_policy(ipsec_policy=ipsec_policy)
                self.exit(changed=True)

        if state == 'absent':
            self.exit_json(changed=False,
                           msg="ipsec policy {0} not found".format(self.params['name']))
        if not self.params['pfs']:
            attrs['pfs'] = 'group5'
        if not self.params['encapsulation_mode']:
            attrs['encapsulation_mode'] = 'tunnel'
        if not self.params['encryption_algorithm']:
            attrs['encryption_algorithm'] = 'aes-128'
        if not self.params['transform_protocol']:
            attrs['transform_protocol'] = 'esp'
        if attrs['lifetime']:
            if not self.params['units']:
                attrs['lifetime']['units'] = 'seconds'
            if not self.params['value']:
                attrs['lifetime']['value'] = 3600
        if self.ansible.check_mode:
            self.exit_json(changed=True)
        created_ipsecpolicy = self.conn.network.create_vpn_ipsec_policy(**attrs)
        self.exit(changed=True, ipsec_policy=created_ipsecpolicy)


def main():
    module = IpsecPolicyModule()
    module()


if __name__ == '__main__':
    main()
