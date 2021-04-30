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
module: ces_alarms
short_description: Modify or Create Alarms
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.3.0"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Modify or Create Alarms
options:
  alarm_description:
    description:
      - Description of the Alarm
    type: str
    default: ""
    required: false
  alarm_name:
    description:
      - Name of the Alarm. Can be an ID too if state == absent
    type: str
    required: true
  metric:
    description:
      - Specifies the Alarm metrics. Required if state == present
    type: dict
    required: false
  state:
    description:
      - Resource state
    type: str
    choices: [present, absent]
    default: present
  condition:
    description:
      - Specifies the alarm triggering condition. Required if state == present
    type: dict
    required: false
  alarm_enabled:
    description:
      - Specifies whether to enable the alarm
    type: bool
    required: false
    default: true
  alarm_action_enabled:
    description:
      - Specifies whether to enable the action to be triggered by an alarm
    type: bool
    required: false
    default: true
  alarm_level:
    description:
      - Specifies the alarm severity. The value can be 1, 2, 3 or 4, which indicates critical, major, minor, and informational, respectively
    type: int
    required: false
    default: 2
  alarm_actions:
    description:
      - Specifies the action triggered by an alarm
    type: list
    required: false
    elements: str
    default: []
  ok_actions:
    description:
      - Specifies the action triggered by clearing an alarm
    type: list
    required: false
    elements: str
    default: []
  switch_alarm_state:
    description:
      - If true switches the alarm state from on to off or off to on. Requires state == present
    type: bool
    required: false
    default: False

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
alarms:
  description: Dictionary of Event Data
  returned: changed
  type: list
  sample: [
      {
        "alarm_action_enabled": true,
        "alarm_actions": {
            "id": null,
            "location": null,
            "name": null,
            "notificationList": null,
            "type": null
        },
        "alarm_description": "",
        "alarm_enabled": true,
        "alarm_id": "al1234506573003nnErvLjNy",
        "alarm_level": 2,
        "alarm_state": null,
        "condition": {
            "comparison_operator": ">=",
            "count": 1,
            "filter": "average",
            "id": null,
            "location": null,
            "name": null,
            "period": 300,
            "unit": "B/s",
            "value": 6
        },
        "id": "al1234506573003nnErvLjNy",
        "location": {
            "cloud": "otc",
            "project": {
                "domain_id": null,
                "domain_name": null,
                "id": "12345a84a13b49529d2e2c3646691288",
                "name": "eu-de"
            },
            "region_name": "eu-de",
            "zone": null
        },
        "metric": {
            "dimensions": [
                {
                    "id": null,
                    "location": null,
                    "name": "instance_id",
                    "value": "123456789-6c9d-4594-9d6b-80da84491bec"
                },
                {
                    "id": null,
                    "location": null,
                    "name": "instance_id",
                    "value": "123456789-0691-4896-8e19-1046b727d4e2"
                }
            ],
            "id": null,
            "location": null,
            "metric_name": "network_outgoing_bytes_rate_inband",
            "name": null,
            "namespace": "SYS.ECS"
        },
        "name": "alarm-sgode",
        "ok_actions": {
            "id": null,
            "location": null,
            "name": null,
            "notificationList": null,
            "type": null
        },
        "update_time": null
      }

  ]
'''

EXAMPLES = '''
# Creating an Alarm with two instances in it:
- name: Creating a alarm
  opentelekomcloud.cloud.ces_alarms:
    alarm_name: alarm-test
    state: present
    metric:
      namespace: "SYS.ECS"
      dimensions:
        - name: "instance_id"
          value: "123456789-6c9d-4594-9d6b-80da84491bec"
        - name: "instance_id"
          value: "123456789-0691-4896-8e19-1046b727d4e2"
      metric_name: "network_outgoing_bytes_rate_inband"
    condition:
      period: 300
      filter: average
      comparison_operator: ">="
      value: 6
      unit: "B/s"
      count: 1
    alarm_enabled: True
    ok_actions:
      - type: notification
        notificationList:
          - "urn:smn:region:12345a86d98e427e907e0097b7e35d48:sd"
    alarm_actions:
      - type: notification
        notificationList:
          - "urn:smn:region:12345a86d98e427e907e0097b7e35d48:sd"
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
        alarm_actions=dict(required=False, type='list', elements='str', default=[]),
        ok_actions=dict(required=False, type='list', elements='str', default=[]),
        switch_alarm_state=dict(required=False, type='bool', default='False'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        changed = False

        if self.params['state'] == 'absent':
            changed = False
            al = self.conn.ces.find_alarm(self.params['alarm_name'])
            if self.ansible.check_mode:
                self.exit(changed=True)
            self.conn.ces.delete_alarm(al)
            changed = True

        if self.params['state'] == 'present':

            if self.params['switch_alarm_state'] is True:
                al = self.conn.ces.find_alarm(self.params['alarm_name'])
                if self.ansible.check_mode:
                    self.exit(changed=True)
                alarms = self.conn.ces.switch_alarm_state(al)
                self.exit(changed=True, alarms=al.to_dict())

            elif self.params['switch_alarm_state'] is False:
                if not self.params['metric'] or not self.params['condition']:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('You want to create an Alarm but did not specify '
                                 'metric or condition parameters which are required for creation ')
                    )
                metric_var = self.params["metric"]
                condition_var = self.params['condition']

                if self.params['alarm_action_enabled']:
                    if self.params['ok_actions'] == [] and self.params['alarm_actions'] == []:
                        self.exit(
                            changed=False,
                            failed=True,
                            message=('alarm_action_enabled == True but neither ok_actions '
                                     'nor alarm_action specified but needed for creation. ')
                        )
                if self.ansible.check_mode:
                    self.exit(changed=True)
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

                alarms = self.conn.ces.create_alarm(**attrs)
                self.exit(changed=True, alarms=alarms.to_dict())

        self.exit(
            changed=changed
        )


def main():
    module = CesAlarmsModule()
    module()


if __name__ == '__main__':
    main()
