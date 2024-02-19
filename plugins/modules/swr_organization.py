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
      - Mandatory name of an organization. Only lowercase letters, digits, 
        periods (.), underscores (_), and hyphens (-) are allowed. Must start
        with letter. Length up to 64 characters.
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
    ?
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


class SwrOrganizationModule(OTCModule):
    argument_spec = dict(
        namespace=dict(required=False),
        state=dict(type='str', required=False,
                   choices=['present', 'absent'],
                   default='present'),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        sm = StateMachine(connection=self.conn,
                           sdk=self.sdk,
                           service_name='swr',
                           type_name='organization')

        kwargs = {'state': self.params['state'], 'attributes': {}}
        kwargs['attributes']['namespace'] = self.params['namespace']
        resource, is_changed = sm(check_mode=self.ansible.check_mode,
                                  non_updateable_attributes=['namespace'],
                                  **kwargs)
        #если создание, сделать потом get
        self.exit_json(resource=resource, changed=is_changed)


def main():
    module = SwrOrganizationModule()
    module()


if __name__ == "__main__":
    main()
