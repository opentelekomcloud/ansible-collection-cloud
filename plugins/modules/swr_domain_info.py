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
module: swr_domain_info
short_description: Get SWR image repositories info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.14.2"
author: "Ziukina Valeriia (@RusselSand)"
description:
  - Get image repositories info from Software Repository for Containers
options:
  namespace:
    description:
      - Mandatory name of an organization
    type: str
    required: true
  repository:
    description:
      - Mandatory name of the repository
    type: str
    required: true
  domain:
    description:
      - Optional name of the domain
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
domains:
  description: Dictionary describing domains
  type: complex
  returned: On Success.
  contains:
    exist:
      description: Domain exists or not
      type: bool
      sample: true
    namespace:
      description: Organization name
      type: str
      sample: "org_name"
    repository:
      description: Repository name
      type: str
      sample: "repo_name"
    access_domain:
      description: Domain name
      type: str
      sample: "domain_name"
    permit:
      description: Permission
      type: str
      sample: "read"
    deadline:
      description: Expiration time
      type: str
      sample: "2021-10-01T16:00:00Z"
    description:
      description: Description
      type: str
      sample: "description"
    creator_id:
      description: ID of the creator
      type: str
      sample: "0504186e6a8010e01f3ec009a7279baa"
    creator_name:
      description: Name of the creator
      type: str
      sample: "xxx"
    created:
      description: Time when an image is created. It is the UTC standard time.
      type: str
      sample: "2021-06-10T08:14:42.56632Z"
    updated:
      description: Time when an image is updated. It is the UTC standard time.
      type: str
      sample: "2021-06-10T08:14:42.56632Z"
    status:
      description: Status. Valid of true, expired if false
      type: bool
      sample: true
'''

EXAMPLES = '''
# Get SWR organisations information
- opentelekomcloud.cloud.swr_domain_info:
    namespace: org_name
    repository: repo_name
    domain: OTC00000000001000000100
  register: swr_domain_info
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SwrOrganisationInfoModule(OTCModule):
    argument_spec = dict(
        namespace=dict(required=True),
        repository=dict(required=True),
        domain=dict(required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        if self.params['domain']:
            domains = self.conn.swr.get_domain(self.params['namespace'],
                                               self.params['repository'],
                                               self.params['domain'])
        else:
            query = {'namespace': self.params['namespace'],
                     'repository': self.params['repository']}
            domains = list(self.conn.swr.domains(**query))
        self.exit_json(
            changed=False,
            domains=domains
        )


def main():
    module = SwrOrganisationInfoModule()
    module()


if __name__ == "__main__":
    main()
