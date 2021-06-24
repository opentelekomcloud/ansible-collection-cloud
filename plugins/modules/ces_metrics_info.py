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
module: ces_metrics_info
short_description: Get Metrics
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.3.0"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get Metrics
options:
  namespace:
    description:
      - Namespace of the monitored object
    type: str
    required: false
  metric_name:
    description:
      - Name of the metrics object
    type: str
    required: false
  start:
    description:
      - specifies the paging start value
    type: str
    required: false
  order:
    description:
      - specifies the order
    type: str
    choices: [desc, asc]
    default: desc
    required: false
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
metrics:
    description: Dictionary of Metrics
    returned: changed
    type: list
    sample: [
        {
            "dimensions": [
                {
                    "id": null,
                    "location": null,
                    "name": "AutoScalingGroup",
                    "value": "123456789-b94d-4cec-9724-aa6d9f583a30"
                }
            ],
            "id": null,
            "metric_name": "instance_num",
            "name": null,
            "namespace": "SYS.AS",
            "unit": "count"
        },
        {
            "dimensions": [
                {
                    "id": null,
                    "location": null,
                    "name": "AutoScalingGroup",
                    "value": "123456789-85da-4d3b-a071-495af2e90fde"
                }
            ],
            "id": null,
            "metric_name": "instance_num",
            "name": null,
            "namespace": "SYS.AS",
            "unit": "count"
        },
        {
            "dimensions": [
                {
                    "id": null,
                    "location": null,
                    "name": "AutoScalingGroup",
                    "value": "123456789-c57c-4849-88d6-525c2adab35d"
                }
            ],
            "id": null,
            "metric_name": "instance_num",
            "name": null,
            "namespace": "SYS.AS",
            "unit": "count"
        }

    ]
'''

EXAMPLES = '''
# Query Metrics from autoscaling groups
- opentelekomcloud.cloud.ces_metrics_info:
    project_id: 12345678913b49529d2e2c3646691288
    namespace: "SYS.AS"
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CesMetricsInfoModule(OTCModule):
    argument_spec = dict(
        metric_name=dict(required=False),
        namespace=dict(required=False),
        start=dict(required=False),
        order=dict(required=False, type='str', choices=['desc', 'asc'], default='desc'),
        # No dim query as it isn't supported by the API
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        data = []
        query = {}

        if self.params['namespace']:
            query['namespace'] = self.params['namespace']
        if self.params['metric_name']:
            query['metric_name'] = self.params['metric_name']
        if self.params['start']:
            query['start'] = self.params['start']
        query['order'] = self.params['order']

        for raw in self.conn.ces.metrics(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            metrics=data
        )


def main():
    module = CesMetricsInfoModule()
    module()


if __name__ == '__main__':
    main()
