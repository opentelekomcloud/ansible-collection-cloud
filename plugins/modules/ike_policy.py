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
module: ike_policy
short_description: Manage VPN IKE policy
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.12.4"
author: "Gubina Polina (@Polina-Gubina)"
description:
    - Manage cbr IKE policy from the OTC.
options:
  name:
    description:
      - Specifies the IKE policy name or id.
    type: str
  auth_algorithm:
    description:
        - Specifies the authentication hash algorithm.
    type: str
    choices: ['md5', 'sha1', 'sha2-256', 'sha2-384', 'sha2-512']
  description:
    description:
      - Provides supplementary information about the IKE policy.
    type: str
  encryption_algorithm:
    description:
      - Specifies the encryption algorithm.
      - The default value is aes-128.
    type: str
    choices: ['3des', 'aes-128', 'aes-192', 'aes-256']
  ike_version:
    description:
      - Specifies the IKE version.
    choices: ['v1', 'v2']
    type: str
  pfs:
    description:
      - Specifies the PFS. The value disable indicates that the PFS function is disabled.
      - The default value is group5.
    type: str
    choices: ['group1', 'group2', 'group5', 'group14', 'group15', 'group16', 'group19', 'group20', 'group21', 'disable']
  phase1_negotiation_mode:
    description:
      - Specifies the IKE mode The default value is main.
    type: str
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
  state:
    description:
      - Whether resource should be present or absent.
    choices: ['present', 'absent']
    type: str
    default: 'present'
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
ike_policy:
    description: IKE policy object.
    type: complex
    returned: On Success.
    contains:
      auth_algorithm:
        description: Specifies the authentication hash algorithm.
        type: str
      description:
        description: Provides supplementary information about the IKE policy.
        type: str
      encryption_algorithm:
        description: Specifies the encryption algorithm.
        type: str
      id:
        description: Specifies the IKE policy ID.
        type: str
      ike_version:
        description: Specifies the IKE version. The value can be v1 or v2.
        type: str
      lifetime:
        description: Specifies the lifetime object of SA.
        type: dict
      name:
        description: Specifies the IKE policy name.
        type: str
      phase1_negotiation_mode:
        description: Specifies the IKE mode The default value is main.
        type: dict
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


class IkePolicyModule(OTCModule):
    argument_spec = dict(
        name=dict(type='str'),
        auth_algorithm=dict(type='str', choices=['md5', 'sha1', 'sha2-256', 'sha2-384', 'sha2-512']),
        description=dict(required=False, type='str'),
        encryption_algorithm=dict(type='str', choices=['3des', 'aes-128', 'aes-192', 'aes-256']),
        ike_version=dict(type='str', choices=['v1', 'v2']),
        pfs=dict(type='str',
                 choices=['group1', 'group2', 'group5', 'group14', 'group15', 'group16', 'group19', 'group20',
                          'group21', 'disable']),
        phase1_negotiation_mode=dict(type='str'),
        value=dict(required=False, type='int'),
        units=dict(required=False, type='str'),
        project_id=dict(type='str', required=False),
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

    def _require_update(self, ike_policy):
        require_update = False
        if ike_policy:
            if self.params['name']:
                if self.params['name'] != ike_policy['name']:
                    require_update = True
            if self.params['description']:
                if self.params['description'] != ike_policy['description']:
                    require_update = True
            if self.params['auth_algorithm']:
                if self.params['auth_algorithm'] != ike_policy['auth_algorithm']:
                    require_update = True
            if self.params['encryption_algorithm']:
                if self.params['encryption_algorithm'] != ike_policy['encryption_algorithm']:
                    require_update = True
            if self.params['pfs']:
                if self.params['pfs'] != ike_policy['pfs']:
                    require_update = True
            if self.params['units']:
                if self.params['units'] != ike_policy['lifetime']['units']:
                    require_update = True
            if self.params['value']:
                if self.params['value'] != ike_policy['lifetime']['value']:
                    require_update = True
        return require_update

    def run(self):
        attrs = {}
        state = self.params['state']
        if self.params['name']:
            attrs['name'] = self.params['name']
        if self.params['auth_algorithm']:
            attrs['auth_algorithm'] = self.params['auth_algorithm']
        if self.params['description']:
            attrs['description'] = self.params['description']
        if self.params['encryption_algorithm']:
            attrs['encryption_algorithm'] = self.params['encryption_algorithm']
        if self.params['ike_version']:
            attrs['ike_version'] = self.params['ike_version']
        if self.params['pfs']:
            attrs['pfs'] = self.params['pfs']
        if self.params['phase1_negotiation_mode']:
            attrs['phase1_negotiation_mode'] = self.params['phase1_negotiation_mode']
        attrs['lifetime'] = {}
        if self.params['units'] or self.params['value']:
            if self.params['units']:
                attrs['lifetime']['units'] = self.params['units']
            if self.params['value']:
                attrs['lifetime']['value'] = self.params['value']
        if self.params['project_id']:
            attrs['project_id'] = self.params['project_id']

        ike_policy = self.conn.network.find_vpn_ike_policy(name_or_id=self.params['name'], ignore_missing=True)

        if self.ansible.check_mode:
            if self._system_state_change(ike_policy):
                self.exit_json(changed=True)
        if ike_policy:
            if state == 'present':
                require_update = self._require_update(ike_policy)
                if self.ansible.check_mode:
                    if require_update:
                        self.exit_json(changed=True)
                    self.exit_json(changed=False)
                if not require_update:
                    self.exit_json(changed=False)
                updated_ikepolicy = self.conn.network.update_vpn_ike_policy(ike_policy=ike_policy, **attrs)
                self.exit(changed=True, ike_policy=updated_ikepolicy)

            if state == 'absent':
                self.conn.network.delete_vpn_ike_policy(ike_policy=ike_policy)
                self.exit(changed=True)

        if state == 'absent':
            self.exit_json(changed=False,
                           msg="ike policy {0} not found".format(self.params['name']))
        if not self.params['encryption_algorithm']:
            attrs['encryption_algorithm'] = 'aes-128'
        if not self.params['ike_version']:
            attrs['ike_version'] = 'v1'
        if not self.params['pfs']:
            attrs['pfs'] = 'group5'
        if not self.params['phase1_negotiation_mode']:
            attrs['phase1_negotiation_mode'] = 'main'
        if not self.params['units']:
            attrs['lifetime']['units'] = 'seconds'
        if not self.params['value']:
            attrs['lifetime']['value'] = 3600
        if self.ansible.check_mode:
            self.exit_json(changed=True)
        created_ikepolicy = self.conn.network.create_vpn_ike_policy(**attrs)
        self.exit(changed=True, ike_policy=created_ikepolicy)


def main():
    module = IkePolicyModule()
    module()


if __name__ == '__main__':
    main()
