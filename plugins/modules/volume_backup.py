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
module: volume_backup
short_description: Add/Delete Volume backup
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Artem Goncharov (@gtema)"
description:
  - Add or Remove Volume Backup in OTC.
options:
  display_name:
    description:
      - Name that has to be given to the backup
    required: true
    type: str
    aliases: ['name']
  display_description:
    description:
      - String describing the backup
    required: false
    type: str
    aliases: ['description']
  state:
    description:
      - Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
  volume:
    description:
      - Name or ID of the volume
      - Required when state = present
    type: str
  snapshot:
    description: Name or ID of the Snapshot to take backup of
    type: str
  force:
    description:
      - Indicates whether to backup, even if the volume is attached.
    type: bool
    default: False
  metadata:
    description: Metadata for the backup
    type: dict
  incremental:
    description: The backup mode
    type: bool
    default: False
  wait:
    description:
      - If the module should wait for the cluster to be created or deleted.
    type: bool
    default: 'yes'
  timeout:
    description:
      - The amount of time the module should wait.
    default: 180
    type: int
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
id:
    description: The Volume backup ID.
    returned: On success when C(state=present)
    type: str
    sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
backup:
    description: Dictionary describing the Cluster.
    returned: On success when C(state=present)
    type: complex
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        name:
            description: Name given to the load balancer.
            type: str
            sample: "elb_test"
'''

EXAMPLES = '''

# Add volume backup
- opentelekomcloud.cloud.volume_backup:
    name: "test_vbs_backup"
    description: "my test backup"
    state: present
    volume: ecs-7b0
    force: True
    incremental: True
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VolumeBackupModule(OTCModule):
    argument_spec = dict(
        display_name=dict(required=True, aliases=['name']),
        display_description=dict(default=None, aliases=['description']),
        volume=dict(),
        snapshot=dict(default=None),
        state=dict(default='present', choices=['absent', 'present']),
        force=dict(default=False, type='bool'),
        metadata=dict(default=None, type='dict'),
        incremental=dict(default=False, type='bool'),
        wait=dict(type='bool', default=True),
        timeout=dict(type='int', default=180)
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present',
             ['volume'])
        ],
        supports_check_mode=True
    )

    def _system_state_change(self, obj):
        state = self.params['state']
        if state == 'present':
            if not object:
                return True
        elif state == 'absent' and obj:
            return True
        return False

    def find_backup(self, backup):
        res = None
        try:
            res = self.conn.block_storage.get_backup(backup)
        except self.sdk.exceptions.ResourceNotFound:
            pass
        if not res:
            objs = list(self.conn.block_storage.backups(
                name=backup))
            if len(objs) == 1:
                res = objs[0]
            elif len(objs) > 1:
                self.fail_json(msg='More than one backup with name %s '
                               'found' % backup)
        return res

    def find_volume(self, volume):
        res = None
        try:
            res = self.conn.block_storage.get_volume(volume)
        except self.sdk.exceptions.ResourceNotFound:
            pass
        if not res:
            objs = list(self.conn.block_storage.volumes(
                details=False, name=volume))
            if len(objs) == 1:
                res = objs[0]
            elif len(objs) > 1:
                self.fail_json(msg='More than one volume with name %s '
                               'found' % volume)
            else:
                self.fail_json(msg='No volume with name %s '
                               'can be found in cloud.' % volume)
        return res

    def find_snapshot(self, snapshot):
        res = None
        try:
            res = self.conn.block_storage.get_snapshot(snapshot)
        except self.sdk.exceptions.ResourceNotFound:
            pass
        if not res:
            objs = list(self.conn.block_storage.snapshots(
                details=False, name=snapshot))
            if len(objs) == 1:
                res = objs[0]
            elif len(objs) > 1:
                self.fail_json(msg='More than one snapshot with name %s '
                               'found' % snapshot)
            else:
                self.fail_json(msg='No snapshot with name %s '
                               'can be found in cloud.' % snapshot)
        return res

    def run(self):
        name = self.params['display_name']
        description = self.params['display_description']
        volume = self.params['volume']
        snapshot = self.params['snapshot']
        force = self.params['force']
        is_incremental = self.params['incremental']
        metadata = self.params['metadata']
        timeout = self.params['timeout']

        changed = False
        backup = None

        # Currently no "find_backup" method is present in SDK,
        # so search this was
        backup = self.find_backup(name)

        if self.ansible.check_mode:
            self.exit_json(changed=self._system_state_change(backup))

        if self.params['state'] == 'present':
            if not backup:
                cloud_volume = self.find_volume(volume)
                cloud_snapshot_id = None

                attrs = {
                    'name': name,
                    'volume_id': cloud_volume.id,
                    'force': force,
                    'is_incremental': is_incremental
                }

                if snapshot:
                    cloud_snapshot_id = self.find_snapshot(snapshot,
                                                           ignore_missing=False).id
                    attrs['snapshot_id'] = cloud_snapshot_id

                if metadata:
                    attrs['metadata'] = metadata

                if description:
                    attrs['description'] = description

                backup = self.conn.block_storage.create_backup(**attrs)
                changed = True

                if not self.params['wait']:
                    self.exit_json(
                        changed=changed,
                        volume_backup=backup.to_dict(),
                        id=backup.id
                    )
                else:
                    try:
                        backup = self.conn.block_storage.wait_for_status(
                            backup,
                            status='available',
                            wait=timeout)
                        self.exit_json(
                            changed=True,
                            volume_backup=backup.to_dict(),
                            id=backup.id
                        )
                    except self.sdk.exceptions.ResourceTimeout:
                        self.fail_json(
                            msg='Timeout failure waiting for backup '
                                'to complete'
                        )

            else:
                # Decide whether update is required
                pass

            self.exit_json(
                changed=changed,
                volume_backup=backup.to_dict(),
                id=backup.id
            )

        elif self.params['state'] == 'absent':
            changed = False

            if backup:
                self.conn.block_storage.delete_backup(backup)
                if self.params['wait']:
                    try:
                        self.conn.block_storage.wait_for_delete(
                            backup,
                            interval=2,
                            wait=timeout)
                    except self.sdk.exceptions.ResourceTimeout:
                        self.fail_json(
                            msg='Timeout failure waiting for backup '
                                'to be deleted'
                        )

            self.exit_json(changed=changed)


def main():
    module = VolumeBackupModule()
    module()


if __name__ == '__main__':
    main()
