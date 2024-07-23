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

DOCUMENTATION = """
module: css_snapshot
short_description: Manage CSS snapshots
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.10.0"
author: "Vladimir Vshivkov (@enrrou)"
description:
  - Manage CSS snapshots
options:
  cluster:
    description:
      - Name or ID of CSS cluster.
    required: true
    type: str
  name:
    description:
      - Name of CSS snapshot name must be start with letter.
      - Name must be 4 to 64 characters in length.
      - The backup name must be unique.
    required: true
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
  wait:
     description:
        - If the module should wait for the snapshot to be created.
     type: bool
     default: 'yes'
  timeout:
    description:
      - The amount of time the module should wait for the snapshot to be created.
    default: 600
    type: int
requirements: ["openstacksdk", "otcextensions"]
"""

RETURN = """
css_snapshot:
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
"""

EXAMPLES = """
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
"""

from ansible_collections.openstack.cloud.plugins.module_utils.resource import (
    StateMachine,
)
from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import (
    OTCModule,
)


class CssSnapshotModule(OTCModule):
    argument_spec = dict(
        name=dict(type='str', required=True),
        cluster=dict(type='str', required=True),
        description=dict(),
        indices=dict(),
        state=dict(choices=['present', 'absent'], default='present'),
        wait=dict(type='bool', default=True),
        timeout=dict(type='int', default=600)
    )
    module_kwargs = dict(supports_check_mode=True)

    class _StateMachine(StateMachine):
        def _create(self, attributes, timeout, wait, **kwargs):
            cluster = attributes['cluster']
            resource = self.create_function(**attributes)
            wait_function = getattr(self.session, 'wait_for_cluster')
            wait_function(cluster, timeout=timeout)
            return self.find_function(cluster, resource.id)

        def _find(self, attributes, **kwargs):
            # use find_* functions for id instead of get_* functions because
            # get_* functions raise exceptions when resources cannot be found
            cluster = attributes['cluster']
            for k in ['id', 'name']:
                if k in attributes:
                    return self.find_function(cluster, attributes[k])

            matches = list(self._find_matches(attributes, **kwargs))
            if len(matches) > 1:
                self.fail_json(msg='Found more than a single resource'
                                   ' which matches the given attributes.')
            elif len(matches) == 1:
                return matches[0]
            else:  # len(matches) == 0
                return None

        def _delete(self, resource, attributes, timeout, wait, **kwargs):
            cluster = attributes['cluster']
            self.delete_function(cluster, resource['id'])

            if wait:
                for count in self.sdk.utils.iterate_timeout(
                    timeout=timeout,
                    message="Timeout waiting for resource to be absent"
                ):
                    if self._find(attributes) is None:
                        break

        def _build_update(self, resource, attributes, updateable_attributes,
                          non_updateable_attributes, **kwargs):
            return {}

    def run(self):
        service_name = 'css'
        type_name = 'snapshot'
        session = getattr(self.conn, 'css')
        create_function = getattr(session, 'create_{0}'.format(type_name))
        delete_function = getattr(session, 'delete_{0}'.format(type_name))
        find_function = getattr(session, 'find_{0}'.format(type_name))
        list_function = getattr(session, '{0}s'.format(type_name))

        crud_functions = dict(
            create=create_function,
            delete=delete_function,
            find=find_function,
            get=None,
            list=list_function,
            update=None,
        )

        sm = self._StateMachine(
            connection=self.conn,
            sdk=self.sdk,
            type_name=type_name,
            service_name=service_name,
            crud_functions=crud_functions
        )

        kwargs = dict(
            (k, self.params[k])
            for k in ['state', 'timeout', 'wait']
            if self.params[k] is not None
        )

        kwargs['attributes'] = dict(
            (k, self.params[k])
            for k in ['name', 'description', 'indices']
            if self.params[k] is not None
        )
        cluster = self.conn.css.find_cluster(
            self.params['cluster'], ignore_missing=False
        )
        kwargs['attributes']['cluster'] = cluster

        snapshot, is_changed = sm(
            check_mode=self.ansible.check_mode,
            updateable_attributes=[],
            non_updateable_attributes=[],
            **kwargs,
        )
        if snapshot is None:
            self.exit_json(changed=is_changed)
        else:
            self.exit_json(changed=is_changed,
                           css_snapshot=snapshot.to_dict(computed=False))


def main():
    module = CssSnapshotModule()
    module()


if __name__ == '__main__':
    main()
