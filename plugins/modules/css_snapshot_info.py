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
module: css_snapshot_info
short_description: Get CSS snapshot info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.9.0"
author: "Vladimir Vshivkov (@enrrou)"
description:
  - Get Cloud Search Service snapshot info
options:
  cluster:
    description:
     - Name or Id of the CSS cluster, to which
       the snapshot to be queried belongs.
    type: str
  name:
    description: Name or Id of the cluster snapshot.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
snapshots:
    description: Dictionary of CSS snapshot info
    returned: changed
    type: list
    sample: [
    {
        "backups": [
            {
                "created": "2021-11-22T13:00:00",
                "datastore": {
                    "type": "elasticsearch",
                    "version": "7.6.2"
                },
                "description": "",
                "id": "e29d99c1-3d19-4ea4-ae8d-f252df76cbe9",
                "clusterId": "37cb1075-c38e-4cd8-81df-442d52df3786",
                "clusterName": "Es-xfx",
                "name": "snapshot-002",
                "status": "COMPLETED",
                "updated": "2021-11-22T13:00:00",
                "backupType": "1",
                "backupMethod": "manual",
                "backupExpectedStartTime": null,
                "backupKeepDay": null,
                "backupPeriod": null,
                "indices": ".kibana,website2",
                "totalShards": 6,
                "failedShards": 0,
                "version": "6.2.3",
                "restoreStatus": "success",
                "startTime": 1520408087099,
                "endTime": 1520408412219,
                "bucketName": "obs-b8ed"
            },
            {
                "created": "2021-11-22T13:00:00",
                "datastore": {
                    "type": "elasticsearch",
                    "version": "7.6.2"
                },
                "description": "",
                "id": "29a2254e-947f-4463-b65a-5f0b17515fae",
                "clusterId": "37cb1075-c38e-4cd8-81df-442d52df3786",
                "clusterName": "Es-xfx",
                "name": "snapshot-001",
                "status": "COMPLETED",
                "updated": "2021-11-22T13:00:00",
                "backupType": "1",
                "backupMethod": "manual",
                "backupExpectedStartTime": null,
                "backupKeepDay": null,
                "backupPeriod": null,
                "indices": ".kibana",
                "totalShards": 1,
                "failedShards": 0,
                "version": "7.6.2",
                "restoreStatus": "none",
                "startTime": 1520350957275,
                "endTime": 1520351284357,
                "bucketName": "obs-b8ed"
            }
        ]
    }
]
'''

EXAMPLES = '''
# Query CSS Snapshots
- opentelekomcloud.cloud.css_snapshot_info:
    cluster: 'test-cluster'
    snapshot: 'test-snapshot'
  register: result
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CssSnapshotInfoModule(OTCModule):

    argument_spec = dict(
        cluster=dict(required=False),
        name=dict(required=False)
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        data = []

        if self.params['cluster']:
            cluster = self.conn.css.find_cluster(
                self.params['cluster'], ignore_missing=False
            )
        else:
            self.fail(changed=False, msg='CSS cluster is missing')

        if self.params['name']:
            # search snapshot by name or id
            raw = self.conn.css.find_snapshot(
                cluster, self.params['name'], ignore_missing=True
            )
            if raw:
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        else:
            for raw in self.conn.css.snapshots(cluster):
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit_json(
            changed=False,
            css_snapshots=data
        )


def main():
    module = CssSnapshotInfoModule()
    module()


if __name__ == '__main__':
    main()
