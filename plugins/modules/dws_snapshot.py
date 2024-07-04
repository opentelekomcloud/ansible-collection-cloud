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

DOCUMENTATION = """
module: dws_snapshot
short_description: Manage DWS snapshots
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.14.4"
author: "Attila Somogyi (@sattila1999)"
description:
  - Manage DWS snapshots
options:
  cluster:
    description:
      - Name or ID of DWS cluster.
    type: str
  name:
    description:
      - Name of DWS snapshot name must be start with letter.
      - Name must be 4 to 64 characters in length.
      - The backup name must be unique.
    type: str
    required: true
  description:
    description:
        - Description of a snapshot.
        - The value contains 0 to 256 characters, and angle brackets (<) and (>) are not allowed.
    type: str
  state:
    description: Whether dws snapshot should be present or absent.
    choices: [present, absent]
    default: present
    type: str
  wait:
    description:
      - If the module should wait for the cluster to be created.
    type: bool
    default: 'yes'
  timeout:
    description:
      - The amount of time the module should wait for the cluster to get
        into active state.
    default: 600
    type: int
requirements: ["openstacksdk", "otcextensions"]
"""

RETURN = """
snapshots:
  description: Specifies the DWS snapshot.
  returned: changed
  type: complex
  contains:
    cluster_id:
      description: ID of the snapshot.
      type: str
      sample: "4cbf8cab-0925-5d4b-odd4-cb6667b8"
    name:
      description: Snapshot name, which must be unique and start with a letter.
      type: str
      sample: "snapshot_101"
    description:
      description:
        - Snapshot description.
        - If no value is specified, the description is empty.
      type: str
      sample: "Snapshot-3 description"
"""

EXAMPLES = """
# Create dws snapshot
- opentelekomcloud.cloud.dws_snapshot:
    cluster: "test-dws"
    name: "snapshot_01"
  register: dws_snapshot

# Delete dws snapshot
- opentelekomcloud.cloud.dws_snapshot:
    cluster: "test-dws"
    name: "snapshot_01"
    state: absent
"""

from ansible_collections.openstack.cloud.plugins.module_utils.resource import (
    StateMachine,
)
from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import (
    OTCModule,
)


class DwsSnapshotModule(OTCModule):
    argument_spec = dict(
        name=dict(type='str', required=True),
        cluster=dict(type='str'),
        description=dict(),
        state=dict(choices=['present', 'absent'], default='present'),
        wait=dict(type='bool', default=True),
        timeout=dict(type='int', default=600),
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['cluster']),
        ],
        supports_check_mode=True,
    )

    class _StateMachine(StateMachine):
        def _create(self, attributes, timeout, wait, **kwargs):
            resource = self.create_function(**attributes)
            wait_function = getattr(self.session, 'wait_for_cluster')
            if attributes.get('cluster_id'):
                wait_function(attributes['cluster_id'], wait=timeout)
            return self.get_function(resource.id)

        def _find_matches(self, attributes, **kwargs):
            return self.list_function()

    def run(self):
        service_name = 'dws'
        type_name = 'snapshot'
        session = getattr(self.conn, 'dws')
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

        kwargs['attributes'] = dict(
            (k, self.params[k])
            for k in ['name', 'description']
            if self.params[k] is not None
        )

        if self.params['cluster']:
            cluster = self.conn.dws.find_cluster(
                self.params['cluster'], ignore_missing=False
            )

            kwargs['attributes']['cluster_id'] = cluster.id

        snapshot, is_changed = sm(
            check_mode=self.ansible.check_mode,
            updateable_attributes=[],
            non_updateable_attributes=[
                'name',
                'cluster',
                'description',
            ],
            **kwargs
        )
        if snapshot is None:
            self.exit_json(changed=is_changed)
        else:
            self.exit_json(
                changed=is_changed,
                dws_snapshot=snapshot.to_dict(computed=False),
            )


def main():
    module = DwsSnapshotModule()
    module()


if __name__ == '__main__':
    main()
