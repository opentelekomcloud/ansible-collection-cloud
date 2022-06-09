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
version_added: "0.1.2"
author: "Gubina Polina (@Polina-Gubina)"
description:
    - Get cbr backup resource list.
options:
  backup_id:
    description:
      - Backup id.
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
  name:
    description:
      - Backup name.
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
    type: str
    choices: ['OS::Cinder::Volume', 'OS::Nova::Server']
  sort:
    description:
      - A group of properties separated by commas (,)\
       and sorting directions. The value format is [:],[:],\
       where the value of direction is asc (in ascending order)\
       or desc (in descending order). If the parameter direction is\
       not specified, the default sorting direction is desc. The value of\
       sort contains a maximum of 255 characters. The value range of key is\
       as follows: [created_at, updated_at, name, status, protected_at, id].
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
  vault_id:
    description:
      - Vault id.
    type: str
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
# Getting one cbr backup by id:
- name: Testing
  opentelekomcloud.cloud.dns_zone:
    name: "test.com."
    state: present
    zone_type: private
    router: 79c32783-e560-4e3a-95b1-5a0756441e12
    description: test2
    ttl: 5000
    email: mail2@mail2.test
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CBRBackupsModule(OTCModule):
    argument_spec = dict(
        backup_id=dict(required=False),
        checkpoint_id=dict(required=False),
        dec=dict(required=False, type='bool'),
        end_time=dict(required=False),
        image_type=dict(type='str', choices=['backup', 'replication']),
        limit=dict(required=False, type='int'),
        marker=dict(type='str'),
        member_status=dict(required=False,
                           type='str', choices=['pending', 'accept', 'reject']),
        name=dict(required=False, type='str'),
        offset=dict(required=False, type='int'),
        own_type=dict(required=False, type='str',
                      choices=['all_granted', 'private', 'shared'],
                      default='private'),
        parent_id=dict(required=False, type='str'),
        resource_az=dict(required=False, type='str'),
        resource_id=dict(required=False, type='str'),
        resource_name=dict(required=False, type='str'),
        resource_type=dict(required=False, type='int',
                           choices=['OS::Cinder::Volume', 'OS::Nova::Server']),
        sort=dict(required=False, type='str'),
        start_time=dict(required=False, type='str'),
        status=dict(required=False, type='str', choices=['available',
                    'protecting', 'deleting', 'restoring', 'error',
                    'waiting_protect', 'waiting_delete', 'waiting_restore']),
        used_percent=dict(required=False, type='str'),
        vault_id=dict(required=False, type='str')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        data = []
        query = {}
        backup = None

        if self.params['backup_id']:
            backup = self.conn.cbr.find_backup(
                name_or_id=self.params['backup_id'])
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
        if self.params['vault_id']:
            query['vault_id'] = self.params['vault_id']

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
