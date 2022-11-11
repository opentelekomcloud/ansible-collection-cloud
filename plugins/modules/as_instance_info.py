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
module: as_instance_info
short_description: Query Instances in an AS Group.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.0"
author: "Irina Pereiaslavskaia (@irina-pereiaslavskaia)"
description:
  - This interface is used to query Instances in an AS Group \
  based on search criteria.
options:
  scaling_group:
    description:
      - Specifies the AS group name or ID.
    type: str
    required: true
  lifecycle_state:
    description:
      - Specifies the instance lifecycle status in the AS group.
      - If it set to INSERVICE, the instance is enabled.
      - If it set to PENDING, the instance is being added to the AS group.
      - If it set to REMOVING, the instance is being removed from the AS group.
    choices: [inservice, pending, removing]
    type: str
  health_status:
    description:
      - Specifies the instance health status.
      - If it set to INITIALIZING, the instance is initializing.
      - If it set to NORMAL, the instance is normal.
      - If it set to ERROR, the instance is abnormal.
    choices: [initializing, normal, error]
    type: str
  start_number:
    description:
      - Specifies the start line number.
    type: int
    default: 0
  limit:
    description:
      - Specifies the number of query records.
      - The value range is 0 to 100.
    type: int
    default: 20
'''

RETURN = '''
scaling_instances:
  description:
    - Query Instances in an AS Group based on search criteria.
  type: complex
  returned: success
  contains:
    total_number:
      description:
        - Specifies the total number of query records.
      type: int
      sample: 1
    start_number:
      description:
        - Specifies the start line number.
      type: int
      sample: 10
    limit:
      description:
        - Specifies the maximum number of resources to be queried.
      type: int
      sample: 10
    scaling_group_instances:
      description:
        - Specifies details about the instances in the AS group.
      type: complex
      returned: success
      contains:
        instance_id:
          description:
            - Specifies the instance ID.
          type: str
          sample: "b25c1589-c96c-465b-9fef-d06540d1945c"
        instance_name:
          description:
            - Specifies the instance name.
          type: str
          sample: "discuz_3D210808"
        scaling_group_id:
          description:
            - Specifies the ID of the AS group to which the instance belongs.
          type: str
          sample: "e5d27f5c-dd76-4a61-b4bc-a67c5686719a"
        scaling_group_name:
          description:
            - Specifies the name of the AS group to which the instance belongs.
            - Supports fuzzy search.
          type: str
          sample: "test_group_name"
        lifecycle_state:
          description:
            - Specifies the instance lifecycle status in the AS group.
            - INSERVICE means that the instance is enabled.
            - PENDING means that the instance is being added to the AS group.
            - REMOVING means that the instance is being removed from the AS group.
          type: str
          sample: "INSERVICE"
        health_status:
          description:
            - Specifies the instance health status.
            - INITIALIZING means that the instance is being initialized.
            - NORMAL means that the instance is functional.
            - ERROR means that the instance is faulty.
          type: str
          sample: "NORMAL"
        scaling_configuration_name:
          description:
            - Specifies the AS configuration name.
          type: str
          sample: "test_config"
        scaling_configuration_id:
          description:
            - Specifies the AS configuration ID.
            - If the returned value is not empty, the instance is \
            an ECS automatically created in a scaling action.
            - If the returned value is empty, the instance is \
            an ECS manually added to the AS group.
          type: str
          sample: "ca3dcd84-d197-4c4f-af2a-cf8ba39696ac"
        create_time:
          description:
            - Specifies the time when the instance is added to the AS group.
            - The time format complies with UTC.
          type: str
          sample: "2021-02-23T06:47:33Z"
        protect_from_scaling_down:
          description:
            - Specifies the instance protection status.
          type: bool
          sample: "true"
'''

EXAMPLES = '''
# Get Instances in an AS Group
- opentelekomcloud.cloud.as_instance_info:
    scaling_group: "89af599d-a8ab-4c29-a063-0b719ed77e8e"
  register: as_instances

# Get Instances in an AS Group
- opentelekomcloud.cloud.as_instance_info:
    scaling_group: "test_group"
    start_number: 2
    limit: 20
  register: as_instances

# Get Instances in an AS Group
- opentelekomcloud.cloud.as_instance_info:
    scaling_group: "89af599d-a8ab-4c29-a063-0b719ed77e8e"
    start_number: 2
    limit: 20
  register: as_instances
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class ASInstanceInfoModule(OTCModule):
    argument_spec = dict(
        scaling_group=dict(type='str', required=True),
        lifecycle_state=dict(type='str', required=False,
                             choices=["inservice", "pending", "removing"]),
        health_status=dict(type='str', required=False,
                           choices=["initializing", "normal", "error"]),
        start_number=dict(type='int', required=False, default=0),
        limit=dict(type='int', required=False, default=20)
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        as_group = self.params['scaling_group']
        lifecycle_state = self.params['lifecycle_state']
        health_status = self.params['health_status']
        start_number = self.params['start_number']
        limit = self.params['limit']

        data = []
        query = {}

        try:
            group = self.conn.auto_scaling.find_group(
                name_or_id=as_group,
                ignore_missing=False
            )
            query['group'] = group.id

        except self.sdk.exceptions.ResourceNotFound:
            self.fail(
                changed=False,
                msg='Scaling group %s not found' % as_group
            )

        if lifecycle_state:
            query['lifecycle_state'] = lifecycle_state.upper()

        if health_status:
            query['health_status'] = health_status

        if start_number >= 0:
            query['marker'] = start_number

        if 0 <= limit <= 100:
            query['limit'] = limit

        else:
            self.fail(
                changed=False,
                msg='Limit is out of range'
            )

        for raw in self.conn.auto_scaling.instances(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            scaling_instances=data
        )


def main():
    module = ASInstanceInfoModule()
    module()


if __name__ == '__main__':
    main()
