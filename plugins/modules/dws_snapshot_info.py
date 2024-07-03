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
module: dws_snapshot_info
short_description: Get DWS snapshot info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.9.0"
author: "Attila Somogyi (@sattila1999)"
description:
  - Get Data Warehouse Service snapshot info
options:
  name:
    description: The snapshot name of the cluster.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
snapshots:
    description: Dictionary of DWS snapshot info
    returned: changed
    type: list
    sample: [
    {
        "snapshot_list": [
            {
                "cluster_id": "454347e7-b1dd-9cd9-85ab-345b844ff537",
                "created_at": "2024-06-27T08:59:26",
                "description": "",
                "id": "eb6ad554-74c6-4e58-hz2c-f6bab80bf2e6",
                "location": {
                    "cloud": "bigdataai",
                    "project": {
                        "domain_id": null,
                        "domain_name": null,
                        "id": "bd183d0148e94747bf57acf742e7fa52",
                        "name": "eu-de"
                    },
                    "region_name": "eu-de",
                    "zone": null
                },
                "name": "snapshot-1",
                "size": 0.127109,
                "status": "AVAILABLE",
                "type": "AUTO",
                "updated_at": "2024-06-27T09:03:56"
            }
        ]
    }
]
'''

EXAMPLES = '''
#Query DWS Snapshots

- opentelekomcloud.cloud.dws_snapshot_info:
    name: 'test'
  register: result
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DwsSnapshotInfoModule(OTCModule):

    argument_spec = dict(
        name=dict(required=False)
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        data = []
        snapshot_name = self.params['name']

        # search snapshot by name or id
        if self.params['name']:
            snapshot = self.conn.dws.find_snapshot(name_or_id=snapshot_name)
            data.append(snapshot)

        else:
            snapshots = self.conn.dws.snapshots()
            for snapshot in snapshots:
                dt = snapshot.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit_json(
            changed=False,
            dws_snapshots=data
        )


def main():
    module = DwsSnapshotInfoModule()
    module()


if __name__ == '__main__':
    main()
