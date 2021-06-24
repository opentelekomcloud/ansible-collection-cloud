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
module: cce_cluster_info
short_description: Get information about CCE clusters
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Artem Goncharov (@gtema)"
description:
  - Get CCE cluster info from the OTC.
options:
  name:
    description:
      - Name of the cluster config.
    type: str
  status:
    description:
      - Status of the group.
    choices: ['available', 'creating', 'deleting']
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
cce_clusters:
    description: List of dictionaries describing AS groups version.
    type: complex
    returned: On Success.
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        metadata:
            description: Cluster Metadata dictionary.
            type: dict
        name:
            description: Cluster Name.
            type: str
        spec:
            description: Cluster specification dictionary.
            type: dict
        status:
            description: Cluster status dictionary.
            type: dict
'''

EXAMPLES = '''
# Get configs versions.
- cce_cluster_info:
    name: my_cluster
    status: available
  register: data
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CceClusterInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
        status=dict(required=False, choices=['available', 'creating',
                                             'deleting'])
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        name_filter = self.params['name']
        status_filter = self.params['status']

        data = []
        for raw in self.conn.cce.clusters():
            if name_filter and raw.name != name_filter:
                continue
            if status_filter and raw.status != status_filter.lower():
                continue
            dt = raw.to_dict()
            dt.pop('location')
            dt.pop('api_version')
            dt.pop('kind')
            data.append(dt)

        self.exit_json(
            changed=False,
            cce_clusters=data
        )


def main():
    module = CceClusterInfoModule()
    module()


if __name__ == '__main__':
    main()
