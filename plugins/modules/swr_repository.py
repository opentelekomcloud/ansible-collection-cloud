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
    type: str
    required: true
  repository:
    description:
      - Mandatory name of repository.
    type: str
    required: true  
  category:
    description:
      - Repository type
    choices: ['app_server', 'linux', 'framework_app', 'database', 'lang', 'other', 'windows', 'arm']
    type: str
  description:
    description:
      - Brief description of the image repository
    type: str
  is_public:
    description:
      - Is repository public or not
    type: bool
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
# class SwrRepositoryMachine(StateMachine):


class SwrRepositoryModule(OTCModule):
    argument_spec = dict(
        namespace=dict(required=True),
        repository=dict(required=True),
        category=dict(required=False,
                      choices=['app_server', 'linux', 'framework_app', 'database', 'lang', 'other', 'windows', 'arm']),
        is_public=dict(required=False),
        description=dict(required=False),
        state=dict(type='str', required=False,
                   choices=['present', 'absent'],
                   default='present'),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        service_name = "swr"
        type_name = "repository"
        session = getattr(self.conn, service_name)
        create_function = getattr(session, 'create_{0}'.format(type_name))
        delete_function = getattr(session, 'delete_{0}'.format(type_name))
        get_function = getattr(session, 'get_{0}'.format(type_name))
        list_function = getattr(session, 'repositories')
        update_function = getattr(session, 'update_{0}'.format(type_name))
        crud = dict(
            create=create_function,
            delete=delete_function,
            find=get_function,
            get=get_function,
            list=list_function,
            update=update_function,)
        sm = StateMachine(connection=self.conn,
                          sdk=self.sdk,
                          service_name=service_name,
                          type_name=type_name,
                          crud_functions=crud)
        kwargs = {'state': self.params['state'],
                  'attributes': dict((k, self.params[k]) for k in
                                     ['namespace', 'repository', 'category', 'is_public', 'description']
                                     if self.params[k] is not None)}
        repository, is_changed = sm(check_mode=self.ansible.check_mode,
                                    non_updateable_attributes=['namespace', 'repository'],
                                    updateable_attributes=['category', 'is_public', 'description'],
                                    wait=False,
                                    timeout=600,
                                    **kwargs)
        self.exit_json(repository=repository, changed=is_changed)


def main():
    module = SwrRepositoryModule()
    module()


if __name__ == "__main__":
    main()
