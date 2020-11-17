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
module: ces_alarms_info
short_description: Get Alarms
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get Alarms
options:
  name:
    description:
      - Name of an Alarm
    type: str
    required: false
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
deh_servers:
    description: Dictionary of Alarms
    returned: changed
    type: list
    sample: [
      {
            "alarm_action_enabled": false,
            "alarm_actions": null,
            "alarm_description": "",
            "alarm_enabled": true,
            "alarm_id": "al3455101172209DmyNj39MW",
            "alarm_level": 2,
            "alarm_state": "ok",
            "condition": {
                "comparison_operator": ">=",
                "count": 3,
                "filter": "average",
                "id": null,
                "location": null,
                "name": null,
                "period": 1,
                "unit": "%",
                "value": 90
            },
            "id": "al3455101172209DmyNj39MW",
            "metric": {
                "dimensions": [
                    {
                        "id": null,
                        "location": null,
                        "name": "instance_id",
                        "value": "23232323-6c9d-4594-9d6b-80da84491bec"
                    }
                ],
                "id": null,
                "location": null,
                "metric_name": "cpu_util",
                "name": null,
                "namespace": "SYS.ECS"
            },
            "name": "alarm-t2tn",
            "ok_actions": null,
            "update_time": 1625101172297

      }
    ]
'''

EXAMPLES = '''
# Query Alarms with the name "test-alarm"
- opentelekomcloud.cloud.ces_alarms_info:
    name: test-alarm
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CesAlarmsInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
    )

    def run(self):

        data = []
        query = {}

        if self.params['name']:
            alarm = self.conn.ces.find_alarm(self.params['name'])
            self.exit(
                changed=False,
                alarms=alarm
            )

        for raw in self.conn.ces.alarms():
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            alarms=data
        )


def main():
    module = CesAlarmsInfoModule()
    module()


if __name__ == '__main__':
    main()
