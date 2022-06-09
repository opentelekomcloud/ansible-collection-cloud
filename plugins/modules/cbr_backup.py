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
module: cbr_backup
short_description: Manage CBR backup resource
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Polina Gubina (@Polina-Gubina)"
description:
    - Manage CBR backup resource from the OTC.
options:
  backup_id:
    description:
      - Backup id.
    type: str
    required: true
  mappings:
    description: 
        - Restored mapping relationship. This parameter is mandatory for\
        VM restoration and optional for disk restoration.
    type: list
    elements: dict
    suboptions:
        backup_id:
            description:
              - backup_id
            type: str
            required: true
          volume_id:
            description:
              - ID of the disk to which data is restored.
            type: str
            required: true
  power_on:
    description: 
        - Whether the server is powered on after restoration.\
        By default it is powered on after restoration.
    type: bool
    default: true
  server_id:
    description:
     - ID of the target VM to be restored.\
     This parameter is mandatory for VM restoration.
    type: str
  volume_id:
    description: 
        - ID of the target disk to be restored.\ 
        This parameter is mandatory for disk restoration.
    type: str
  state:
    description:
      - Whether resource should be present or absent.
    choices: [present, absent]
    type: str
    default: "present"
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
backup:
  description: CBR backups list.
  type: complex
  returned: On Success.
  contains:
    checkpoint_id:
      description: Restore point ID.
      type: str
      sample: "MyZone123"
    created_at:
      description: Creation time.
      type: str
      sample: "mail@mail.com"
    description:
      description: Backup description.
      type: str
      sample: "fe80804323f2065d0175980e81617c10"
    expired_at:
      description: Expiration time.
      type: str
      sample: "test.test2."
    extend_info:
      description: Extended information.
      type: str
    id:
      description: Backup id.
      type: str
      sample: ""
    image_type:
      description: Backup type.
      type: str
      sample: 300
    name:
      description: Backup name.
      type: str
      sample: "private"
    parent_id:
      description: Parent backup ID.
      type: str
      sample: 300
    project_id:
      description: Project ID.
      type: str
      sample: "private"
    protected_at:
      description: Backup time.
      type: str
      sample: "private"
    resource_az:
      description: Resource availability zone.
      type: str
      sample: 300
    resource_id:
      description: Resource ID.
      type: str
      sample: "private"
    resource_name:
      description: Resource name.
      type: str
      sample: 300
    resource_size:
      description: Resource size, in GB.
      type: str
      sample: "private"
    resource_type:
      description: Resource type.
      type: str
      sample: 300
    status:
      description: Backup status.
      type: str
      sample: "private"
    updated_at:
      description: Update time.
      type: str
      sample: 300
    vault_id:
      description: Vault id.
      type: str
      sample: "private"
    provider_id:
      description: Backup provider ID, which is used to distinguish\
       backup objects. The value can be as follows:.
      type: str
      sample: "private"
'''

EXAMPLES = '''
# Restore backup:
- name: 
  opentelekomcloud.cloud.cbr_backup:

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CBRBackupModule(OTCModule):
    argument_spec = dict(
        backup_id=dict(required=False),
        mappings=dict(type='list', required=False, elements='dict',
                      options=dict(backup_id=dict(type='str', required=True),
                                   volume_id=dict(type='str', required=True))),
        power_on=dict(type='bool', default='true', required=False),
        server_id=dict(type='str', required=False),
        volume_id=dict(type='str', required=False),
        state=dict(type='str',
                    choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def _parse_mappings(self):
        mappings = self.params['mappings']
        parsed_mappings = []
        for m in mappings:
            mapping = {}
            mapping['backup_id'] = m.get('backup_id')\
                if m.get('backup_id') else self.fail_json(msg="'backup_id' is required for 'mappings'")
            mapping['volume_id'] = m.get('volume_id')\
                if m.get('volume_id') else self.fail_json(msg="'volume_id' is required for 'mappings'")
            parsed_mappings.append(mapping)
        return parsed_mappings

    def run(self):
        changed = False
        attrs = {}
        query = {'backup': self.params['backup_id']}

        if self.params['state'] == 'absent':
            self.conn.cbr.delete_backup(backup=self.params['backup_id'])
            self.exit(
                changed=True
            )
        if self.params['mappings']:
            query['mappings'] = self._parse_mappings()
        if self.params['power_on']:
            query['power_on'] = self.params['power_on']
        if self.params['server_id']:
            query['server_id'] = self.params['server_id']
        if self.params['volume_id']:
            query['volume_id'] = self.params['volume_id']

        self.conn.cbr.restore_data(**query)

        self.exit(
            changed=True
        )


def main():
    module =CBRBackupModule()
    module()


if __name__ == '__main__':
    main()
