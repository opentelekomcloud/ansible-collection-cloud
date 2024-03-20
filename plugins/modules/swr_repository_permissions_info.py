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
module: swr_repository_permissions_info
short_description: Get SWR repository permissions info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.14.2"
author: "Ziukina Valeriia (@RusselSand)"
description:
  - Get repository permissions info from Software Repository for Containers
options:
  namespace:
    description:
      - Mandatory name of an organisation
    type: str
  repository:
    description:
      - Mandatory name of a repository
    type: str
  user_name:
    description:
      - Optional user name
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
organizations:
  description: Dictionary describing organizations
  type: complex
  returned: On Success.
  contains:
      namespace:
        description: Name of organization.
        type: str
      repository:
        description: Name of repository.
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
      self_auth:
        description: Check if this permission is for user who is making request
        type: bool
'''

EXAMPLES = '''
# Get SWR repository permissions information
- opentelekomcloud.cloud.swr_repository_permissions_info:
    namespace: org_name
    repository: repo_name
  register: swr_repository_permissions
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SwrRepoPermissionInfoModule(OTCModule):
    argument_spec = dict(
        namespace=dict(required=True),
        repository=dict(required=True),
        user_name=dict(required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        permissions = self.conn.swr.repository_permissions(namespace=self.params['namespace'],
                                                           repository=self.params['repository'])
        all_auth = list()
        for permission in permissions:
            permission_dict = {'namespace': permission['namespace'],
                               'repository': permission['repository'],
                               'user_id': permission['self_auth']['user_id'],
                               'user_name': permission['self_auth']['user_name'],
                               'user_auth': permission['self_auth']['auth'],
                               'self_auth': True}
            all_auth.append(permission_dict)
            for other_permission in permission['others_auths']:
                permission_dict = {'namespace': permission['namespace'],
                                   'repository': permission['repository'],
                                   'user_id': other_permission['user_id'],
                                   'user_name': other_permission['user_name'],
                                   'user_auth': other_permission['auth'],
                                   'self_auth': False}
                all_auth.append(permission_dict)
        if self.params['user_name']:
            all_auth = list(filter(lambda x: x['user_name'] == self.params['user_name'], all_auth))
        self.exit_json(
            changed=False,
            permissions=all_auth
        )


def main():
    module = SwrRepoPermissionInfoModule()
    module()


if __name__ == "__main__":
    main()
