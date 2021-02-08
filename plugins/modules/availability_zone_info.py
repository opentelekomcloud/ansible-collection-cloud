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
module: availability_zone_info
short_description: Get AZ info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.7.0"
author: "Artem Goncharov (@gtema)"
description:
  - Get AZ info.
options:
  name:
    description: The name or ID of a AZ.
    type: str
  service:
    description:
      - Service name to list supported avaiability zones for.
      - Currently only compute is supported
    type: str
    default: compute
requirements: ["openstacksdk"]
'''

RETURN = '''
availability_zone_info:
  description: List of Availability zones.
  type: complex
  returned: On Success.
  contains:
    name:
      description: Specifies the AZ name.
      type: str
'''

EXAMPLES = '''
# Get AZ.
- opentelekomcloud.cloud.availability_zone_info:
  register: az
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class AvailabilityZoneInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(type='str', required=False),
        service=dict(type='str', default='compute')
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        data = []

        raw_data = []
        if self.params['service'] == 'compute':
            raw_data = self.conn.compute.availability_zones()
        if raw_data:
            for raw in raw_data:
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit(
            changed=False,
            availability_zones=data
        )


def main():
    module = AvailabilityZoneInfoModule()
    module()


if __name__ == '__main__':
    main()
