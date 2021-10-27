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
module: css_snapshot_info
short_description: Get CSS snapshot info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.9.0"
author: "Vladimir Vshivkov (@enrrou)"
description:
  - Get Cloud Search Service snapshot info
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
snapshots:
    description: Dictionary of CSS snapshot info
    returned: changed
    type: list
    sample: [
        {
            "id": null,
            "name": null,
            "resources": [
                {
                    "id": null,
                    "location": null,
                    "name": null,
                }
            ]
        }
    ]
'''

EXAMPLES = '''
#Query CSS Snapshots
---
- hosts: localhost
  tasks:
    - name: Get CSS Snapshots
      opentelekomcloud.cloud.css_snapshot_info:
        cluster: test
        project: test
      register: result
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CssSnapshotInfoModule(OTCModule):
    argument_spec = dict(
        cluster=dict(required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )
    def run(self):
        data = []
        query = {
            'cluster': self.params['cluster']
        }
        for raw in self.conn.css.snapshots(**query):
            dt = raw.to_dict()
            data.append(dt)
        self.exit(
            changed=False,
            snapshots=data
        )

def main():
    module = CssSnapshotInfoModule()
    module()


if __name__ == '__main__':
    main()
