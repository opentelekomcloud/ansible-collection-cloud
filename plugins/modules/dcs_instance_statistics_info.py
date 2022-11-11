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
module: dcs_instance_statistics_info
short_description: Get Instance Statistics
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.2"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get Instance Statistics
options:
  instance_id:
    description:
      - Instance ID to filter results for that instance
    type: str
    required: false
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
instances:
    description: Dictionary of Metrics
    returned: changed
    type: list
    sample: [
        "instances": [
            {
                "cmd_get_count": 0,
                "cmd_set_count": 0,
                "id": "12345678-20fb-441b-a0cd-46369a9f7db0",
                "input_kbps": "0.06",
                "instance_id": "12345678-20fb-441b-a0cd-46369a9f7db0",
                "keys": 0,
                "max_memory": 6554,
                "name": null,
                "output_kbps": "1.44",
                "used_cpu": "0.0",
                "used_memory": 4
            }
        ]
    ]
'''

EXAMPLES = '''
# Query statistics about all instances
- opentelekomcloud.cloud.dcs_instance_statistics_info:

# Query statistics about a specific instance
- opentelekomcloud.cloud.dcs_instance_statistics_info:
        instance_id: "12345678-b17b-434d-b6a1-4cc5abb1f2ca"
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DcsInstanceStatisticsInfoModule(OTCModule):
    argument_spec = dict(
        instance_id=dict(required=False),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        final_data = []

        for raw in self.conn.dcs.statistics():
            dt = raw.to_dict()
            dt.pop('location')
            if self.params['instance_id']:
                if raw.instance_id == self.params['instance_id']:
                    final_data = dt
                    break
            else:
                final_data.append(dt)

        self.exit(
            changed=False,
            instances=final_data
        )


def main():
    module = DcsInstanceStatisticsInfoModule()
    module()


if __name__ == '__main__':
    main()
