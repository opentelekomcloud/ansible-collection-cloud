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
module: cbr_backup_info
short_description: Get cbr backup resource list
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.12.4"
author: "Gubina Polina (@Polina-Gubina)"
description:
    - Get cbr backup resource list.
options:
  name:
    description:
      - Backup name or id.
    type: str
  checkpoint_id:
    description:
      - Restore point ID.
    type: str
  dec:
    description:
      - Dedicated cloud.
    type: bool
  end_time:
    description:
      - Time when the backup ends, in %YYYY-%mm-%ddT%HH:%MM:%SSZ format.
    type: str
  image_type:
    description:
      - Backup type.
    choices: ['backup', 'replication']
    type: str
  limit:
    description:
      - Number of records displayed per page.\
      The value must be a positive integer.
    type: int
  marker:
    description:
      - ID of the last record displayed on the previous page.
    type: str
  member_status:
    description:
      - Backup sharing status.
    choices: ['pending', 'accept', 'reject']
    type: str
  offset:
    description:
      - Offset value. The value must be a positive integer.
    type: int
  own_type:
    description:
      - Owning type of a backup. private backups are queried by default.
    type: str
    default: 'private'
    choices: ['all_granted', 'private', 'shared']
  parent_id:
    description:
      - Parent backup id.
    type: str
  resource_az:
    description:
      - AZ-based filtering is supported.
    type: str
  resource_id:
    description:
      - Resource id.
    type: str
  resource_name:
    description:
      - Resource name.
    type: str
  resource_type:
    description:
      - Resource type.
    choices: ['OS::Cinder::Volume', 'OS::Nova::Server']
    type: str
  sort:
    description:
      - A group of properties separated by commas (,) and sorting directions.
    type: str
  start_time:
    description:
      - Time when the backup starts, in %YYYY-%mm-%ddT%HH:%MM:%SSZ format.\
      For example, 2018-02-01T12:00:00Z.
    type: str
  status:
    description:
      - Status. When the API is called, multiple statuses can be transferred\
      for filtering, for example, status=available&status=error.
    type: str
    choices: ['available', 'protecting', 'deleting', 'restoring', 'error',\
    'waiting_protect', 'waiting_delete', 'waiting_restore']
  used_percent:
    description:
      - Backups are filtered based on the occupied vault capacity. The value\
      ranges from 1 to 100. For example, if used_percent is set to 80,\
      all backups who occupied 80% or more of the vault capacity are displayed.
    type: str
  vault:
    description:
      - Vault id or name.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
backups:
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
        auto_trigger:
          description:
            - Whether the backup is automatically generated.
          type: bool
        bootable:
          description:
            - Whether the backup is a system disk backup.
          type: bool
        incremental:
          description:
            - Whether the backup is an incremental backup.
          type: bool
        snapshot_id:
          description:
            - Snapshot ID of the disk backup.
          type: str
        support_lld:
          description:
            - Whether to allow lazyloading for fast restoration.
          type: bool
        supported_restore_mode:
          description:
            - Restoration mode. Possible values are na,\
            snapshot, and backup. snapshot indicates the backup\
            can be used to create a full-server image. backup\
            indicates the data is restored from backups of the EVS\
            disks of the server. na indicates the backup cannot be\
            used for restoration.
          type: str
        os_images_data:
          description:
            - ID list of images created using backups.
          type: list
          elements: dict
          contains:
            image_id:
              description:
                - Image ID.
              type: str
        contain_system_disk:
          description:
            - Whether the VM backup data contains system disk data.
          type: bool
        encrypted:
          description:
            - Whether the backup is encrypted.
          type: bool
        system_disk:
          description:
            - Whether the disk is a system disk.
          type: bool
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
# Getting one cbr backup:
- opentelekomcloud.cloud.cbr_backup_info:
    name: "name-or-id"

# Getting cbr backups list for vault:
- opentelekomcloud.cloud.cbr_backup_info:
    vault: "name-or-id-vault"
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CBRBackupsModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
        checkpoint_id=dict(required=False),
        dec=dict(required=False, type='bool'),
        end_time=dict(required=False),
        image_type=dict(type='str', choices=['backup', 'replication']),
        limit=dict(required=False, type='int'),
        marker=dict(type='str'),
        member_status=dict(required=False,
                           type='str', choices=['pending', 'accept', 'reject']),
        offset=dict(required=False, type='int'),
        own_type=dict(required=False, type='str',
                      choices=['all_granted', 'private', 'shared'],
                      default='private'),
        parent_id=dict(required=False, type='str'),
        resource_az=dict(required=False, type='str'),
        resource_id=dict(required=False, type='str'),
        resource_name=dict(required=False, type='str'),
        resource_type=dict(required=False, type='str',
                           choices=['OS::Cinder::Volume', 'OS::Nova::Server']),
        sort=dict(required=False, type='str'),
        start_time=dict(required=False, type='str'),
        status=dict(required=False, type='str',
                    choices=['available', 'protecting', 'deleting',
                             'restoring', 'error', 'waiting_protect',
                             'waiting_delete', 'waiting_restore']),
        used_percent=dict(required=False, type='str'),
        vault=dict(required=False, type='str')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        data = []
        query = {}
        backup = None

        if self.params['name']:
            backup = self.conn.cbr.find_backup(
                name_or_id=self.params['name'])
            self.exit(
                changed=False,
                backup=backup
            )
        if self.params['checkpoint_id']:
            query['checkpoint_id'] = self.params['checkpoint_id']
        if self.params['dec']:
            query['dec'] = self.params['dec']
        if self.params['end_time']:
            query['end_time'] = self.params['end_time']
        if self.params['image_type']:
            query['image_type'] = self.params['image_type']
        if self.params['limit']:
            query['limit'] = self.params['limit']
        if self.params['marker']:
            query['marker'] = self.params['marker']
        if self.params['member_status']:
            query['member_status'] = self.params['member_status']
        if self.params['name']:
            query['name'] = self.params['name']
        if self.params['offset']:
            query['offset'] = self.params['offset']
        if self.params['own_type']:
            query['own_type'] = self.params['own_type']
        if self.params['parent_id']:
            query['parent_id'] = self.params['parent_id']
        if self.params['resource_az']:
            query['resource_az'] = self.params['resource_az']
        if self.params['resource_id']:
            query['resource_id'] = self.params['resource_id']
        if self.params['resource_name']:
            query['resource_name'] = self.params['resource_name']
        if self.params['resource_type']:
            query['resource_type'] = self.params['resource_type']
        if self.params['sort']:
            query['sort'] = self.params['sort']
        if self.params['start_time']:
            query['start_time'] = self.params['start_time']
        if self.params['status']:
            query['status'] = self.params['status']
        if self.params['used_percent']:
            query['used_percent'] = self.params['used_percent']
        if self.params['vault']:
            vault = self.conn.cbr.find_vault(name_or_id=self.params['vault'])
            if not vault:
                self.fail_json(msg="Vault not found")
            query['vault_id'] = vault.id

        for raw in self.conn.cbr.backups(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            backups=data
        )


def main():
    module = CBRBackupsModule()
    module()


if __name__ == '__main__':
    main()
