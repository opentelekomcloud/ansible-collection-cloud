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
# limitations under the Licens.

DOCUMENTATION = '''
---
module: dds_instance
short_description: Manage DDS instance
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.2"
author: "Yustina Kvrivishvili (@YustinaKvr)"
description:
  - Manage DDS instances.
options:
  name:
    description: 
        - Specifies the DB instance name.
        - The DB instance name of the same DB engine is unique for the same tenant.
        - The value must be 4 to 64 characters in length and start with a letter.
        - It is case-sensitive and can contain only letters, digits, hyphens, and underscores.
    type: str
    required: true
  datastore_version:
    description: Specifies the database version.
    choices: [3.2, 3.4]
    type: str
    default: '3.4'
  region:
    description:
        - Specifies the region ID.
        - The value cannot be empty.
    type: str
    required: true
  availability_zone:
    description:
        - Specifies the AZ ID.
        - The value cannot be empty.
    type: int
    required: true
  vpc_id:
    description:
        - Specifies the VPC ID. The value cannot be empty.
        - The string length and whether the string complying with UUID regex rules are verified.
    type: str
    required: true
  subnet_id:
    description: Specifies the subnet ID.
    type: str
    required: true
  security_group:
    description: Specifies the ID of the security group where a specified DB instance belongs to.
    type: str
    required: true
  password:
    description:
        - Specifies the database password. The value must be 8 to 32 characters in length, 
        - contain uppercase and lowercase letters, digits and special characters.
    required: true
  disk_encryption:
    description:
        - Specifies the key ID used for disk encryption.
        - The string must comply with UUID regular expression rules.
        - If this parameter is not transferred, disk encryption is not performed.
    type: str
  mode:
    description:
        - Specifies the instance type. Cluster, replica set instances are supported.
    choices: [sharding, replicaset]
    type: str
    required: true
  flavor_type:
    description:
        - Specifies the node type. For a replica set instance, the value is replica.
        - For a cluster instance, the value can be mongos, shard, or config
    choices: [mongos, shard, config, replica]
    type: str
    required: true
  flavor_num:
    description: Specifies node quantity.
    type: int
    required: true
  flavor_storage:
    description:
        - Specifies the disk type. This parameter is optional for all nodes except mongos. 
        - This parameter is invalid for the mongos nodes.
    type: str
    default: 'ULTRAHIGH'
  backup_timeframe:
    description:
        - Specifies the backup time window.
        - Automated backups will be triggered during the backup time window. Value cannot be empty.
    type: str
    required: true
  backup_keepdays:
    description:
        - Specifies the number of days to retain the generated backup files.
        - The value range is from 0 to 732.
    type: int
  ssl_option:
    description:
        - Specifies whether to enable SSL. The value 0 indicates that SSL is disabled, 1 - enabled.
        - If this parameter is not transferred, SSL is enabled by default.
    type: str


requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
dds_instance:
    description: List of dictionaries describing DDS Instance.
    type: complex
    returned: On Success.
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        name:
            description: Name (version) of the instance.
            type: str
            sample: "test"
'''

EXAMPLES = '''
- name: provision rds instance
  opentelekomcloud.cloud.dds_instance:
    name: "{{ instance_name }}"
    datastore_type: "mysql"
    datastore_version: "8.0"
    flavor: "{{ rds_flavor }}"
    router: "{{ router_name }}"
    network: "{{ network_name }}"
    security_group: "default"
    volume_type: "common"
    volume_size: 100
    password: "Test@123"
    region: "eu-de"
    availability_zone: "eu-de-01"
    timeout: 600

'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DdsInstanceModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True, type='str'),
        datastore_version=dict(type='str', choices=['3.2', '3.4'], default='3.4'),
        region=dict(required=True, type='str'),
        availability_zone=dict(required=True, type='str'),
        vpc_id=dict(required=True, type='str'),
        subnet_id=dict(required=True, type='str'),
        security_group=dict(required=True, type='str'),
        password=dict(required=True, type='str', no_log=True),
        disk_encryption=dict(type='str'),
        mode=dict(required=True, type='str', choices=['sharding', 'replicaset']),
        flavor_type=dict(required=True, type='str', choices=['mongos', 'shard', 'config',
                                                             'replica']),
        flavor_num=dict(required=True, type='int'),
        flavor_storage=dict(type='str', default='ULTRAHIGH'),
        backup_timeframe=dict(required=True, type='str'),
        backup_keepdays=dict(type='int'),
        ssl_option=dict(type='int'),
    )
    module_kwargs = dict(
        required_if=[
            ('backup_keepdays', not None, ['backup_timeframe']),
            ('backup_timeframe', not None, ['backup_keepdays']),
        ],
        supports_check_mode=True
    )

    otce_min_version = '0.11.0'

    def _system_state_change(self, obj):
        state = self.params['state']
        if state == 'present':
            if not obj:
                return True
        elif state == 'absent' and obj:
            return True
        return False

    def run(self):

        name = self.params['name']

        changed = False

        instance = self.conn.dds.find_instance(
            name_or_id=name)

        if self.ansible.check_mode:
            self.exit(changed=self._system_state_change(instance))

        if self.params['state'] == 'absent':
            changed = False

            if instance:
                attrs = {
                    'instance': instance.id
                }

                self.conn.delete_dds_instance(**attrs)
                changed = True

        elif self.params['state'] == 'present':
            if instance:
                self.exit(changed=False)

            volume_type = self.params['volume_type']
            if volume_type:
                self.params['volume_type'] = volume_type.upper()

            instance = self.conn.create_rds_instance(**self.params)
            self.exit(changed=True, instance=instance.to_dict())

        self.exit(changed=changed)


def main():
    module = DdsInstanceModule()
    module()


if __name__ == "__main__":
    main()
