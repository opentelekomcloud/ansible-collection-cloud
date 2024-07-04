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
  datastore_type:
    choices: [elasticsearch, opensearch]
    description: Datastore type
    type: str
  datastore_version:
    description: Datastore version.
    type: str
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
    default: common
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
    aliases: ['network']
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
        aliases: ['basePath']
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
  wait:
     description:
        - If the module should wait for the cluster to be created.
     type: bool
     default: 'yes'
  timeout:
    description:
      - The amount of time the module should wait for the cluster to get
        into active state.
    default: 1200
    type: int
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
        timeout: 1200
        tags:
        - key: "key0"
          value: "value0"
        - key: "key1"
          value: "value1"
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

from ansible_collections.openstack.cloud.plugins.module_utils.resource import StateMachine
from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CssClusterModule(OTCModule):
    argument_spec = dict(
        name=dict(type='str', required=True),
        datastore_version=dict(type='str'),
        datastore_type=dict(type='str', choices=['elasticsearch', 'opensearch']),
        instance_num=dict(type='int'),
        flavor=dict(type='str'),
        volume_type=dict(type='str', choices=['common', 'high', 'ultrahigh'], default='common'),
        volume_size=dict(type='int'),
        system_encrypted=dict(type='int', choices=[0, 1]),
        system_cmkid=dict(type='str'),
        https_enable=dict(type='bool'),
        authority_enable=dict(type='bool'),
        admin_pwd=dict(type='str', no_log=True),
        router=dict(type='str'),
        net=dict(type='str', aliases=['network']),
        security_group=dict(type='str'),
        tags=dict(required=False, type='list', elements='dict'),
        backup_strategy=dict(
            type='dict',
            options=dict(
                period=dict(type='str'),
                prefix=dict(type='str'),
                keepday=dict(type='int'),
                bucket=dict(type='str'),
                basepath=dict(type='str', aliases=['basePath']),
                agency=dict(type='str'),
            ),
        ),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        wait=dict(type='bool', default=True),
        timeout=dict(type='int', default=1200)
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['flavor', 'router', 'net', 'security_group',
                                  'instance_num', 'volume_size', 'datastore_type',
                                  'datastore_version']),
            ('authority_enable', 'true', ['admin_pwd']),
            ('system_encrypted', '1', ['system_cmkid']),
        ],
        supports_check_mode=True,
    )

    class _StateMachine(StateMachine):

        def _create(self, attributes, timeout, wait, **kwargs):
            resource = self.create_function(**attributes)
            wait_function = getattr(self.session, 'wait_for_cluster')
            wait_function(resource, timeout=timeout)
            return self.get_function(resource.id)

    def run(self):
        service_name = 'css'
        type_name = 'cluster'
        session = getattr(self.conn, 'css')
        create_function = getattr(session, 'create_{0}'.format(type_name))
        delete_function = getattr(session, 'delete_{0}'.format(type_name))
        get_function = getattr(session, 'get_{0}'.format(type_name))
        find_function = getattr(session, 'find_{0}'.format(type_name))
        list_function = getattr(session, '{0}s'.format(type_name))

        crud = dict(
            create=create_function,
            delete=delete_function,
            find=find_function,
            get=get_function,
            list=list_function,
            update=None,
        )

        sm = self._StateMachine(
            connection=self.conn,
            service_name=service_name,
            type_name=type_name,
            sdk=self.sdk,
            crud_functions=crud,
        )

        kwargs = dict(
            (k, self.params[k])
            for k in ['state', 'timeout', 'wait']
            if self.params[k] is not None
        )
        kwargs['attributes'] = {'name': self.params['name']}

        if self.params['state'] == 'present':
            vpc_id = self.conn.vpc.find_vpc(
                self.params['router'], ignore_missing=False).id
            network = self.conn.vpc.find_subnet(
                self.params['net'], ignore_missing=True)
            if not network:
                network = self.conn.network.find_network(
                    self.params['net'], ignore_missing=False)
            net_id = network.id

            security_group_id = self.conn.network.find_security_group(
                self.params['security_group'], ignore_missing=False).id
            attrs = {
                'datastore': {
                    'type': self.params['datastore_type'],
                    'version': self.params['datastore_version'],
                },
                'instanceNum': self.params['instance_num'],
                'instance': {
                    'flavorRef': self.params['flavor'],
                    'volume': {
                        'volume_type': self.params['volume_type'].upper(),
                        'size': self.params['volume_size'],
                    },
                    'nics': {
                        'vpcId': vpc_id,
                        'netId': net_id,
                        'securityGroupId': security_group_id,
                    },
                },
            }
            if self.params['system_cmkid']:
                attrs['diskEncryption'] = {
                    'systemEncrypted': self.params['system_encrypted'] or 1,
                    'systemCmkid': self.params['system_cmkid'],
                }
            if self.params['https_enable']:
                attrs['httpsEnable'] = self.params['https_enable']
            if self.params['authority_enable']:
                attrs['authorityEnable'] = self.params['authority_enable']
            if self.params['admin_pwd']:
                attrs['adminPwd'] = self.params['admin_pwd']
            if self.params['tags']:
                attrs['tags'] = self.params['tags']
            if self.params['backup_strategy']:
                if self.params['backup_strategy'].get('basepath'):
                    del self.params['backup_strategy']['basepath']
                attrs['backupStrategy'] = self.params['backup_strategy']
            kwargs['attributes'].update(**attrs)

        cluster, is_changed = sm(
            check_mode=self.ansible.check_mode,
            updateable_attributes=[],
            non_updateable_attributes=[
                'name', 'datastore_type', 'datastore_version', 'instance_num',
                'volume_size', 'volume_type', 'router', 'net', 'security_group',
                'flavor', 'backup_strategy', 'timeout', 'tags', 'system_encrypted',
                'system_cmkid', 'https_enable', 'authority_enable', 'admin_pwd'],
            **kwargs
        )

        if cluster is None:
            self.exit_json(changed=is_changed)
        else:
            self.exit_json(
                changed=is_changed,
                css_cluster=cluster.to_dict(computed=False),
            )


def main():
    module = CssClusterModule()
    module()


if __name__ == '__main__':
    main()
