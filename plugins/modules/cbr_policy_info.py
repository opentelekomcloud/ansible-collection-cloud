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
module: cbr_policy_info
short_description: Get CBR policy information
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.15.1"
author: "Sidelnikov Anton (@anton-sidelnikov)"
description:
  - Get a CBR policy by name or ID, or list policies matching filters.
options:
  id:
    description:
      - Policy ID.
      - Mutually exclusive with C(name).
    type: str
  name:
    description:
      - Policy name.
      - When specified, a single policy is returned.
      - Mutually exclusive with C(id).
    type: str
  operation_type:
    description:
      - Policy protection type.
    type: str
    choices: [backup, replication]
  vault:
    description:
      - Vault name or ID used to filter policies.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
policy:
  description:
    - CBR policy matching C(name) or C(id).
    - Returned only when C(name) or C(id) is specified.
  type: dict
  returned: success
  contains:
    associated_vaults:
      description: Vaults associated with the policy.
      type: list
      elements: dict
    enabled:
      description: Whether the policy is enabled.
      type: bool
    id:
      description: Policy ID.
      type: str
    name:
      description: Policy name.
      type: str
    operation_definition:
      description: Backup retention settings.
      type: dict
      contains:
        day_backups:
          description: Number of retained daily backups.
          type: int
        max_backups:
          description: Maximum number of retained backups.
          type: int
        month_backups:
          description: Number of retained monthly backups.
          type: int
        retention_duration_days:
          description: Backup retention duration in days.
          type: int
        timezone:
          description: Time zone used by long-term retention rules.
          type: str
        week_backups:
          description: Number of retained weekly backups.
          type: int
        year_backups:
          description: Number of retained yearly backups.
          type: int
    operation_type:
      description: Policy protection type.
      type: str
    trigger:
      description: Policy scheduling configuration.
      type: dict
policies:
  description:
    - CBR policies matching the supplied filters.
    - Returned when C(name) is not specified.
  type: list
  elements: dict
  returned: success
'''

EXAMPLES = '''
- name: Get a policy by name
  opentelekomcloud.cloud.cbr_policy_info:
    name: backup-policy
  register: policy

- name: Get a policy by ID
  opentelekomcloud.cloud.cbr_policy_info:
    id: "4d57a7a8-8ec8-4d17-9233-10f1413062ad"
  register: policy

- name: List backup policies
  opentelekomcloud.cloud.cbr_policy_info:
    operation_type: backup
  register: policies

- name: List policies associated with a vault
  opentelekomcloud.cloud.cbr_policy_info:
    vault: backup-vault
  register: policies
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


def _to_dict(resource):
    if resource is None:
        return None
    data = resource.to_dict()
    data.pop('location', None)
    return data


class CBRPolicyInfoModule(OTCModule):
    otce_min_version = '0.34.2'

    argument_spec = dict(
        id=dict(type='str'),
        name=dict(type='str'),
        operation_type=dict(type='str', choices=['backup', 'replication']),
        vault=dict(type='str'),
    )
    module_kwargs = dict(
        supports_check_mode=True,
        mutually_exclusive=[
            ('id', 'name'),
        ],
    )

    def run(self):
        name_or_id = self.params['id'] or self.params['name']
        if name_or_id:
            policy = self.conn.cbr.find_policy(name_or_id=name_or_id)
            self.exit(
                changed=False,
                policy=_to_dict(policy)
            )

        query = {}
        if self.params['operation_type']:
            query['operation_type'] = self.params['operation_type']
        if self.params['vault']:
            vault = self.conn.cbr.find_vault(self.params['vault'])
            if not vault:
                self.fail_json(msg='Vault %s not found' % self.params['vault'])
            query['vault_id'] = vault.id

        policies = [_to_dict(policy) for policy in self.conn.cbr.policies(**query)]
        self.exit(
            changed=False,
            policies=policies
        )


def main():
    module = CBRPolicyInfoModule()
    module()


if __name__ == '__main__':
    main()
