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
module: volume_snapshot_info
short_description: Get information about volume snapshots
extends_documentation_fragment: opentelekomcloud.cloud.otc.doc
version_added: "0.0.1"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Get a generator of snapshots info from the OTC.
options:
  details:
    description: More detailed output
    type: bool
    default: True
  name:
    description:
      - Name of the snapshot.
    type: str
  volume:
    description:
      - Name or ID of the volume.
    type: str
  status:
    description:
      - Specifies the snapshot status.
        choices: ['creating', 'available', 'error', 'deleting',
        'error_deleting', 'rollbacking', 'backing-up']
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
volume_snapshots:
    description: List of dictionaries describing volume snapshots.
    type: complex
    returned: On Success.
    contains:
        created_at:
            description: Specifies the time when the snapshot was created.
            type: str
            sample: "2016-02-16T16:54:14.981520"
        description:
            description: Specifies the snapshot description.
            type: str
            sample: "test description"
        id:
            description: Specifies the snapshot ID.
            type: str
            sample: "b836dc3d-4e10-4ea4-a34c-8f6b0460a583"
        metadata:
            description: Specifies the snapshot metadata.
            type: dict
        name:
            description: Specifies the snapshot name.
            type: str
            sample: "test01"
        size:
            description: Specifies the snapshot size, in GB.
            type: int
            sample: 1
        status:
            description: Specifies the snapshot status. For details.
            type: str
            sample: "available"
        volume_id:
            description: Specifies the ID of the snapshot's source disk.
            type: str
            sample: "ba5730ea-8621-4ae8-b702-ff0ffc12c209"
'''

EXAMPLES = '''
# Get configs versions.
- volume_snapshot_info:
    name: my_snapshot
    status: available
  register: data
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VolumeSnapshotInfoModule(OTCModule):
    argument_spec = dict(
        details=dict(default=True, type='bool'),
        name=dict(required=False),
        volume=dict(required=False),
        status=dict(required=False, choices=['creating', 'available', 'error',
                                             'deleting', 'error_deleting', 'rollbacking',
                                             'backing-up']),
    )

    def run(self):

        details_filter = self.params['details']
        name_filter = self.params['name']
        volume_filter = self.params['volume']
        status_filter = self.params['status']

        data = []
        query = {}
        if name_filter:
            query['name'] = name_filter
        if volume_filter:
            query['volume_id'] = self.conn.block_storage.find_volume(volume_filter)
        if status_filter:
            query['status'] = status_filter.lower()

        for raw in self.conn.block_storage.snapshots(details_filter, **query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit_json(
            changed=False,
            volume_snapshots=data
        )


def main():
    module = VolumeSnapshotInfoModule()
    module()


if __name__ == '__main__':
    main()
