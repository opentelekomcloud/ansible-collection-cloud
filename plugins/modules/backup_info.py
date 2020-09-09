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
module: backup_info
short_description: Get Backups
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Vladimir Hasko (@vladimirhasko)"
description:
  - Get Backup info from the OTC.
options:
  name:
    description:
      - Name of the Backup.
    type: str
  volume:
    description:
      - Name of the volume.
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
        volume=dict(required=False)
    )

    def run(self):
        name_filter = self.params['name']
        volume = self.params['volume']

        data = []
        attrs = {}

        if name_filter:
            attrs['name'] = name_filter
        if volume:
            attrs['volume_id'] = self.conn.block_storage.find_volume(volume)

        for raw in self.conn.block_storage.backups(**attrs):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit_json(
            changed=False,
            backups=data
        )


def main():
    module = BackupInfoModule()
    module()


if __name__ == '__main__':
    main()
