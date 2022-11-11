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
  datastore_version:
    description: Specifies the database version.
    choices: ['3.2', '3.4']
    type: str
    default: '3.4'
  region:
    description:
      - Specifies the region ID.
      - The value cannot be empty.
    type: str
  availability_zone:
    description:
      - Specifies the AZ ID.
      - The value cannot be empty.
    type: str
  router:
    description:
      - Specifies the VPC ID. The value cannot be empty.
      - The string length and whether the string complying with UUID regex rules are verified.
    type: str
  network:
    description: Specifies the subnet ID.
    type: str
  security_group:
    description: Specifies the ID of the security group where a specified DB instance belongs to.
    type: str
  state:
    choices: [present, absent]
    default: present
    description: Instance state
    type: str
  password:
    description:
      - Specifies the database password. The value must be 8 to 32 characters in length,
      - contain uppercase and lowercase letters, digits and special characters.
    type: str
  disk_encryption:
    description:
      - Specifies the key ID used for disk encryption.
      - The string must comply with UUID regular expression rules.
      - If this parameter is not transferred, disk encryption is not performed.
    type: str
  mode:
    description:
      - Specifies the instance type. Cluster, replica set instances are supported.
    choices: [Sharding, ReplicaSet]
    type: str
  flavors:
    description:
      - Specifies the instance specifications.
    type: list
    elements: dict
    suboptions:
      type:
        description:
          - Specifies the node type. For a replica set instance, the value is replica.
          -   For a cluster instance, the value can be mongos, shard, or config
        choices: [mongos, shard, config, replica]
        type: str
      num:
        description: Specifies node quantity.
        type: int
      storage:
        description:
          - Specifies the disk type. This parameter is optional for all nodes except mongos.
          - This parameter is invalid for the mongos nodes.
        type: str
        default: 'ULTRAHIGH'
      spec_code:
          description: Specifies the resource specification code.
          type: str
      size:
        description:
          - Specifies the disk size. This parameter is mandatory for all nodes except mongos.
          - This parameter is invalid for the mongos nodes.
          - For a cluster instance, the storage space of a shard node can be 10 to 1000 GB,
          - and the config storage space is 20 GB. This parameter is invalid for mongos nodes.
          - Therefore, you do not need to specify the storage space for mongos nodes.
          - For a replica set instance, the value ranges from 10 to 2000.
        type: int
  backup_timeframe:
    description:
        - Specifies the backup time window.
        - Automated backups will be triggered during the backup time window. Value cannot be empty.
    type: str
  backup_keepdays:
    description:
      - Specifies the number of days to retain the generated backup files.
      - The value range is from 0 to 732.
    type: int
  ssl_option:
    description:
      - Specifies whether to enable SSL. The value 0 indicates that SSL is disabled, 1 - enabled.
      - If this parameter is not transferred, SSL is enabled by default.
    type: int


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
- name: Create DDS Instance
  opentelekomcloud.cloud.dds_instance:
    name: "{{ instance_name }}"
    datastore_version: "3.4"
    region: "eu-de"
    availability_zone: "eu-de-01"
    router: "{{ router_name }}"
    mode: "ReplicaSet"
    network: "{{ network_name }}"
    security_group: "default"
    password: "Test@123"
    flavors:
      - type: "replica"
        num: 1
        storage: "ULTRAHIGH"
        size: 10
        spec_code: "dds.mongodb.s2.medium.4.repset"
    backup_timeframe: "00:00-01:00"
    backup_keepdays: 7
    ssl_option: 1
    state: present
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DdsInstanceModule(OTCModule):
    argument_spec = dict(
        name=dict(type='str'),
        datastore_version=dict(type='str', choices=['3.2', '3.4'], default='3.4'),
        region=dict(type='str'),
        availability_zone=dict(type='str'),
        router=dict(type='str'),
        network=dict(type='str'),
        security_group=dict(type='str'),
        password=dict(type='str', no_log=True),
        disk_encryption=dict(type='str'),
        mode=dict(type='str', choices=['Sharding', 'ReplicaSet']),
        flavors=dict(type='list', elements='dict'),
        backup_timeframe=dict(type='str'),
        backup_keepdays=dict(type='int'),
        ssl_option=dict(type='int'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
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
        attrs = {}
        if self.params['disk_encryption']:
            attrs['disk_encryption_id'] = self.params.pop('disk_encryption')
        if self.params['name']:
            attrs['name'] = self.params['name']
        if self.params['datastore_version']:
            attrs['datastore_version'] = self.params['datastore_version']
        if self.params['region']:
            attrs['region'] = self.params['region']
        if self.params['availability_zone']:
            attrs['availability_zone'] = self.params['availability_zone']
        if self.params['router']:
            attrs['router'] = self.params['router']
        if self.params['mode']:
            attrs['mode'] = self.params['mode']
        if self.params['network']:
            attrs['network'] = self.params['network']
        if self.params['security_group']:
            attrs['security_group'] = self.params['security_group']
        if self.params['password']:
            attrs['password'] = self.params['password']
        if self.params['backup_timeframe']:
            attrs['backup_timeframe'] = self.params['backup_timeframe']
        if self.params['backup_keepdays']:
            attrs['backup_keepdays'] = self.params['backup_keepdays']
        if self.params['ssl_option']:
            attrs['ssl_option'] = self.params['ssl_option']
        if self.params['flavors']:
            attrs['flavors'] = self.params['flavors']

        changed = False

        instance = self.conn.dds.find_instance(
            name_or_id=attrs['name'])

        if self.ansible.check_mode:
            self.exit(changed=self._system_state_change(instance))

        if self.params['state'] == 'absent':
            changed = False

            if instance:
                attrs = {
                    'instance': instance.id
                }
                if self.params['wait']:
                    attrs['wait'] = True

                self.conn.delete_dds_instance(**attrs)
                changed = True

        elif self.params['state'] == 'present':
            if not instance:
                instance = self.conn.create_dds_instance(**attrs)
                self.exit(changed=True, instance=instance.to_dict())

        self.exit(changed=changed)


def main():
    module = DdsInstanceModule()
    module()


if __name__ == "__main__":
    main()
