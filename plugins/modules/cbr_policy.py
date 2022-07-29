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
module: cbr_policy
short_description: Manage CBR Policy
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.12.4"
author: "Gubina Polina (@Polina-Gubina)"
description: Manage CBR policy resource from the OTC.
options:
  name:
    description: Specifies the policy name or id.
    type: str
    required: true
  enabled:
    description: Whether to enable the policy.
    type: bool
    default: 'yes'
  day_backups:
    description:
        - Specifies the number of retained daily backups.\
        The latest backup of each day is saved in the long term.\
        This parameter can be effective together with the maximum number\
        of retained backups specified by max_backups.
        - If this parameter is configured, timezone is mandatory.
    type: int
  max_backups:
    description:
        - Maximum number of retained backups. 
        - If the value is set to -1, the backups will\
        not be cleared even though the configured retained backup\
        quantity is exceeded. If this parameter and retention_duration_days\
        are both left blank, the backups will be retained permanently.
    type: int
    default: -1
  month_backups:
    description:
     - Specifies the number of retained monthly backups.\
     The latest backup of each month is saved in the long term.\
     This parameter can be effective together with the maximum\
     number of retained backups specified by max_backups.
     - If this parameter is configured, timezone is mandatory.
    type: int
  retention_duration_days:
    description:
        - ID of the target disk to be restored.\
        This parameter is mandatory for disk restoration.
    type: int
    default: -1
  timezone:
    description:
     - Time zone where the user is located.\
     Set this parameter only after you have configured any of the\
     parameters day_backups, week_backups, month_backups, year_backups.
    type: str
  week_backups:
    description:
        - Specifies the number of retained weekly backups.\
        The latest backup of each week is saved in the long term.\
        This parameter can be effective together with the maximum numbe\
        of retained backups specified by max_backups. The value ranges from 0\
        to 100. If this parameter is configured, timezone is mandatory.
    type: int
  year_backups:
    description:
     - Specifies the number of retained yearly backups.\
     The latest backup of each year is saved in the long term.\
     This parameter can be effective together with the maximum\
     number of retained backups specified by max_backups.\
     The value ranges from 0 to 100. If this parameter is configured,\
     timezone is mandatory.
    type: int
  operation_type:
    description: Protection type, which is backup.
    type: str
    default: "backup"
  pattern:
    description: 
      - Scheduling rule. It supports only parameters FREQ,\
      BYDAY, BYHOUR, BYMINUTE, and INTERVAL. FREQ can be set only to\
      WEEKLY or DAILY. BYDAY can be set to MO, TU, WE, TH, FR, SA,\
      and SU (seven days of a week). BYHOUR ranges from 0 to 23 hours.\
      BYMINUTE ranges from 0 minutes to 59 minutes.\
      The scheduling interval must not be less than 1 hour.\
      A maximum of 24 time points are allowed in a day.
    type: list
    required: true
    action: append
  state:
    description:
      - Whether resource should be present or absent.
    choices: [present, absent]
    type: str
    default: present
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
backup:
  description: CBR backups list.
  type: complex
  returned: On Success.
  contains:
    checkpoint_id:
      description: Restore point ID.
      type: str
    created_at:
      description: Creation time.
      type: str
    description:
      description: Backup description.
      type: str
    expired_at:
      description: Expiration time.
      type: str
    extend_info:
      description: Extended information.
      type: complex
      contains:
        allocated:
          description:
            - Allocated capacity, in MB.
          type: int
        charging_mode:
          description:
            - Billing mode.
          type: str
    id:
      description: Backup id.
      type: str
    image_type:
      description: Backup type.
      type: str
    name:
      description: Backup name.
      type: str
    parent_id:
      description: Parent backup ID.
      type: str
    project_id:
      description: Project ID.
      type: str
    protected_at:
      description: Backup time.
      type: str
    resource_az:
      description: Resource availability zone.
      type: str
    resource_id:
      description: Resource ID.
      type: str
    resource_name:
      description: Resource name.
      type: str
    resource_size:
      description: Resource size, in GB.
      type: str
    resource_type:
      description: Resource type.
      type: str
    status:
      description: Backup status.
      type: str
    updated_at:
      description: Update time.
      type: str
    vault_id:
      description: Vault id.
      type: str
    provider_id:
      description: Backup provider ID, which is used to distinguish\
       backup objects. The value can be as follows:.
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


class CBRPolicyModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        enabled=dict(type='bool', default=True, required=False),
        day_backups=dict(type='int', required=False),
        max_backups=dict(type='int', required=False, default=-1),
        month_backups=dict(type='int', required=False),
        retention_duration_days=dict(type='int', required=False, default=-1),
        timezone=dict(type='str', required=False),
        week_backups=dict(type='int', required=False),
        year_backups=dict(type='int', required=False),
        operation_type=dict(type='str', required=False, default="backup"),
        pattern=dict(type='list', required=True, action='append'),
        state=dict(type='str', default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def _require_update(self, policy):
        require_update = False
        if policy:
            if self.params['enabled'] != policy.enabled:
                require_update = True
            if self.params['pattern']:
                require_update = True
            for param_key in ['day_backups', 'max_backups', 'month_backups',
                              'retention_duration_days', 'timezone',
                              'week_backups', 'year_backups']:
                if self.params[param_key] != policy.operation_definition[param_key]:
                    require_update = True
                    break
        return require_update

    def _system_state_change(self, policy):
        state = self.params['state']
        if state == 'present':
            if not policy:
                return True
        elif state == 'absent' and policy:
            return True
        return False

    def run(self):
        query = {}

        state = self.params['state']
        query['operation_type'] = self.params['operation_type']
        query['trigger'] = {}
        query['trigger']['properties'] = {}
        query['trigger']['properties']['pattern'] = []
        query['trigger']['properties']['pattern'] = self.params['pattern']

        if self.params['enabled']:
            query['enabled'] = self.params['enabled']

        query['operation_definition'] = {}
        if self.params['day_backups']:
            query['operation_definition']['day_backups'] = self.params['day_backups']
        if self.params['max_backups']:
            query['operation_definition']['max_backups'] = self.params['max_backups']
        if self.params['month_backups']:
            query['operation_definition']['month_backups'] = self.params['month_backups']
        if self.params['retention_duration_days']:
            query['operation_definition']['retention_duration_days'] = self.params['retention_duration_days']
        if self.params['timezone']:
            query['operation_definition']['timezone'] = self.params['timezone']
        if self.params['week_backups']:
            query['operation_definition']['week_backups'] = self.params['week_backups']
        if self.params['year_backups']:
            query['operation_definition']['year_backups'] = self.params['year_backups']

        policy = self.conn.cbr.find_policy(name_or_id=self.params['name'])

        if self.ansible.check_mode:
            require_update = self._require_update(policy)
            state_change = self._system_state_change(policy)
            if state_change or require_update:
                self.exit_json(changed=True)
            self.exit_json(changed=False)

        if state == 'absent':
            if policy:
                self.conn.cbr.delete_policy(policy=policy.id)
                changed = True
            else:
                changed = False
            self.exit(
                changed=changed
            )

        if policy:
            policy = self.conn.cbr.update_policy(policy=policy.id, **query)
        else:
            query['name'] = self.params['name']
            policy = self.conn.cbr.create_policy(**query)
        self.exit(
            policy=policy,
            changed=True
        )


def main():
    module = CBRPolicyModule()
    module()


if __name__ == '__main__':
    main()
