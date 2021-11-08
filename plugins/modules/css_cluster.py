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
version_added: "0.9.0"
author: "Vladimir Vshivkov (@enrrou)"
description:
  - Manage CSS clusters
options:
  cluster:
    description:
      - Name or ID of CSS cluster.
    type: str
    required: true
  name:
    description:
      - Name of RDS backup name must be start with letter.
      - Name must be 4 to 64 characters in length.
      - The backup name must be unique.
    required: true
    type: str

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
snapshots:
    description: Dictionary of CSS snapshot
    returned: changed
    type: list
    sample: [
        {
            "snapshot_list": [
                {
                    "id": null,
                    "name": null,
                }
            ]
        }
    ]
'''

EXAMPLES = '''
#Create CSS Cluster
---
- hosts: localhost
  tasks:
    - name: Create CSS Cluster
      opentelekomcloud.cloud.css_cluster:
        cluster: test
        state: present
        datastore_version: 7.6.2
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CssClusterModule(OTCModule):
    argument_spec = dict(
        name=dict(type='str', required=True),
        cluster=dict(type='str', required=True),
        datastore_version=dict(type='str', choices=['6.2.3', '7.1.1', '7.6.2'], default='6.2.3'),
        datastore_type=dict(type='str', default='elasticsearch'),
        instance_num=dict(type='int'),
        instance_flavor=dict(type='str'),
        instance_volume_type=dict(type='str', choices=['COMMON', 'HIGH', 'ULTRAHIGH']),
        instance_volume_size=dict(type='int'),
        backup_period=dict(type='str'),
        backup_prefix=dict(type='str'),
        backup_keepday=dict(type='int'),
        disk_encryption=dict(type='str'),
        system_cmkid=dict(type='str'),
        https_enable=dict(type='str', choices=['true', 'false']),
        authority_enable=dict(type='bool'),
        admin_pwd=dict(type='str'),
        tag_key=dict(type='str'),
        tag_value=dict(type='str'),
        state=dict(type='str',
                   choices=['present', 'absent'],
                   default='present')
    )
    module_kwargs = dict(
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
        attrs = {}

        cluster = None
        changed = False

        cluster = self.conn.css.find_cluster(
            name_or_id=self.params['name'])

        if self.ansible.check_mode:
            self.exit_json(changed=self._system_state_change(cluster))

        if self.params['state'] == 'present':
            if not cluster:
                changed = True
                cluster = self.conn.css.create_cluster(**self.params)
            else:
                pass

            self.exit_json(
                changed=changed,
                css_cluster=cluster.to_dict(),
                id=cluster.id
            )

        elif self.params['state'] == 'absent':
            changed = False

            if cluster:
                # Delete cluster
                attrs = {
                    'cluster': cluster.id
                }

                changed = True
                self.conn.css.delete_cluster(**attrs)

            self.exit_json(changed=changed)


def main():
    module = CssClusterModule()
    module()


if __name__ == '__main__':
    main()
