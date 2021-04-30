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
module: as_group_info
short_description: Get AutoScaling groups
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Artem Goncharov (@gtema)"
description:
  - Get details about AutoScaling groups available in the project.
options:
  name:
    description:
      - Name of the AS group.
    type: str
  status:
    description:
      - Status of the group.
    choices: ['inservice', 'paused', 'error', 'deleting']
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
as_groups:
    description: List of dictionaries describing AS groups version.
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
- as_group_info:
    name: my_prod_as_group
  register: data
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class AutoScalingGroupInfoModule(OTCModule):

    argument_spec = dict(
        name=dict(required=False),
        status=dict(required=False, choices=[
            'inservice', 'paused', 'error', 'deleting'])
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        name_filter = self.params['name']
        status_filter = self.params['status']

        data = []
        # TODO: Pass filters into SDK
        attrs = {}
        if name_filter:
            attrs['scaling_groups_name'] = name_filter
        if status_filter:
            attrs['scaling_group_status'] = status_filter.upper()
        for raw in self.conn.auto_scaling.groups(**attrs):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit_json(
            changed=False,
            as_groups=data
        )


def main():
    module = AutoScalingGroupInfoModule()
    module()


if __name__ == '__main__':
    main()
