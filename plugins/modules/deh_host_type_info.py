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
module: deh_host_type_info
short_description: Get info about all available host types in a AZ
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Tino Schreiber (@tischrei)"
description:
  - Get info about all available host types in a AZ
options:
  az:
    description:
      - Availability zone where host types are requested
    type: str
    required: true
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
deh_host_types:
    description: Dictionary of host types in an Availability Zone
    returned: success
    type: list
    sample: [
      {
            "host_type": "s2-medium",
            "host_type_name": "s2-medium",
            "id": null,
            "name": null
        },
        {
            "host_type": "m3",
            "host_type_name": "Memory Optimized",
            "id": null,
            "name": null
        },
        {
            "host_type": "c3",
            "host_type_name": "General Exclusive",
            "id": null,
            "name": null
        },
        {
            "host_type": "s2",
            "host_type_name": "General Computing usage",
            "id": null,
            "name": null
        },
        {
            "host_type": "h1",
            "host_type_name": "High performance",
            "id": null,
            "name": null
        },
        {
            "host_type": "general",
            "host_type_name": "General computing",
            "id": null,
            "name": null
        }
    ]
'''

EXAMPLES = '''
# Query all host types in an Availability Zone
- deh_host_type_info:
    cloud: "{{ test_cloud }}"
    az: eu-de-01
  register: deh
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DehHostTypeInfoModule(OTCModule):
    argument_spec = dict(
        az=dict(required=True)
    )

    def run(self):

        data = []
        query = {}

        if self.params['az']:
            query['az'] = self.params['az']

        for raw in self.conn.deh.host_types(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            deh_host_types=data
        )


def main():
    module = DehHostTypeInfoModule()
    module()


if __name__ == '__main__':
    main()
