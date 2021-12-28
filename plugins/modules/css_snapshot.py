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
  name:
    description:
      - Name of CSS snapshot name must be start with letter.
      - Name must be 4 to 64 characters in length.
      - The backup name must be unique.
    type: str
  description:
    description:
        - Description of a snapshot.
        - The value contains 0 to 256 characters, and angle brackets (<) and (>) are not allowed.
    type: str
  indices:
    description:
        - Name of the index to be backed up.
        - Multiple index names are separated by commas (,).
        - By default, data of all indices is backed up.
    type: str
  state:
    description: Whether css snapshot should be present or absent.
    choices: [present, absent]
    default: present
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
snapshots:
  description: Specifies the CSS snapshot.
  returned: changed
  type: complex
  contains:
    id:
        description:  ID of the snapshot.
        returned: On success when C(state=present)
        type: str
        sample: "4dae5bac-0925-4d5b-add8-cb6667b8"
    name:
        description:  Snapshot name.
        returned: On success when C(state=present)
        type: str
        sample: "snapshot_101"
'''

EXAMPLES = '''
# Create css snapshot
- opentelekomcloud.cloud.css_snapshot:
    cluster: "test-css"
    name: "snapshot_01"
  register: css_snapshot

# Delete css snapshot
- opentelekomcloud.cloud.css_snapshot:
    cluster: "test-css"
    name: "snapshot_01"
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CssSnapshotModule(OTCModule):
    argument_spec = dict(
        name=dict(),
        cluster=dict(),
        description=dict(),
        indices=dict(),
        state=dict(choices=['present', 'absent'],
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

                if cluster:
                    changed = False

                    if self.ansible.check_mode:
                        self.exit(changed=self._system_state_change(name))

                    if self.params['state'] == 'present':
                        attrs['name'] = name

                        if snapshot_description:
                            attrs['description'] = snapshot_description

                            snapshot = self.conn.css.create_snapshot(cluster, **attrs)
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
