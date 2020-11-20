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
module: ces_event_data_info
short_description: Get Event Data
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.2.1"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get Event Data
options:
  namespace:
    description:
      - Namespace of a service
    type: str
    required: true
  type:
    description:
      - Specifies the event type
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
events:
    description: Dictionary of Event Data
    returned: changed
    type: list
    sample: [
      {
        "datapoints": [
        {
            "type": "instance_host_info",
            "timestamp": 1450231200000,
            "value": "xxx"
        },
        {
            "type": "instance_host_info",
            "timestamp": 1450231800000,
            "value": "xxx"
        }
        ]
      }
    ]
'''

EXAMPLES = '''
# Query Event_data with some params
- opentelekomcloud.cloud.ces_event_data_info:
    namespace: "SYS.ECS"
    type: "instance_host_info"
    dim0: "instance_id,12345789-6c9d-4594-9d6b-80da84491bec"
    time_from: "1605480241322"
    time_to: "1605523441322"
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CesEventDataInfoModule(OTCModule):
    argument_spec = dict(
        namespace=dict(required=True),
        type=dict(required=True),
        time_from=dict(required=True),
        time_to=dict(required=True),
        dim0=dict(required=True),
        dim1=dict(required=False),
        dim2=dict(required=False),
    )

    def run(self):

        data = []
        query = {}

        query['namespace'] = self.params['namespace']
        query['type'] = self.params['type']
        query['from'] = self.params['time_from']
        query['to'] = self.params['time_to']
        query['dim.0'] = self.params['dim0']
        if self.params['dim1']:
            query['dim.1'] = self.params['dim1']
            if self.params['dim2']:
                query['dim.2'] = self.params['dim2']

        for raw in self.conn.ces.event_data(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            events=data
        )


def main():
    module = CesEventDataInfoModule()
    module()


if __name__ == '__main__':
    main()
