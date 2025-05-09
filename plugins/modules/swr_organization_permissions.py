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
module: swr_organization_permissions
short_description: Create, update or delete organization permissions in SWR
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.14.2"
author: "Ziukina Valeriia (@RusselSand)"
description:
  - Create, update or delete repository permissions in Software Repository for Containers
options:
  namespace:
    description: Mandatory name of organization.
    type: str
    required: true
  user_id:
    description: User ID
    type: str
    required: true
  user_name:
    description: Username
    type: str
    required: true
  user_auth:
    description: User permission (7 — manage, 3 — write, 1 — read)
    default: 1
    choices: [1, 3, 7]
    type: int
  state:
    description:
      - Whether resource should be present or absent.
    choices: ['present', 'absent']
    type: str
    default: 'present'
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
permission:
    description: Repository permission
    type: complex
    returned: On Success.
    contains:
      namespace:
        description: Specifies the name of the organization.
        type: str
'''

EXAMPLES = '''
# Create or delete SWR organization permission
- name: Create new repository permission
  opentelekomcloud.cloud.swr_organization_permissions:
    namespace: organization_name
    user_id: user_id
    user_name: user_name
    user_auth: 7
  register: permission

- name: Delete an repository permission
  opentelekomcloud.cloud.swr_organization_permissions:
    namespace: organization_name
    user_id: user_id
    user_name: user_name
    state: absent
  register: permission
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule
from ansible_collections.openstack.cloud.plugins.module_utils.resource import StateMachine


class SwrOrgPermissionMachine(StateMachine):
    def __call__(self, attributes, check_mode, state, timeout, wait,
                 updateable_attributes, non_updateable_attributes, **kwargs):
        resource = self._find(attributes, **kwargs)
        if check_mode:
            return self._simulate(state, resource, attributes, timeout, wait,
                                  updateable_attributes,
                                  non_updateable_attributes, **kwargs)

        if state == 'present' and not resource:
            # Create resource
            resource = self._create(attributes, timeout, wait, **kwargs)
            return resource, True

        elif state == 'present' and resource:
            # Do not update resource
            resource = self._update(attributes, timeout, wait, **kwargs)
            return resource, True

        elif state == 'absent' and resource:
            # Delete resource
            self._delete(resource, attributes, timeout, wait, **kwargs)
            return None, True

        elif state == 'absent' and not resource:
            # Do nothing
            return None, False

    def _update(self, attributes, timeout, wait, **kwargs):
        resource = self.update_function(**attributes, value="")
        if wait:
            resource = self.sdk.resource.wait_for_status(self.session,
                                                         resource,
                                                         status='active',
                                                         failures=['error'],
                                                         wait=timeout,
                                                         attribute='status')
        return resource

    def _delete(self, resource, attributes, timeout, wait, **kwargs):
        self.delete_function(namespace=attributes['namespace'],
                             user_ids=[attributes['permissions'][0]['user_id']])
        if wait:
            for count in self.sdk.utils.iterate_timeout(
                    timeout=timeout,
                    message="Timeout waiting for resource to be absent"
            ):
                if self._find(attributes) is None:
                    break

    def _find(self, attributes, **kwargs):
        permissions = self.list_function(
            namespace=attributes['namespace'])
        user_id = attributes['permissions'][0]['user_id']
        all_auth = list()
        for permission in permissions:
            all_auth.append(permission['self_auth'])
            all_auth += permission['others_auths']
        current_user = list(filter(lambda x: x['user_id'] == user_id, all_auth))
        if len(current_user) > 1:
            self.fail_json(msg='Found more than a single resource'
                               ' which matches the given attributes.')
        elif len(current_user) == 0:
            return None
        else:
            return current_user[0]


class SwrRepoPermissionModule(OTCModule):
    argument_spec = dict(
        namespace=dict(required=True),
        user_id=dict(required=True),
        user_name=dict(required=True),
        user_auth=dict(required=False,
                       type='int',
                       choices=[1, 3, 7],
                       default=1),
        state=dict(type='str', required=False,
                   choices=['present', 'absent'],
                   default='present'),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        service_name = "swr"
        type_name = "organization_permissions"
        session = getattr(self.conn, service_name)
        create_function = getattr(session, 'create_{0}'.format(type_name))
        delete_function = getattr(session, 'delete_{0}'.format(type_name))
        update_function = getattr(session, 'update_{0}'.format(type_name))
        list_function = getattr(session, 'organization_permissions')
        crud = dict(
            create=create_function,
            delete=delete_function,
            find=None,
            get=None,
            list=list_function,
            update=update_function,
        )
        sm = SwrOrgPermissionMachine(connection=self.conn,
                                     sdk=self.sdk,
                                     service_name=service_name,
                                     type_name=type_name,
                                     crud_functions=crud)
        kwargs = {'state': self.params['state'],
                  'attributes': dict((k, self.params[k]) for k in
                                     ['namespace']
                                     if self.params[k] is not None)}
        kwargs['attributes']['permissions'] = [{
            'user_id': self.params['user_id'],
            'user_name': self.params['user_name'],
            'user_auth': self.params['user_auth']
        }]
        permission, is_changed = sm(check_mode=self.ansible.check_mode,
                                    non_updateable_attributes=['namespace', 'repository'],
                                    updateable_attributes=['permissions'],
                                    wait=False,
                                    timeout=600,
                                    **kwargs)
        self.exit_json(permission=permission, changed=is_changed)


def main():
    module = SwrRepoPermissionModule()
    module()


if __name__ == "__main__":
    main()
