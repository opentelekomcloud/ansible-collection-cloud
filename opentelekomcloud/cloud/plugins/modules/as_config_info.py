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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: as_config_info
short_description: Get AutoScaling configs
extends_documentation_fragment: opentelekomcloud.cloud.otc.doc
version_added: "2.9"
author: "Artem Goncharov (@gtema)"
description:
  - Get AS config info from the OTC.
options:
  name:
    description:
      - Name of the AS config.
    type: str
  image_id:
    description:
      - ID of the image to filter results.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
as_configs:
    description: List of dictionaries describing AutoScaling Configs.
    type: complex
    returned: On Success.
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        name:
            description: Name (version) of the datastore.
            type: str
            sample: "10.0"
'''

EXAMPLES = '''
# Get configs versions.
- as_config_info:
  register: as

- as_config_info:
    name: my_fake_config
  register: as
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class AutoScalingConfigInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
        image_id=dict(required=False)
    )

    def run(self):
        name_filter = self.params['name']
        image_id_filter = self.params['image_id']

        data = []
        # TODO: Pass filters into SDK
        for raw in self.conn.auto_scaling.configs():
            if name_filter and raw.name != name_filter:
                continue
            if (image_id_filter
                    and raw.instance_config['image_id'] != image_id_filter):
                continue
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit_json(
            changed=False,
            as_configs=data
        )


def main():
    module = AutoScalingConfigInfoModule()
    module()


if __name__ == '__main__':
    main()
