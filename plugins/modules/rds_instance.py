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
module: rds_instance
short_description: Manage RDS instance
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.2"
author: "Artem Goncharov (@gtema)"
description:
  - Manage RDS instances.
options:
  availability_zone:
    description:
        - Instance availability zone.
        - Can be a CSV list (i.e. eu-de-01,eu-de-02)
        - Mandatory for creating instance
    type: str
  backup_keepdays:
    description:
        - Retention days for the backup files
        - Must be specified together with backup_timeframe
    type: int
  backup_timeframe:
    description:
        - Backup time window in HH:MM-HH:MM format UTC time
        - Must be specified together with backup_keepdays
    type: str
  configuration:
    description: Parameter template
    type: str
  datastore_type:
    choices: [mysql, postgresql, sqlserver]
    description: Datastore type
    default: postgresql
    type: str
  datastore_version:
    description: Datastore version
    type: str
  disk_encryption:
    description: KMS ID
    type: str
  flavor:
    description:
        - Instance specification code
        - Mandatory for new instance
    type: str
  ha_mode:
    choices: [async, semisync, sync]
    description: Replication mode for the HA type
    type: str
  name:
    description: Instance name or ID
    type: str
    required: true
  network:
    description: Name or ID of the neutron network
    type: str
  password:
    description: Database password
    type: str
  port:
    description: Database port
    type: int
  region:
    choices: [eu-de]
    default: eu-de
    description: Database region
    type: str
  replica_of:
    description: Instance ID to create the replica of
    type: str
  router:
    description: Name or ID of the Neutron router (VPC)
    type: str
  security_group:
    description: Name or ID of the security group
    type: str
  state:
    choices: [present, absent]
    default: present
    description: Instance state
    type: str
  volume_type:
    description: |
      - Type of the volume
      - Supported values: common, ultrahigh
      - Mandatory for new instance
    type: str
  volume_size:
    description:
        - Size of the volume
        - Mandatory for new instance
    type: int
  wait:
     description:
        - If the module should wait for the instance to be created.
     type: bool
     default: 'yes'
  timeout:
    description:
      - The amount of time the module should wait for the instance to get
        into active state.
    default: 600
    type: int


requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
rds_instance:
    description: List of dictionaries describing RDS Instance.
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
  opentelekomcloud.cloud.rds_instance:
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


class RdsInstanceModule(OTCModule):
    argument_spec = dict(
        availability_zone=dict(type='str'),
        backup_keepdays=dict(type='int'),
        backup_timeframe=dict(type='str'),
        configuration=dict(type='str'),
        datastore_type=dict(type='str', default='postgresql',
                            choices=['postgresql', 'mysql', 'sqlserver']),
        datastore_version=dict(type='str'),
        disk_encryption=dict(type='str'),
        flavor=dict(type='str'),
        ha_mode=dict(type='str', choices=['async', 'semisync', 'sync']),
        name=dict(required=True, type='str'),
        network=dict(type='str'),
        password=dict(type='str', no_log=True),
        port=dict(type='int'),
        region=dict(type='str', choices=['eu-de'], default='eu-de'),
        replica_of=dict(type='str'),
        router=dict(type='str'),
        security_group=dict(type='str'),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        volume_type=dict(type='str'),
        volume_size=dict(type='int'),
        wait=dict(type='bool', default=True),
        timeout=dict(type='int', default=600)
    )
    module_kwargs = dict(
        required_if=[
            ('backup_keepdays', not None, ['backup_timeframe']),
            ('backup_timeframe', not None, ['backup_keepdays']),
            ('replica_of', None, [
                'datastore_type', 'datastore_version',
                'network', 'router', 'security_group',
                'password', 'region'
            ])
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
        if self.params['wait']:
            self.params['wait_timeout'] = self.params.pop('timeout')
        else:
            self.params.pop('timeout')
        name = self.params['name']

        changed = False

        instance = self.conn.rds.find_instance(
            name_or_id=name)

        if self.ansible.check_mode:
            self.exit(changed=self._system_state_change(instance))

        if self.params['state'] == 'absent':
            changed = False

            if instance:
                attrs = {
                    'instance': instance.id,
                    'wait': self.params['wait']
                }

                self.conn.delete_rds_instance(**attrs)
                changed = True

        elif self.params['state'] == 'present':
            # Attention: not conform password result in BadRequest with no info

            if instance:
                self.exit(changed=False)

            volume_type = self.params['volume_type']
            if volume_type:
                self.params['volume_type'] = volume_type.upper()

            instance = self.conn.create_rds_instance(**self.params)
            self.exit(changed=True, instance=instance.to_dict())

        self.exit(changed=changed)


def main():
    module = RdsInstanceModule()
    module()


if __name__ == "__main__":
    main()
