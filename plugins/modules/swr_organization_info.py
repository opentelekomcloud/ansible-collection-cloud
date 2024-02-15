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
module: swr_organization_info
short_description: Get SWR organisations info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.14.2"
author: "Valeriia Ziukina"
description:
  - Get organizations info from Software Repository for Containers
options:
  namespace:
    description:
      - Optional name of an organisation
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
organizations:
  description: Dictionary describing organizations
  type: complex
  returned: On Success.
  contains:
    id:
      description: Organization ID
      type: int
      sample: 1343008
    name:
      description: Organization name
      type: str
      sample: "group"
    creator_name:
      description: IAM username
      type: str
      sample: "username"
    auth:
      description: User permission
      type: int
      sample: 7
'''

EXAMPLES = '''
# Get SWR organisations information
- opentelekomcloud.cloud.swr_organization_info:
    namespace: org_name
  register: swr_organization_info
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SwrOrganisationInfoModule(OTCModule):
    argument_spec = dict(
        namespace=dict(required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        if self.params['namespace']:
            orgs = self.conn.swr.get_organization(self.params['namespace'])
        else:
            orgs = list(self.conn.swr.organizations())
        self.exit_json(
            changed=False,
            organizations=orgs
        )

def main():
    module = SwrOrganisationInfoModule()
    module()


if __name__ == "__main__":
    main()