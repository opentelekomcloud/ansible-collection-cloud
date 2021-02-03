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
module: as_policy_info
short_description: Query AS policies based on search criteria.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.6.0"
author: "Irina Pereiaslavskaia (@irina-pereiaslavskaia)"
description:
  - This interface is used to query AS policies based on search criteria.
options:
  scaling_group:
    description: Specifies the AS group name or ID.
    type: str
    required: true
  scaling_policy:
    description: Specifies the AS policy name or ID.
    type: str
  scaling_policy_type:
    description: Specifies the AS policy type.
    choices: [alarm, scheduled, recurrence]
    type: str
  start_number:
    description: Specifies the start line number.
    type: int
    default: 0
  limit:
    description: Specifies the number of query records.
    type: int
    default: 20
'''

RETURN = '''
as_policies:
  description: Query AS policies based on search criteria.
  type: complex
  returned: success
  contains:
    total_number:
      description: Specifies the total number of query records.
      type: int
      sample: 1
    start_number:
      description: Specifies the start line number.
      type: int
      sample: 0
    limit:
      description: Specifies the maximum number of resources to be queried.
      type: int
      sample: 20
    scaling_policies:
      description: Specifies scaling policies.
      type: complex
      returned: success
      contains:
        scaling_group_id:
          description: Specifies the AS group ID.
          type: str
          sample: "e5d27f5c-dd76-4a61-b4bc-a67c5686719a"
        scaling_policy_name:
          description: Specifies the AS policy name.
          type: str
          sample: "as-policy-test"
        scaling_policy_id:
          description: Specifies the AS policy ID.
          type: str
          sample: "fd7d63ce-8f5c-443e-b9a0-bef9386b23b3"
        policy_status:
          description: Specifies the AS policy status.
          type: str
          sample: "INSERVICE"
        scaling_policy_type:
          description: Specifies the AS policy type.
          type: str
          sample: "SCHEDULED"
        alarm_id:
          description: Specifies the alarm ID.
          type: str
          sample: "al16117680339426q5qYw5gZ"
        cool_down_time:
          description: Specifies the cooldown period.
          type: int
          sample: 300
        create_time:
          description: Specifies the time when an AS policy was created.
          type: str
          sample: "2015-07-24T01:21Z"
        scheduled_policy:
          description: Specifies the periodic or scheduled AS policy.
          type: complex
          returned: success
          contains:
            launch_time:
              description: The time when the scaling action is triggered.
              type: str
              sample: "2015-07-24T01:21Z"
            recurrence_type:
              description: The type of a periodically triggered scaling action.
              type: str
              sample: "Daily"
            recurrence_value:
              description: The frequency at which scaling actions are triggered.
              type: str
            start_time:
              description: The start time of the scaling action triggered.
              type: str
              sample: "2015-07-24T01:21Z"
            end_time:
              description: The end time of the scaling action triggered.
              type: str
              sample: "2015-07-24T01:21Z"
        scaling_policy_action:
          description: Specifies the scaling action of the AS policy.
          type: complex
          returned: success
          contains:
            operation:
              description: Specifies the scaling action.
              type: str
              sample: "ADD"
            instance_number:
              description: The number of instances to be operated.
              type: int
              sample: 1
            instance_percentage:
              description: The percentage of instances to be operated.
              type: int
'''

EXAMPLES = '''
# Get Auto Scaling Policies
- opentelekomcloud.cloud.as_policy_info:
    scaling_group: "89af599d-a8ab-4c29-a063-0b719ed77e8e"
  register: as_policies

# Get Auto Scaling Policies
- opentelekomcloud.cloud.as_policy_info:
    scaling_group: "test_group"
    scaling_policy: "test_name"
    scaling_policy_type: "alarm"
    start_number: 2
    limit: 20
  register: as_policies

# Get Auto Scaling Policies
- opentelekomcloud.cloud.as_policy_info:
    scaling_group: "89af599d-a8ab-4c29-a063-0b719ed77e8e"
    scaling_policy: "c3e1c13e-a5e5-428e-a8bc-6c5fc0f4b3f5"
    scaling_policy_type: "alarm"
    start_number: 2
    limit: 20
  register: as_policies
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class ASPolicyInfoModule(OTCModule):
    argument_spec = dict(
        scaling_group=dict(type='str', required=True),
        scaling_policy=dict(type='str', required=False),
        scaling_policy_type=dict(type='str',
                                 choices=["alarm", "scheduled", "recurrence"],
                                 required=False),
        start_number=dict(type='int', required=False, default=0),
        limit=dict(type='int', required=False, default=20)
    )

    def run(self):
        as_group = self.params['scaling_group']
        as_policy = self.params['scaling_policy']
        as_policy_type = self.params['scaling_policy_type']
        start_number = self.params['start_number']
        limit = self.params['limit']

        data = []
        query = {}
        if as_group:
            group = self.conn.auto_scaling.find_group(
                name_or_id=as_group
            )
            if group:
                query['group'] = group.id
                if as_policy:
                    policy = self.conn.auto_scaling.find_policy(
                        name_or_id=as_policy,
                        group=group.id
                    )
                    if policy:
                        query['name'] = policy.name
                    else:
                        self.exit(
                            changed=False,
                            scaling_policies=[],
                            msg='Policy with %s not found' % as_policy
                        )
                if as_policy_type:
                    query['type'] = as_policy_type.upper()
                if start_number >= 0:
                    query['marker'] = start_number
                if 0 <= limit <= 100:
                    query['limit'] = limit
                else:
                    self.fail(
                        changed=False,
                        msg='Limit is out of range'
                    )
            else:
                self.fail(
                    changed=False,
                    msg='Group %s not found' % group
                )
        else:
            self.fail(
                changed=False,
                msg='Scaling group is missing'
            )

        for raw in self.conn.auto_scaling.policies(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            scaling_policies=data
        )


def main():
    module = ASPolicyInfoModule()
    module()


if __name__ == '__main__':
    main()
