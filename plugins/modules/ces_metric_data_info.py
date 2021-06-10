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
module: ces_metric_data_info
short_description: Get Metric Data
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.3.0"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get Metric Data
options:
  namespace:
    description:
      - Namespace of a service
    type: str
    required: true
  metric_name:
    description:
      - Specifies the metric name
    type: str
    required: true
  period:
    description:
      - Specifies the monitoring granularity
    type: int
    required: true
  filter:
    description:
      - Specifies the data rollup method.
    type: str
    required: true
  time_from:
    description:
      - Specifies the start time of the query
    type: str
    required: true
  time_to:
    description:
      - Specifies the end time of the query
    type: str
    required: true
  dim0:
    description:
      - Specifies the first monitoring dimension
    type: str
    required: true
  dim1:
    description:
      - Specifies the second monitoring dimension
    type: str
    required: false
  dim2:
    description:
      - Specifies the second monitoring dimension
    type: str
    required: false
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
metricdata:
    description: Dictionary of Metric Data
    returned: changed
    type: list
    sample: [
      {
        "datapoints": [
            {
                "average": 0.08085808580858085,
                "id": null,
                "location": null,
                "maximum": null,
                "minimum": null,
                "name": null,
                "sumspec": null,
                "timestamp": 1605617122000,
                "unit": "%",
                "variance": null
            },
            {
                "average": 0.06333333333333334,
                "id": null,
                "location": null,
                "maximum": null,
                "minimum": null,
                "name": null,
                "sumspec": null,
                "timestamp": 1605617422000,
                "unit": "%",
                "variance": null
            },
            {
                "average": 0.057239057239057235,
                "id": null,
                "location": null,
                "maximum": null,
                "minimum": null,
                "name": null,
                "sumspec": null,
                "timestamp": 1605617719000,
                "unit": "%",
                "variance": null
            },
            {
                "average": 0.080327868852459,
                "id": null,
                "location": null,
                "maximum": null,
                "minimum": null,
                "name": null,
                "sumspec": null,
                "timestamp": 1605618024000,
                "unit": "%",
                "variance": null
            }
        ],
        "id": null,
        "metric_name": cpu_util,
        "name": null
      }
    ]
'''

EXAMPLES = '''
# Query Metric Data from CPU Utilization of an ECS instance
- opentelekomcloud.cloud.ces_metric_data_info:
    namespace: "SYS.ECS"
    metric_name: "cpu_util"
    time_from: "1605617014387"
    time_to: "1605618214387"
    period: 1
    filter: average
    dim0: "instance_id,123456789-6c9d-4594-9d6b-80da84491bec"
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CesMetricDataInfoModule(OTCModule):
    argument_spec = dict(
        namespace=dict(required=True),
        metric_name=dict(required=True),
        time_from=dict(required=True),
        time_to=dict(required=True),
        period=dict(required=True, type='int'),
        filter=dict(required=True),
        dim0=dict(required=True),
        dim1=dict(required=False),
        dim2=dict(required=False),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        data = []
        query = {}

        query['namespace'] = self.params['namespace']
        query['from'] = self.params['time_from']
        query['to'] = self.params['time_to']
        query['metric_name'] = self.params['metric_name']
        query['period'] = self.params['period']
        query['filter'] = self.params['filter']
        query['dim.0'] = self.params['dim0']
        if self.params['dim1']:
            query['dim.1'] = self.params['dim1']
            if self.params['dim2']:
                query['dim.2'] = self.params['dim2']

        for raw in self.conn.ces.metric_data(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            metricdata=data
        )


def main():
    module = CesMetricDataInfoModule()
    module()


if __name__ == '__main__':
    main()
