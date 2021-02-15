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
module: as_policy
short_description: Create/Remove Auto Scaling Policy from the OTC
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.6.0"
author: "Irina Pereiaslavskaia (@irina-pereiaslavskaia)"
description:
  - Create/Remove Auto Scaling Policy from the OTC.
options:
  scaling_policy:
    description:
      - Specifies the AS policy name or ID.
      - Max name length is 64 characters.
      - Name can contains only letters, digits, underscores, hyphens
    type: str
    required: true
  scaling_group:
    description:
      - Name or ID of the AS group.
    type: str
  scaling_policy_type:
    description:
      - Specifies the AS policy type
    choices: [alarm, scheduled, recurrence]
    type: str
  alarm_id:
    description:
      - Specifies the periodic or scheduled AS policy.
      - This parameter is mandatory when scaling_policy_type is set to ALARM.
    type: str
  scheduled_policy:
    description:
      - Specifies the periodic or scheduled AS policy.
      - This parameter is mandatory when scaling_policy_type is set to \
      SCHEDULED or RECURRENCE.
    type: dict
    suboptions:
      launch_time:
        description:
          - Specifies the time when the scaling action is triggered.
          - The time format complies with UTC.
          - If scaling_policy_type is set to SCHEDULED,\
          the time format is YYYY-MM-DDThh:mmZ.
          - If scaling_policy_type is set to RECURRENCE,\
          the time format is hh:mm.
        type: str
      recurrence_type:
        description:
          - Specifies the periodic triggering type.
          - This parameter is mandatory when scaling_policy_type \
          is set to RECURRENCE.
        choices: [daily, weekly, monthly]
        type:str
      recurrence_value:
        description:
          - Specifies the day when a periodic scaling action is triggered.
          - This parameter is mandatory when scaling_policy_type is set \
          to RECURRENCE.
          - If recurrence_type is set to "Daily", the value is null, \
          indicating that the scaling action is triggered once a day.
          - If recurrence_type is set to Weekly, the value ranges from \
          1 (Sunday) to 7 (Saturday). The digits refer to dates in each \
          week and separated by a comma, such as 1,3,5.
          - If recurrence_type is set to Monthly, the value ranges \
          from 1 to 31. The digits refer to the dates in each month \
          and separated by a comma, such as 1,10,13,28.
        type: str
      start_time:
        description:
          - Specifies the start time of the scaling action triggered \
          periodically.
          - The time format complies with UTC.
          - The default value is the local time.
          - The time format is YYYY-MM-DDThh:mmZ.
        type: str
      end_time:
        description:
          - Specifies the end time of the scaling action triggered \
          periodically.
          - The end time cannot be earlier than the current and start time.
          - The time format complies with UTC.
          - The time format is YYYY-MM-DDThh:mmZ.
        type: str
  scaling_policy_action:
    description:
      - Specifies the scaling action of the AS policy.
    type: dict
    suboptions:
      operation:
        description:
          - Specifies the operation to be performed.
          - The default operation is ADD.
        type: str
        choices: [add, remove, reduce, set]
        default: add
      instance_number:
        description:
          - Specifies the number of instances to be operated.
          - The default number is 1.
          - If operation is set to SET, the value range is 0 to 200.
          - If operation is set to ADD, REMOVE or REDUCE,\
          the value range is 1 to 200.
        type: int
        default: 1
      instance_percentage:
        description:
          - Specifies the percentage of instances to be operated.
          - If operation is set to ADD, REMOVE or REDUCE, \
          the value of this parameter is an integer from 1 to 20000.
          - If operation is set to SET, the value is an integer \
          from 0 to 20000.
          - Either instance_number or instance_percentage is required.
          - If neither instance_number nor instance_percentage is specified,\
           the number of instances to be operated is 1.
        type: int
  cool_down_time:
    description:
      - Specifies the cooldown period (in seconds).
      - The value ranges from 0 to 86400
    type: int
    default: 300
  state:
    description:
      - Whether resource should be present or absent.
    choices: [present, absent]
    type: str
    default: "present"
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
as_policy:
  description: AS policy ID.
  type: complex
  returned: success
  contains:
    scaling_policy_id:
      description: Specifies the AS policy ID.
      type: str
      sample: "0h327883-324n-4dzd-9c61-68d03ee191dd"
'''

EXAMPLES = '''
#
- opentelekomcloud.cloud.as_policy:
    scaling_group: "as-group-test"
    scaling_policy: "collection-test"
    scaling_policy_type: "alarm"
    alarm_id: "as-alarm-test"
  register: result

'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class ASPolicyModule(OTCModule):
    argument_spec = dict(
        scaling_policy=dict(type='str', required=True),
        scaling_group=dict(type='str', required=True),
        scaling_policy_type=dict(type='str', required=False,
                                 choices=['alarm', 'scheduled', 'recurrence']),
        alarm_id=dict(type='str', required=False),
        scheduled_policy=dict(type='dict', required=False, options=dict(
            launch_time = dict(type = 'str', required = False),
            recurrence_type = dict(type = 'str', required = False,
                                   choices = ['daily', 'weekly', 'monthly']),
            recurrence_value = dict(type = 'str', required = False),
            start_time = dict(type = 'str', required = False),
            end_time = dict(type = 'str', required = False),
        )),
        scaling_policy_action=dict(type='dict',required=False,options=dict(
            operation = dict(type = 'str', required = False, default = 'add',
                             choices = ['add', 'remove', 'reduce', 'set']),
            instance_number = dict(type = 'int', required = False,
                                   default = 1),
            instance_percentage = dict(type = 'int', required = False)
        )),
        cool_down_time=dict(type='int', required=False, default=300),
        state=dict(type='str', required=False,choices=['present', 'absent'])
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    otce_min_version = '0.7.1'

    def _get_attrs_for_policy_update(self,policy, filters=None):
        pass

    def _needs_update(self,policy, filters):
        pass

    def _system_state_change(self, obj, filters=None):
        state = self.params['state']
        if state == 'present':
            if not obj:
                return True
            return self._needs_update(obj, filters)
        elif state == 'absent' and obj:
            return True
        return False

    def run(self):

        as_policy = self.params['scaling_policy']
        as_group = self.params['scaling_group']
        as_policy_type = self.params['scaling_policy_type']
        alarm_id = self.params['alarm_id']
        scheduled_policy = self.params['scheduled_policy']
        launch_time = scheduled_policy['launch_time']
        recurrence_type = scheduled_policy['recurrence_type']
        recurrence_value = scheduled_policy['recurrence_value']
        start_time = scheduled_policy['start_time']
        end_time = scheduled_policy['end_time']
        scaling_policy_action = self.params['scaling_policy_action']
        operation = scaling_policy_action['operation']
        instance_number = scaling_policy_action['instance_number']
        instance_percentage = scaling_policy_action['instance_percentage']
        cool_down_time = self.params['cool_down_time']
        state = self.params['state']

        attrs = {}

        changed = False

        if as_group:
            group = self.conn.auto_scaling.find_group(
                name_or_id=as_group
            )
            if group:
                if as_policy:
                    policy = self.conn.auto_scaling.find_policy(
                        name_or_id=as_policy,
                        group=group.id
                    )
                    if policy:
                        if state == 'present':
                            #update
                            #collect attrs for updating
                            if policy.name != as_policy and policy.id != as_policy:
                                attrs['name'] = as_policy
                            if as_policy_type and policy.type != as_policy_type.upper():
                                attrs['type'] = as_policy_type.upper()
                            if as_policy_type == 'alarm':
                                if alarm_id:
                                    attrs['alarm_id'] = alarm_id
                                elif policy.alarm_id is None:
                                    self.fail(changed=changed, msg='Alarm id is required')
                            elif as_policy_type == 'scheduled' or as_policy_type == 'recurrence':
                                if launch_time:
                                    attrs['scheduled_policy']['launch_time'] = launch_time
                                elif policy.scheduled_policy.launch_time is None:
                                    self.fail(changed=changed, msg='Launch time is required')
                            elif as_policy_type == 'scheduled':
                                if recurrence_type and policy.scheduled_policy.recurrence_type != recurrence_type.title():
                                    attrs['scheduled_policy']['recurrence_type'] = recurrence_type.title()
                                if recurrence_value and policy.scheduled_policy.recurrence_value != recurrence_value:
                                    attrs['scheduled_policy']['recurrence_value'] = recurrence_value
                                if start_time and policy.scheduled_policy.start_time != start_time:
                                    attrs['scheduled_policy']['start_time'] = start_time
                                if end_time and policy.scheduled_policy.end_time != end_time:
                                    attrs['scheduled_policy']['end_time'] = end_time
                            elif as_policy_type == 'recurrence':
                                if recurrence_type and policy.scheduled_policy.recurrence_type != recurrence_type.title():
                                    attrs['scheduled_policy']['recurrence_type'] = recurrence_type.title()
                                elif policy.scheduled_policy.recurrence_type is None:
                                    self.fail(changed=changed, msg='Recurrence type is required')
                                if recurrence_value and policy.scheduled_policy.recurrence_value != recurrence_value:
                                    attrs['scheduled_policy']['recurrence_value'] = recurrence_value
                                elif policy.scheduled_policy.recurrence_value is None:
                                    self.fail(changed=changed, msg='Recurrence value is required')
                                if start_time and policy.scheduled_policy.start_time != start_time:
                                    attrs['scheduled_policy']['start_time'] = start_time
                                if end_time and policy.scheduled_policy.end_time != end_time:
                                    attrs['scheduled_policy']['end_time'] = end_time
                                elif policy.scheduled_policy.end_time is None:
                                    self.fail(changed=changed, msg='End time is required')
                            if operation and policy.scaling_policy_action.operation != operation.upper():
                                attrs['scaling_policy_action']['operation'] = operation.upper()
                            if instance_number and policy.scaling_policy_action.instance_number != instance_number:
                                attrs['scaling_policy_action']['instance_number'] = instance_number
                            if instance_percentage and policy.scaling_policy_action.instance_percentage != instance_percentage:
                                attrs['scaling_policy_action']['instance_percentage'] = instance_percentage
                            if cool_down_time and policy.cool_down_time != cool_down_time:
                                attrs['cool_down_time'] = cool_down_time
                            #update policy
                            policy = self.conn.auto_scaling.update_policy(policy=policy, **attrs)
                            changed = True
                            self.exit(changed=changed, policy=policy.to_dict(),
                                      id=policy.id, msg='Scaling policy %s was created' % as_policy)

                        elif state == 'absent':
                            #delete policy
                            self.conn.auto_scaling.delete_policy(policy=policy)
                            changed = True
                            self.exit(changed=changed, msg='Scaling policy %s was deleted' % as_policy)
                    else:
                        if state == 'present':
                            #create policy
                            #collect attrs for updating
                            attrs['name'] = as_policy
                            if as_policy_type:
                                attrs['type'] = as_policy_type.upper()
                            else:
                                self.fail(changed=changed, msg='Scaling policy type is required')
                            if as_policy_type == 'alarm':
                                if alarm_id:
                                    attrs['alarm_id'] = alarm_id
                                elif policy.alarm_id is None:
                                    self.fail(changed=changed, msg='Alarm id is required')
                            if as_policy_type == 'scheduled' or as_policy_type == 'recurrence':
                                if launch_time:
                                    attrs['scheduled_policy']['launch_time'] = launch_time
                                else:
                                    self.fail(changed=changed, msg='Launch time is required')
                            if as_policy_type == 'scheduled':
                                if recurrence_type:
                                    attrs['scheduled_policy']['recurrence_type'] = recurrence_type.title()
                                if recurrence_value:
                                    attrs['scheduled_policy']['recurrence_value'] = recurrence_value
                                if start_time:
                                    attrs['scheduled_policy']['start_time'] = start_time
                                if end_time:
                                    attrs['scheduled_policy']['end_time'] = end_time
                            if as_policy_type == 'recurrence':
                                if recurrence_type:
                                    attrs['scheduled_policy']['recurrence_type'] = recurrence_type.title()
                                else:
                                    self.fail(changed=changed, msg='Recurrence type is required')
                                if recurrence_value:
                                    attrs['scheduled_policy']['recurrence_value'] = recurrence_value
                                else:
                                    self.fail(changed=changed, msg='Recurrence value is required')
                                if start_time:
                                    attrs['scheduled_policy']['start_time'] = start_time
                                if end_time:
                                    attrs['scheduled_policy']['end_time'] = end_time
                                else:
                                    self.fail(changed=changed, msg='End time is required')
                            if operation:
                                attrs['scaling_policy_action']['operation'] = operation.upper()
                            if instance_number:
                                attrs['scaling_policy_action']['instance_number'] = instance_number
                            if instance_percentage:
                                attrs['scaling_policy_action']['instance_percentage'] = instance_percentage
                            if cool_down_time:
                                attrs['cool_down_time'] = cool_down_time
                            policy = self.conn.auto_scaling.create_policy(**attrs)
                            changed = True
                            self.exit(changed=changed, policy=policy.to_dict(),
                                      id=policy.id, msg='Scaling policy %s was created' % policy)
                        else:
                            self.fail(
                                changed=changed,
                                msg='Policy %s not found' % policy
                            )
                else:
                    self.fail(
                        changed=changed,
                        msg='Scaling policy is missing'
                    )
            else:
                self.fail(
                    changed=changed,
                    msg='AS group %s not found' % group
                )
        else:
            self.fail(
                changed=changed,
                msg='Scaling group is missing'
            )


def main():
    module = ASPolicyModule()
    module()


if __name__ == "__main__":
    main()
