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
short_description: Manage CBR Backup Resource
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.12.4"
author: "Gubina Polina (@Polina-Gubina)"
description: Manage CBR backup resource from the OTC.
options:
  name:
    description: Backup name of id.
    type: str
    required: true
  mappings:
    description:
        - Restored mapping relationship. This parameter is mandatory for VM restoration and optional for disk restoration.
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
    default: True
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
    default: present
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
    created_at:
      description: Creation time.
      type: str
    description:
      description: Backup description.
      type: str
    expired_at:
      description: Expiration time.
      type: str
    extend_info:
      description: Extended information.
      type: complex
      contains:
        allocated:
          description:
            - Allocated capacity, in MB.
          type: int
        charging_mode:
          description:
            - Billing mode.
          type: str
    id:
      description: Backup id.
      type: str
    image_type:
      description: Backup type.
      type: str
    name:
      description: Backup name.
      type: str
    parent_id:
      description: Parent backup ID.
      type: str
    project_id:
      description: Project ID.
      type: str
    protected_at:
      description: Backup time.
      type: str
    resource_az:
      description: Resource availability zone.
      type: str
    resource_id:
      description: Resource ID.
      type: str
    resource_name:
      description: Resource name.
      type: str
    resource_size:
      description: Resource size, in GB.
      type: str
    resource_type:
      description: Resource type.
      type: str
    status:
      description: Backup status.
      type: str
    updated_at:
      description: Update time.
      type: str
    vault_id:
      description: Vault id.
      type: str
    provider_id:
      description: Backup provider ID, which is used to distinguish\
       backup objects. The value can be as follows:.
      type: str
'''

EXAMPLES = '''
# Restore backup:
- name:
  opentelekomcloud.cloud.cbr_backup:
    name: "backup-name-or-id"
    volume_id: "volume-id"

# Delete backup:
- name:
  opentelekomcloud.cloud.cbr_backup:
    name: "backup-name-or-id"
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CBRBackupModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        mappings=dict(type='list', required=False, elements='dict',
                      options=dict(backup_id=dict(type='str', required=True),
                                   volume_id=dict(type='str', required=True))),
        power_on=dict(type='bool', default=True, required=False),
        server_id=dict(type='str', required=False),
        volume_id=dict(type='str', required=False),
        state=dict(type='str',
                   choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['name'])
        ],
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

    def _system_state_change(self, backup):
        state = self.params['state']
        if state == 'present':
            if not backup:
                return True
        elif state == 'absent' and backup:
            return True
        return False

    def run(self):
        query = {}

        if self.params['mappings']:
            query['mappings'] = self._parse_mappings()
        if self.params['power_on']:
            query['power_on'] = self.params['power_on']
        if self.params['server_id']:
            query['server_id'] = self.params['server_id']
        if self.params['volume_id']:
            query['volume_id'] = self.params['volume_id']

        backup = self.conn.cbr.find_backup(name_or_id=self.params['name'])
        query['backup'] = backup.id

        if self.ansible.check_mode:
            self.exit_json(changed=self._system_state_change(backup))

        if backup:
            if self.params['state'] == 'present':
                self.conn.cbr.restore_data(**query)
            else:
                self.conn.cbr.delete_backup(backup=backup.id)
            self.exit(
                changed=True
            )
        self.exit(
            changed=False
        )


def main():
    module = CBRBackupModule()
    module()


if __name__ == '__main__':
    main()
