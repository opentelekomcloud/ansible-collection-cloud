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
module: swr_organization
short_description: Create, update or delete organizations in SWR
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.14.2"
author: "Ziukina Valeriia (@RusselSand)"
description:
  - Create, update or delete organizations in Software Repository for Containers
options:
  namespace:
    description:
      - Mandatory name of organization.
      - Only lowercase letters, digits, periods (.), underscores (_), and hyphens (-) are allowed.
      - Must start with letter.
      - Length up to 64 characters.
    type: str
  state:
    description:
      - Whether resource should be present or absent.
    choices: ['present', 'absent']
    type: str
    default: 'present'
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
organization:
    description: Organization object.
    type: complex
    returned: On Success.
    contains:
      id:
        description: Specifies the ID of the organization.
        type: int
      name:
        description: Specifies the name of the organization.
        type: str
      auth:
        description: User permission
        type: int
      creator_name:
        description: Name of the creator og the organization
        type: str
'''

EXAMPLES = '''
# Get SWR organisations information
- name: Create new organization
  opentelekomcloud.cloud.swr_organization:
    namespace: org_name

- name: Delete an organization
  opentelekomcloud.cloud.swr_organization:
    namespace: org_name
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule
from ansible_collections.openstack.cloud.plugins.module_utils.resource import StateMachine


class SwrOrganizationMachine(StateMachine):
    def __call__(self, attributes, check_mode, state, timeout, wait,
                 updateable_attributes, non_updateable_attributes, **kwargs):
        # kwargs is for passing arguments to subclasses

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
            return resource, False

        elif state == 'absent' and resource:
            # Delete resource
            self._delete(resource, attributes, timeout, wait, **kwargs)
            return None, True

        elif state == 'absent' and not resource:
            # Do nothing
            return None, False

    def _delete(self, resource, attributes, timeout, wait, **kwargs):
        self.delete_function(**attributes)


class SwrOrganizationModule(OTCModule):
    argument_spec = dict(
        namespace=dict(required=True),
        state=dict(type='str', required=False,
                   choices=['present', 'absent'],
                   default='present'),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        service_name = "swr"
        type_name = "organization"
        session = getattr(self.conn, service_name)
        create_function = getattr(session, 'create_{0}'.format(type_name))
        delete_function = getattr(session, 'delete_{0}'.format(type_name))
        find_function = getattr(session, 'find_{0}'.format(type_name))
        get_function = getattr(session, 'get_{0}'.format(type_name))
        list_function = getattr(session, '{0}s'.format(type_name))
        crud = dict(
            create=create_function,
            delete=delete_function,
            find=find_function,
            get=get_function,
            list=list_function,
            update=None,
        )
        sm = SwrOrganizationMachine(connection=self.conn,
                                    sdk=self.sdk,
                                    service_name=service_name,
                                    type_name=type_name,
                                    crud_functions=crud)

        kwargs = {'state': self.params['state'], 'attributes': {}}
        kwargs['attributes']['namespace'] = self.params['namespace']
        organization, is_changed = sm(check_mode=self.ansible.check_mode,
                                      non_updateable_attributes=['namespace'],
                                      updateable_attributes=[],
                                      wait=False,
                                      timeout=600,
                                      **kwargs)
        # если создание, сделать потом get
        self.exit_json(organization=organization, changed=is_changed)


def main():
    module = SwrOrganizationModule()
    module()


if __name__ == "__main__":
    main()
