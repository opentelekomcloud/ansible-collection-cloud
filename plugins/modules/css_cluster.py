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
module: css_cluster
short_description: Manage CSS clusters
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: 0.9.0
author: Vladimir Vshivkov (@enrrou)
description:
  - Manage CSS clusters
options:
  name:
    description:
      - Cluster name.
      - It contains 4 to 32 characters. Only letters, digits, hyphens (-), and
        underscores (_) are allowed.
      - The value must start with a letter.
    required: true
    type: str
  datastore_version:
    description:
      - Engine version. The value can be 6.2.3, 7.1.1 or 7.6.2.
      - The default value is 7.6.2.
    type: str
    choices: [7.6.2, 7.9.3]
    default: 7.6.2
  datastore_type:
    description:
      - Engine type.
      - The default value is elasticsearch. Currently, the value can only be
        elasticsearch.
    type: str
    default: elasticsearch
  instance_num:
    description:
      - Number of clusters.
      - The value range is 1 to 32.
    type: int
  flavor:
    description: Instance flavor name.
    type: str
  volume_type:
    description:
      - Information about the volume.
      - COMMON Common I/O
      - HIGH High I/O
      - ULTRAHIGH Ultra-high I/O
    type: str
    choices:
      - common
      - high
      - ultrahigh
  volume_size:
    description:
      - 'Volume size, which must be a multiple of 4 and 10.'
      - Unit GB
    type: int
  system_encrypted:
    description:
      - Value 1 indicates encryption is performed
      - Value 0 indicates encryption is not performed.
    choices:
      - '0'
      - '1'
    type: int
  system_cmkid:
    description:
      - Key ID.
      - The Default Master Keys cannot be used to create grants. Specifically,
        you cannot use Default Master Keys whose aliases end with /default in
        KMS to create clusters.
      - After a cluster is created, do not delete the key used by the cluster.
        Otherwise, the cluster will become unavailable.
    type: str
  https_enable:
    type: bool
    description:
      - Whether communication is encrypted on the cluster.
      - Available values include true and false. By default, communication is
        encrypted.
      - Value true indicates that communication is encrypted on the cluster.
      - Value false indicates that communication is not encrypted on the
        cluster.
  authority_enable:
    type: bool
    description:
      - Whether to enable authentication.
      - Available values include true and false.
      - Authentication is disabled by default.
      - 'When authentication is enabled, httpsEnable must be set to true.'
  admin_pwd:
    description:
      - Password of the cluster user admin in security mode.
      - This parameter is mandatory only when authority_enable is set to true.
      - The password can contain 8 to 32 characters.
      - Passwords must contain at least 3 of the following character types
        uppercase letters, lowercase letters, numbers, and special characters
        (~!@#$%^&*()-_=+\\|[{}];:,<.>/?).
    type: str
  router:
    description: 'VPC ID, which is used for configuring cluster network.'
    type: str
  net:
    description:
      - Subnet ID. All instances in a cluster must have the same subnets and
        security groups.
    type: str
  security_group:
    description:
      - Security group ID. All instances in a cluster must have the same subnets
        and security groups.
    type: str
  tags:
    description:
      - Tags in a cluster.
    type: list
    elements: dict
    suboptions:
      key:
        description:
        - Tag key. The value can contain 1 to 36 characters.
          Only digits, letters, hyphens (-) and underscores (_) are allowed.
      value:
        description:
        - Tag value. The value can contain 0 to 43 characters.
          Only digits, letters, hyphens (-) and underscores (_) are allowed.
  backup_strategy:
    description:
      - Automatic snapshot creation. This function is disabled by default.
    type: dict
    suboptions:
      period:
        description:
        - Time when a snapshot is created every day. Snapshots can only be created
            on the hour. The time format is the time followed by the time zone,
            specifically, HH:mm z. In the format, HH:mm refers to the hour time and
            z refers to the time zone, for example, 00:00 GMT+08:00 and 01:00
            GMT+08:00.
        type: str
      prefix:
        description:
          - Prefix of the name of the snapshot that is automatically created.
        type: str
      keepday:
        description:
        - Number of days for which automatically created snapshots are reserved.
          Value range is 1 to 90
        type: int
      bucket:
        description:
        - OBS bucket used for storing backup.
          If there is snapshot data in an OBS bucket,
          only the OBS bucket will be used for backup storage and cannot be changed.
        type: str
      basepath:
        description:
        - Storage path of the snapshot in the OBS bucket.
        type: str
      agency:
        description:
        - IAM agency used to access OBS.
        type: str
  state:
    description: Instance state
    type: str
    choices:
      - present
      - absent
    default: present
'''

RETURN = '''
cluster:
    description: Dictionary of CSS cluster
    returned: changed
    type: list
    sample: [
        {
            "cluster": {
                "id": "ef683016-871e-48bc-bf93-74a29d60d214",
                "name": "ES-Test"
            }
        }
    ]
'''

EXAMPLES = '''
#Create CSS Cluster
---
- hosts: localhost
  tasks:
    - name: Create CSS cluster
      opentelekomcloud.cloud.css_cluster:
        name: ES-Test
        state: present
        instance_num: 3
        volume_size: 40
        authority_enable: false
        volume_type: common
        router: '{{ router_id }}'
        net: '{{ net_id }}'
        security_group: '{{ security_group_id }}'
        flavor: 'css.xlarge.2'
        https_enable: false
        system_encrypted: 0
        tags:
        - 'key': "key0"
          'value': "value0"
        - 'key': "key1"
          'value': "value1"
        backup_strategy:
          period: "00:00 GMT+03:00"
          prefix: "yetanother"
          keepday: 1
          agency: "css-agency"
          bucket: "css-bucket"
          basepath: "css-test"

#Delete CSS Cluster
- hosts: localhost
  tasks:
    - name: Create CSS cluster
      opentelekomcloud.cloud.css_cluster:
        name: ES-Test
        state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CssClusterModule(OTCModule):
    argument_spec = dict(
        name=dict(type='str', required=True),
        datastore_version=dict(type='str', choices=['7.6.2', '7.9.3'], default='7.6.2'),
        datastore_type=dict(type='str', default='elasticsearch'),
        instance_num=dict(type='int'),
        flavor=dict(type='str'),
        volume_type=dict(type='str', choices=['common', 'high', 'ultrahigh']),
        volume_size=dict(type='int'),
        system_encrypted=dict(type='int', choices=[0, 1]),
        system_cmkid=dict(type='str'),
        https_enable=dict(type='bool'),
        authority_enable=dict(type='bool'),
        admin_pwd=dict(type='str', no_log=True),
        router=dict(type='str'),
        net=dict(type='str'),
        security_group=dict(type='str'),
        tags=dict(required=False, type='list', elements='dict'),
        backup_strategy=dict(type='dict', options=dict(
            period=dict(type='str'),
            prefix=dict(type='str'),
            keepday=dict(type='int'),
            bucket=dict(type='str'),
            basepath=dict(type='str'),
            agency=dict(type='str'),
        )),

        state=dict(type='str',
                   choices=['present', 'absent'],
                   default='present')
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present',
             ['flavor', 'router', 'net',
              'security_group', 'instance_num']),
            ('authority_enable', 'true',
             ['admin_pwd']),
            ('system_encrypted', '1',
             ['system_cmkid'])
        ],
        supports_check_mode=True
    )

    def _system_state_change(self, cluster):
        state = self.params['state']
        if state == 'present':
            if not cluster:
                return True
        elif state == 'absent' and cluster:
            return True
        return False

    def run(self):
        changed = False

        cluster = self.conn.css.find_cluster(
            name_or_id=self.params['name'],
            ignore_missing=True
        )

        if self.ansible.check_mode:
            self.exit_json(changed=self._system_state_change(cluster))

        # Delete cluster
        if self.params['state'] == 'absent':
            if cluster:
                changed = True
                self.conn.css.delete_cluster(cluster=cluster.id,
                                             ignore_missing=True)
            self.exit_json(changed=changed)

        # Create cluster
        elif self.params['state'] == 'present':
            if cluster:
                self.exit(changed=changed)

            if not cluster:
                changed = True
                volume_type = self.params['volume_type']

                attrs = {
                    'datastore': {
                        'type': self.params['datastore_type'],
                        'version': self.params['datastore_version']
                    },
                    'instance': {
                        "flavorRef": self.params['flavor'],
                        'nics': {
                            'netId': self.params['net'],
                            'vpcId': self.params['router'],
                            'securityGroupId': self.params['security_group']
                        },
                        'volume': {
                            'volume_type': volume_type.upper(),
                            'size': self.params['volume_size']
                        }
                    },
                    'diskEncryption': {
                        'systemEncrypted': self.params['system_encrypted']
                    },
                    'backupStrategy': {},
                    'name': self.params['name']
                }

                if self.params['system_cmkid']:
                    attrs['diskEncryption']['systemCmkid'] = self.params['system_cmkid']
                if self.params['instance_num']:
                    attrs['instanceNum'] = self.params['instance_num']
                if self.params['https_enable']:
                    attrs['httpsEnable'] = self.params['https_enable']
                if self.params['authority_enable']:
                    attrs['authorityEnable'] = self.params['authority_enable']
                if self.params['admin_pwd']:
                    attrs['adminPwd'] = self.params['admin_pwd']
                if self.params['tags']:
                    attrs['tags'] = self.params['tags']

                if self.params['backup_strategy']:
                    if self.params['backup_strategy']['period']:
                        attrs['backupStrategy']['period'] = self.params['backup_strategy']['period']
                    if self.params['backup_strategy']['prefix']:
                        attrs['backupStrategy']['prefix'] = self.params['backup_strategy']['prefix']
                    if self.params['backup_strategy']['bucket']:
                        attrs['backupStrategy']['bucket'] = self.params['backup_strategy']['bucket']
                    if self.params['backup_strategy']['basepath']:
                        attrs['backupStrategy']['basePath'] = self.params['backup_strategy']['basepath']
                    if self.params['backup_strategy']['agency']:
                        attrs['backupStrategy']['agency'] = self.params['backup_strategy']['agency']
                    if self.params['backup_strategy']['keepday'] in range(1, 90):
                        attrs['backupStrategy']['keepDay'] = self.params['backup_strategy']['keepday']
                    else:
                        self.exit(
                            changed=False,
                            failed=True,
                            message='backup strategy keepday must be in range from 1 to 90'
                        )

                cluster = self.conn.css.create_cluster(**self.params)

            self.exit_json(
                changed=changed,
                css_cluster=cluster.to_dict(),
                id=cluster.id
            )


def main():
    module = CssClusterModule()
    module()


if __name__ == '__main__':
    main()
