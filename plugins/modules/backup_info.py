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
module: backup_info
short_description: Get Backups
extends_documentation_fragment: opentelekomcloud.cloud.otc.doc
version_added: "2.9"
author: "Vladimir Hasko (@vladimirhasko)"
description:
  - Get Backup info from the OTC.
options:
  name:
    description:
      - Name of the Backup.
    type: str
  volume_id:
    description:
      - ID of the volume to filter backup results.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
backups:
    description: List of dictionaries describing volume backups.
    type: complex
    returned: On Success.
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        name:
            description: Name (version) of the backup.
            type: str
            sample: "10.0"
'''

EXAMPLES = '''
# Get backups.
- backup_info:
  register: backup

- backup_info:
    name: my_fake_backup
  register: backup
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class BackupInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
        volume_id=dict(required=False)
    )

    def run(self):
        name_filter = self.params['name']
        volume_id_filter = self.params['volume_id']

        data = []
        # TODO: Pass filters into SDK
        for raw in conn.block_storage.backups():
            if name_filter and raw.name != name_filter:
                continue
            if (volume_id_filter
                    and raw.['volume_id'] != volume_id_filter):
                continue
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit_json(
            changed=False,
            backups=data
        )


def main():
    module = AutoScalingConfigInfoModule()
    module()


if __name__ == '__main__':
    main()
