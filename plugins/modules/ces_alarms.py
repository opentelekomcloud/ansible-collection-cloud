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
module: dns_alarms
short_description: Modify or Create Alarms
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Modify or Create Alarms
options:
  description:
    description:
      - Description of the Record
    type: str
  floating_ip:
    description:
      - Name or ID of the floating ip
    type: str
    required: true
  ptrdname:
    description:
      - Domain name of the PTR record required if updating/creating rule
    type: str
  state:
    description:
      - Resource state
    type: str
    choices: [present, absent]
    default: present
  ttl:
    description:
      - PTR record cache duration (in second) on a local DNS server
    type: int

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
ptr:
  description: Modify or Create Alarms
  type: complex
  returned: On Success.
  contains:
    description:
      description: Description of the Record
      type: str
      sample: "MyRecord123"
    floating_ip:
      description: Name or ID of the floating ip
      type: str
      sample: "123.123.123.123"
    ptrdname:
      description: Domain name of the PTR record required if updating/creating rule
      type: str
      sample: "example.com"
    status:
      description: Resource status
      type: str
      sample: "ACTIVE"
    ttl:
      description: PTR record cache duration (in second) on a local DNS server
      type: int
      sample: 300
'''

EXAMPLES = '''
# Creating a record:
- name: Creating a record
  opentelekomcloud.cloud.dns_floating_ip:
    floating_ip: 123.123.123.123
    ptrdname: "test2.com."
    description: "test2nownow"
    ttl: 300
    state: present
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CesAlarmsModule(OTCModule):
    argument_spec = dict(
        alarm_name=dict(required=True),
        alarm_description=dict(required=False, default=''),
        metric=dict(required=False, type='dict'),
        condition=dict(required=False, type='dict'),
        alarm_enabled=dict(required=False, type='bool', default='True'),
        alarm_action_enabled=dict(required=False, type='bool', default='True'),
        alarm_level=dict(required=False, type='int', default=2),
        alarm_actions=dict(required=False, type='list'),
        ok_actions=dict(required=False, type='list'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['metric', 'condition']),
        ],
        supports_check_mode=True
    )

    def run(self):
        changed = False

        if self.params['state'] == 'absent':
            changed = False
            al = self.conn.ces.find_alarm(self.params['alarm_name'])
            self.conn.ces.delete_alarm(al)
            changed = True

        if self.params['state'] == 'present':
            metric_var = self.params["metric"]
            condition_var = self.params['condition']

            if self.params['alarm_action_enabled']:
                if not self.params['ok_actions'] and not self.params['alarm_actions']:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('alarm_action_enabled == True but neither ok_actions '
                                 'nor alarm_action specified but needed for creation. ')
                    )
                if self.params['ok_actions'] and self.params['alarm_actions']:
                    ok_actions_var = self.params['ok_actions']
                    alarm_actions_var = self.params['alarm_actions']

                    if ok_actions_var[0]["notificationList"] != alarm_actions_var[0]['notificationList']:
                        self.exit(
                            changed=False,
                            failed=True,
                            message=('ok_actions and alarm_actions specified but notificationList '
                                    'in them differs which is not allowed. ')
                        )

            attrs = {
                "alarm_name": self.params['alarm_name'],
                "alarm_description": self.params['alarm_description'],
                "metric": {
                    "namespace": metric_var['namespace'],
                    "dimensions": metric_var['dimensions'],
                    "metric_name": metric_var['metric_name']
                },
                "condition": {
                    "period": condition_var['period'],
                    "filter": condition_var['filter'],
                    "comparison_operator": condition_var['comparison_operator'],
                    "value": condition_var['value'],
                    "unit": condition_var['unit'],
                    "count": condition_var['count'],
                },
                "alarm_enabled": self.params['alarm_enabled'],
                "alarm_action_enabled": self.params['alarm_action_enabled'],
                "alarm_level": self.params['alarm_level'],
                "ok_actions": self.params['ok_actions'],
                "alarm_actions": self.params['alarm_actions']

            }
        # raise Exception(attrs)
        alarms = self.conn.ces.create_alarm(**attrs)
        self.exit(changed=True, recordset=alarms.to_dict())
            

        self.exit(
            changed=changed
        )


def main():
    module = CesAlarmsModule()
    module()


if __name__ == '__main__':
    main()
