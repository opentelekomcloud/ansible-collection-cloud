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
module: rds_backup
short_description: Manage RDS backup
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Irina Pereiaslavskaia (@irina-pereiaslavskaia)"
description:
  - Manage RDS backups
options:
  instance:
    description: Name or ID of RDS instance.
    required: true
    type: str
  backup_name:
    description:
      - Name of RDS backup name must be start with letter.
      - Name must be 4 to 64 characters in length.
      - The backup name must be unique.
    required: true
    type: str
    aliases: ['name']
  backup_description:
    description:
      - Backup description contains a maximum of 256 characters.
      - Backup description can't contain symbols: >!<"&'= .
    type: str
    aliases: ['description']
  state:
    description: Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
  wait:
    description:
      - If the module should wait for the RDS backup to be created or deleted.
    type: bool
    default: 'yes'
  timeout:
    description:
      - The amount of time the module should wait.
    default: 200
    type: int
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
backup:
    description: Dictionary describing RDS backup.
    type: complex
    returned: On Success when C(state=present)
    contains:
      id:
        description: Indicates the backup ID.
        type: str
        sample: "2f4ddb93-b901-4b08-93d8-1d2e472f30fe"
      instance_id:
        description: Indicates the DB instance ID.
        type: str
        sample: "d8e6ca5a624745bcb546a227aa3ae1cfin01"
      name:
        description: Indicates the backup name.
        type: str
        sample: "backup_test"
      description:
        description: Indicates the backup description.
        type: str
        sample: "This is a description"
      begin_time:
        description: Indicates the backup start time in the "yyyy-mm-ddThh:mm:ssZ" format.
        type: str
        sample: "2020-09-12T01:17:05"
      status:
        description: Indicates the backup status.
        type: str
        sample: "COMPLETED"
      type:
        description: Indicates the backup type.
        type: str
        sample: "manual"
'''

EXAMPLES = '''
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class RdsBackupModule(OTCModule):
    argument_spec = dict(
        instance=dict(type='str'),
        name=dict(type='str'),
        description=dict(type='str'),
        state = dict(type = 'str',
                     choices = ['present', 'absent'],
                     default = 'present'),
        wait=dict(type='bool', default=True),
        timeout=dict(type='int', default=200)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    otce_min_version = '0.7.1'

    def _system_state_change(self, obj):
        state = self.params['state']
        if state == 'present':
            if not obj:
                return True
        elif state == 'absent' and obj:
            return True
        return False

    def _wait_for_delete(self, backup, instance, interval, wait):
        """Wait for backup to be deleted"""
        orig_backup = backup
        for count in self.sdk.utils.iterate_timeout(
                timeout=wait,
                message="Timeout waiting for backup to delete",
                wait=interval):
            backup = self.conn.rds.find_backup(name_or_id=backup.name,
                                               instance=instance)
            if backup.status.lower() == 'deleting':
                return orig_backup
            if backup is None:
                return backup

    def run(self):
        name = self.params['name']
        backup_description = self.params['description']
        timeout = self.params['timeout']
        attrs = {}

        instance = self.conn.rds.find_instance(name_or_id=self.params['instance'])

        if instance:
            changed = False

            backup = self.conn.rds.find_backup(name_or_id=name,
                                               instance=instance)

            if self.ansible.check_mode:
                self.exit(changed=self._system_state_change(backup))

            if self.params['state'] == 'present':

                if not backup:

                    attrs['name'] = name
                    if backup_description:
                        attrs['description'] = backup_description

                    backup = self.conn.rds.create_backup(instance, **attrs)
                    changed = True

                    if not self.params['wait']:
                        self.exit(changed=changed,
                                  backup=backup.to_dict(),
                                  id=backup.id)
                    else:
                        try:
                            backup = self.conn.rds.wait_for_backup(backup,
                                                                   wait=timeout)
                            self.exit(changed=changed,
                                      backup=backup.to_dict(),
                                      id=backup.id)
                        except self.sdk.exceptions.ResourceTimeout:
                            self.fail(msg='Timeout failure waiting for backup '
                                          'with name %s to complete' % name)

                else:
                    changed = False
                    self.exit(changed=changed,
                              msg = 'RDS backup with name %s '
                                    'already exists' % name)

            elif self.params['state'] == 'absent':

                if backup:
                    self.conn.rds.delete_backup(backup)
                    changed = True

                    if not self.params['wait']:
                        self.exit(changed=changed)

                    else:
                        try:
                            self._wait_for_delete(
                                backup=backup,
                                instance=instance,
                                interval=10,
                                wait=timeout
                            )
                        except self.sdk.exceptions.ResourceTimeout:
                            self.fail(msg='Timeout failure waiting for backup '
                                          'with name %s to be deleted' % name)
                        self.exit(changed=changed,
                                  msg='RDS backup with name %s was deleted' % name)

                else:
                    changed = False
                    self.exit(changed=changed,
                              msg='RDS backup with name %s not exists' % name)
        else:
            self.exit(msg='RDS instance %s is not exist' % instance)


def main():
    module = RdsBackupModule()
    module()


if __name__ == "__main__":
    main()