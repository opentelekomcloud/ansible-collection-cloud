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
  is_enabled:
    description: Whether to enable the policy. By default 'true'.
    type: bool
  count_day_backups:
    description:
      - Specifies the number of retained daily backups. This parameter can be
        effective together with the maximum number of retained backups
        specified by max_backups.
      - If this parameter is configured, timezone is mandatory.
    type: int
  count_max_backups:
    description:
      - Maximum number of retained backups.
      - If the value is set to -1, the backups will not be cleared even though
        the configured retained backup quantity is exceeded. If this parameter
        and retention_duration_days are both left blank, the backups will be
        retained permanently.  By default -1.
    type: int
  count_month_backups:
    description:
      - Specifies the number of retained monthly backups. The latest backup of
        each month is saved in the long term. This parameter can be effective
        together with the maximum number of retained backups specified by
        max_backups.
      - If this parameter is configured, timezone is mandatory.
    type: int
  retention_duration_days:
    description:
      - ID of the target disk to be restored. This parameter is mandatory for
        disk restoration. By default -1.
    type: int
  timezone:
    description:
      - Time zone where the user is located, for example, UTC+08:00. Set this
        parameter only after you have configured any of the parameters
        day_backups, week_backups, month_backups, year_backups.
    type: str
  count_week_backups:
    description:
      - Specifies the number of retained weekly backups.  The latest backup of
        each week is saved in the long term.  This parameter can be effective
        together with the maximum number of retained backups specified by
        max_backups. The value ranges from 0 to 100. If this parameter is
        configured, timezone is mandatory.
    type: int
  count_year_backups:
    description:
      - Specifies the number of retained yearly backups.  The latest backup of
        each year is saved in the long term.  This parameter can be effective
        together with the maximum number of retained backups specified by
        max_backups.  The value ranges from 0 to 100. If this parameter is
        configured, timezone is mandatory.
    type: int
  operation_type:
    description:
      - Protection type of the policy, 'backup' by default.
      - For now, value 'backup' is only possible.
    type: str
  pattern:
    description:
      - Scheduling rule. A maximum of 24 rules can be configured. The
        scheduling rule complies with iCalendar RFC 2445, but it supports only
        parameters FREQ, BYDAY, BYHOUR, BYMINUTE, and INTERVAL. FREQ can be set
        only to WEEKLY or DAILY. BYDAY can be set to MO, TU, WE, TH, FR, SA,
        and SU (seven days of a week). BYHOUR ranges from 0 to 23 hours.
        BYMINUTE ranges from 0 minutes to 59 minutes. The scheduling interval
        must not be less than 1 hour.  A maximum of 24 time points are allowed
        in a day. For example
        - if the scheduling time is 14:00 from Monday to Sunday, set the
          scheduling rule to
          'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU;BYHOUR=14;BYMINUTE=00'
        - If the scheduling time is 14:00 every day, set the scheduling rule to
          'FREQ=DAILY;INTERVAL=1;BYHOUR=14;BYMINUTE=00'
        - If the scheduling time is 14:00 every day, set the scheduling rule to
          'FREQ=DAILY;INTERVAL=1;BYHOUR=14;BYMINUTE=00'
      - For update pattern all rules must be in the same order as existing policy has.
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
policy:
  description: CBR policy object.
  type: complex
  returned: On Success.
  contains:
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
      description: Policy attributes.
      type: complex
      contains:
        day_backups:
          description:
            - Specifies the number of retained daily backups.
          type: int
        max_backups:
          description:
            - Maximum number of retained backups.
          type: int
        month_backups:
          description:
            - Specifies the number of retained monthly backups.
          type: int
        retention_duration_days:
          description:
            - Duration of retaining a backup, in days.
          type: int
        timezone:
          description:
            - Time zone where the user is located.
          type: str
        week_backups:
          description:
            - Specifies the number of retained weekly backups.
          type: int
        year_backups:
          description:
            - Specifies the number of retained yearly backups.
          type: str
    operation_type:
      description: Backup id.
      type: str
    trigger:
      description: Time scheduling rule for the policy.
      type: complex
      contains:
        id:
          description: Scheduler ID.
          type: str
        name:
          description: Scheduler name.
          type: str
        properties:
          description: Scheduler attributes.
          type: complex
          contains:
            pattern:
              description: Scheduling policy of the scheduler.
              type: list
            start_time:
              description: Start time of the scheduler.
              type: str
        type:
          description:
            - Scheduler type. Currently, only time (periodic scheduling) is supported.
          type: str
    associated_vaults:
      description: Associated vault.
      type: list
      contains:
        destination_vault_id:
          description:
            - ID of the associated remote vault.
          type: str
        vault_id:
          description:
            - Vault ID.
          type: str
'''

EXAMPLES = '''
# Create policy:
opentelekomcloud.cloud.cbr_policy:
  name: "newpolicy"
  count_day_backups: 0
  count_month_backups: 0
  retention_duration_days: 5
  count_year_backups: 0
  pattern:
    - "FREQ=WEEKLY;BYHOUR=14;BYDAY=MO,TU,WE,TH,FR,SA,SU;BYMINUTE=00"

# Update policy:
opentelekomcloud.cloud.cbr_policy:
  name: "newpolicy"
  count_day_backups: 5
  is_enabled: False

# Delete policy:
opentelekomcloud.cloud.cbr_policy:
  name: "newpolicy"
  state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CBRPolicyModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        is_enabled=dict(type='bool', required=False),
        count_day_backups=dict(type='int', required=False),
        count_max_backups=dict(type='int', required=False),
        count_month_backups=dict(type='int', required=False),
        retention_duration_days=dict(type='int', required=False),
        timezone=dict(type='str', required=False),
        count_week_backups=dict(type='int', required=False),
        count_year_backups=dict(type='int', required=False),
        operation_type=dict(type='str', required=False),
        pattern=dict(type='list', required=False, elements='str'),
        state=dict(type='str', default='present', choices=['present', 'absent'])
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['pattern'])
        ],
        supports_check_mode=True
    )

    def _require_update(self, policy):
        require_update = False
        if policy:
            if self.params['is_enabled'] is not None:
                if self.params['is_enabled'] != policy.enabled:
                    require_update = True
            if self.params['pattern']:
                if set(self.params['pattern']) != set(
                        policy['trigger']['properties']['pattern']):
                    require_update = True
            if self.params['count_day_backups'] is not None:
                if self.params['count_day_backups'] != policy.operation_definition['day_backups']:
                    require_update = True
            if self.params['count_max_backups'] is not None:
                if self.params['count_max_backups'] != policy.operation_definition['max_backups']:
                    require_update = True
            if self.params['count_month_backups'] is not None:
                if self.params['count_month_backups'] != policy.operation_definition['month_backups']:
                    require_update = True
            if self.params['count_week_backups'] is not None:
                if self.params['count_week_backups'] != policy.operation_definition['week_backups']:
                    require_update = True
            if self.params['count_year_backups'] is not None:
                if self.params['count_year_backups'] != policy.operation_definition['year_backups']:
                    require_update = True
            if self.params['retention_duration_days'] is not None:
                if self.params['retention_duration_days'] != policy.operation_definition['retention_duration_days']:
                    require_update = True
            if self.params['timezone'] is not None:
                if self.params['timezone'] != policy.operation_definition['timezone']:
                    require_update = True
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
        policy = self.conn.cbr.find_policy(name_or_id=self.params['name'])
        changed = False

        if self.ansible.check_mode:
            require_update = self._require_update(policy)
            state_change = self._system_state_change(policy)
            if state_change or require_update:
                changed = True
            else:
                changed = False
            if policy:
                self.exit_json(changed=changed, policy=policy)
            self.exit_json(changed=changed)

        if state == 'absent':
            if policy:
                self.conn.cbr.delete_policy(policy=policy.id)
                changed = True
            else:
                changed = False
            self.exit(
                changed=changed
            )

        query['trigger'] = {'properties': {}}
        query['trigger']['properties']['pattern'] = self.params['pattern']
        if self.params['is_enabled'] is not None:
            query['enabled'] = self.params['is_enabled']

        query['operation_definition'] = {}
        if self.params['count_day_backups'] is not None:
            query['operation_definition']['day_backups'] = self.params['count_day_backups']
        if self.params['count_day_backups']:
            query['operation_definition']['max_backups'] = self.params['count_day_backups']
        if self.params['count_month_backups'] is not None:
            query['operation_definition']['month_backups'] = self.params['count_month_backups']
        if self.params['retention_duration_days'] is not None:
            query['operation_definition']['retention_duration_days'] = self.params['retention_duration_days']
        if self.params['timezone']:
            query['operation_definition']['timezone'] = self.params['timezone']
        if self.params['count_week_backups'] is not None:
            query['operation_definition']['week_backups'] = self.params['count_week_backups']
        if self.params['count_year_backups'] is not None:
            query['operation_definition']['year_backups'] = self.params['count_year_backups']

        if not policy:
            if self.params['operation_type']:
                query['operation_type'] = self.params['operation_type']
            else:
                query['operation_type'] = 'backup'
            if self.params['is_enabled'] is None:
                query['enabled'] = True
            if not self.params['count_day_backups']:
                query['operation_definition']['max_backups'] = -1
            if not self.params['retention_duration_days']:
                query['operation_definition']['retention_duration_days'] = -1
            query['name'] = self.params['name']
            policy = self.conn.cbr.create_policy(**query)
            changed = True
        else:
            if not query['operation_definition']:
                del query['operation_definition']
            if not self.params['pattern']:
                del query['trigger']

            changed = self._require_update(policy)
            policy = self.conn.cbr.update_policy(policy=policy.id, **query)
        self.exit(
            policy=policy,
            changed=changed
        )


def main():
    module = CBRPolicyModule()
    module()


if __name__ == '__main__':
    main()
