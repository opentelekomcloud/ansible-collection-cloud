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
module: rds_backup_info
short_description: Get RDS Backup info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Irina Pereiaslavskaia (@irina-pereiaslavskaia)"
description:
  - Get RDS backup info from the OTC.
options:
  instance:
    description: Name or ID of the RDS instance
    required: true
    type: str
  backup:
    description: Name or ID of the RDS Backup
    required: false
    type: str
  backup_type:
    choices: [auto, manual, fragment, incremental]
    description: Backup type
    required: false
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
rds_backups:
  description: List of dictionaries describing rds backups.
  type: complex
  returned: On Success
  contains:
    id:
      description: Indicates the backup ID.
      type: str
      sample: "a11a111a111a11111bbbbb2222ccc3333302"
    name:
      description: Indicates the backup name.
      type: str
      sample: "test01"
    type:
      description: Indicates the backup type.
      type: str
      sample: "auto"
    size:
      description: Specifies the backup size in kB.
      type: int
      sample: 2803
    status:
      description: Indicates the backup status.
      type: str
      sample: "COMPLETED"
    begin_time:
      description: Indicates the backup start time in the "yyyy-mm-ddThh:mm:ssZ" format.
      type: str
      sample: "2018-08-06T12:41:14+0800"
    end_time:
      description: Indicates the backup end time.
      type: str
      sample: "2018-08-06T12:43:14+0800"
    datastore:
      description: Indicates the database version.
      type: dict
    databases:
      description: Indicates a list of self-built databases that support partial backups.
      type: list
    instance_id:
      description: Indicates the ID of the DB instance for which the backup is creates.
      type: str
      sample: "a11a111a111a11111bbbbb2222ccc3333304"
'''

EXAMPLES = '''
# Get RDS Backups (all parameters are specified, names of rds instance and backup are used)
- rds_backup_info:
    instance: "test_instance_name"
    backup: "test_backup_name"
    backup_type: "auto"
  register: rds_backup

# Get RDS Backups (all parameters are specified, IDs of rds instance and backup are used)
- rds_backup_info:
    instance: "a11a111a111a11111bbbbb2222ccc3333305"
    backup: "a11a111a111a11111bbbbb2222ccc3333307"
    backup_type: "manual"
  register: rds_backup

# Get RDS Backups (instance name and backup type are specified)
- rds_backup_info:
    instance: "test_instance_name"
    backup_type: "manual"
  register: rds_backup

# Get RDS Backups (instance id and backup name are specified)
- rds_backup_info:
    instance: "a11a111a111a11111bbbbb2222ccc3333305"
    backup: "test_backup_name"
  register: rds_backup

# Get RDS Backups (instance name is specified)
- rds_backup_info:
    instance: "test_instance_name"
  register: rds_backup
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class RdsBackupInfoModule(OTCModule):
    argument_spec = dict(
        instance=dict(type='str',
                      required=True),
        backup=dict(type='str',
                    required=False),
        backup_type=dict(type='str',
                         choices=['auto', 'manual', 'fragment', 'incremental'],
                         required=False)
    )

    def run(self):

        instance_filter = self.params['instance']
        backup_filter = self.params['backup']
        backup_type_filter = self.params['backup_type']

        data = []
        query = {}
        if instance_filter:
            instance = self.conn.rds.find_instance(name_or_id=instance_filter)
            query['instance'] = instance
            if backup_filter:
                backup = self.conn.rds.find_backup(name_or_id=backup_filter,
                                                   instance=instance)
                query['backup_id'] = backup.id
            if backup_type_filter:
                query['backup_type'] = backup_type_filter

        for raw in self.conn.rds.backups(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            rds_backups=data
        )


def main():
    module = RdsBackupInfoModule()
    module()


if __name__ == '__main__':
    main()
