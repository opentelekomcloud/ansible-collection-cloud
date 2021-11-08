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
module: css_snapshot
short_description: Manage CSS snapshots
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.9.0"
author: "Vladimir Vshivkov (@enrrou)"
description:
  - Manage CSS snapshots
options:
  cluster:
    description:
      - Name or ID of CSS cluster.
    type: str
    required: true
  name:
    description:
      - Name of CSS snapshot name must be start with letter.
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
#Query CSS Snapshots
---
- hosts: localhost
  tasks:
    - name: Get CSS Snapshots
      opentelekomcloud.cloud.css_snapshot:
        cluster: test
      register: result
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CssSnapshotModule(OTCModule):
    argument_spec = dict(
        name=dict(type='str', required=True),
        cluster=dict(type='str', required=True),
        description=dict(type='str', required=False),
        indices=dict(type='str'),
        state=dict(type='str',
                   choices=['present', 'absent'],
                   default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        attrs = {}
        name = self.params['name']
        snapshot_description = self.params['description']

        if self.params['description']:
            attrs['description'] = self.params['description']
        if self.params['indices']:
            attrs['indices'] = self.params['indices']

        if self.params['name']:
            if self.params['cluster']:
                cluster = self.conn.css.find_cluster(name_or_id=attrs['cluster'])
                print(cluster)

                if cluster:
                    changed = False

                    if self.ansible.check_mode:
                        self.exit(changed=self._system_state_change(name))

                    if self.params['state'] == 'present':
                        attrs['name'] = name

                        if snapshot_description:
                            attrs['description'] = snapshot_description

                            snapshot = self.conn.css.create_snapshot(cluster, **attrs)
                            print(snapshot)
                            changed = True

                            self.exit(changed=changed,
                                      snapshot=snapshot.to_dict(),
                                      id=snapshot.id,
                                      msg='CSS snapshot with name %s was created' % name)

                        else:
                            changed = False
                            self.fail(changed=changed,
                                      msg='CSS snapshot with name %s '
                                      'already exists' % name)

                    elif self.params['state'] == 'absent':
                        self.conn.css.delete_snapshot(name, cluster)
                        changed = True

                    self.exit(changed=changed,
                              msg='CSS snapshot with name %s was deleted' % name)

                else:
                    changed = False
                    self.fail(changed=changed,
                              msg='CSS snapshot with name %s does not exist' % name)
            else:
                self.fail(msg='CSS snapshot %s does not exist' % self.params['cluster'])


def main():
    module = CssSnapshotModule()
    module()


if __name__ == '__main__':
    main()
