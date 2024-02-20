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
module: swr_repository_info
short_description: Get SWR repositories info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.14.2"
author: "Ziukina Valeriia (@RusselSand)"
description:
  - Get repositories info from Software Repository for Containers
options:
  namespace:
    description:
      - Optional name of an organisation
    type: str
  repository:
    description:
      - Optional name of a repository
    type: str
  center:
    description:
      - Use only if you need self-owned images
    type: str
    choices: ['self']
  category:
    description:
      - Repository type.
    type: str
    choices: ['app_server', 'linux', 'framework_app', 'database', 'lang', 'other', 
    'windows', 'arm']
  offset:
    description:
      - start index. Can be used only with limit
    type: str
  limit:
    description:
      - number of returned records. Can be used only with offset
    type: str
  order_column:
    description:
      - Sorting criteria. Can be used only with order_type
    type: str
    choices: ['name', 'updated_time', 'tag_count']
  order_type:
    description:
      - Sorting type. Can be used only with order_column
    type: str
    choices: ['desc', 'asc']
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
repositories:
  description: Dictionary describing repositories
  type: complex
  returned: On Success.
  contains:
    id:
      description: Repository ID
      type: int
      sample: 1343008
    ns_id:
      description: Organization ID
      type: int
      sample: 1343
    name:
      description: Image repository name
      type: str
      sample: "repo_name"
    category:
      description: Image repository type
      type: str
      sample: "app_server"
    description:
      description: Brief description of the image repository
      type: str
      sample: "this is example test repository"
    creator_id:
      description: Image repository creator ID
      type: str
      sample: "8b17f8573e8c4a7a8a04e0fe8e60dfa3"
    creator_name:
      description: Image repository creator
      type: str
      sample: "username"
    size:
      description: Image repository size
      type: int
      sample: 0
    is_public:
      description: Repository is public or not
      type: bool
      sample: True
    num_images:
      description: Number of images in repository
      type: int
      sample: 1
    num_download:
      description: Download times of an image repository.
      type: int
      sample: 0
    url:
      description: URL of the image repository logo image. Empty by default
      type: str
      sample: ""
    path:
      description: External image pull address
      type: str
      sample: "swr.eu-de.otc.t-systems.com/org_name/swr_repo"
    internal_path:
      description: Internal image pull address
      type: str
      sample: "100.125.7.20:20202/org_name/swr_repo"
    created:
      description: Time when an image repository is created
      type: str
      sample: "2024-02-19T10:20:36.285975Z"
    updated:
      description: Time when an image repository is updated
      type: str
      sample: "2024-02-19T10:20:36.285976Z"
    domain_id:
      description: Account ID
      type: str
      sample: "859d69666ff44ba6a20855edb43f311e"
    priority:
      description: Image sorting priority.
      type: int
      sample: 0
    tags:
      description: Image tag list.
      type: list
      sample: []
    status:
      description: (Reserved field) Status.
      type: bool
      sample: False
    total_range:
      description: Total number of records.
      type: int
      sample: 1
'''

EXAMPLES = '''
# Get SWR repositories information
- opentelekomcloud.cloud.swr_repository_info:
    namespace: org_name
    name: repo_name
  register: swr_repository_info
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SwrRepositoryInfoModule(OTCModule):
    argument_spec = dict(
        namespace=dict(required=False),
        repository=dict(required=False),
        center=dict(required=False),
        category=dict(required=False),
        offset=dict(required=False),
        limit=dict(required=False),
        order_column=dict(required=False),
        order_type=dict(required=False),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        if self.params['namespace'] and self.params['repository']:
            repos = self.conn.swr.get_repository(
                namespace=self.params['namespace'],
                repository=self.params['repository']
            )
        else:
            query = {}

            namespace = self.params['namespace']
            name = self.params['repository']
            center = self.params['center']
            category = self.params['category']
            offset = self.params['offset']
            limit = self.params['limit']
            order_column = self.params['order_column']
            order_type = self.params['order_type']

            if namespace:
                query['namespace'] = namespace
            if name:
                query['name'] = name
            if center:
                query['center'] = center
            if category:
                query['category'] = category
            if offset and limit:
                query['offset'] = offset
                query['limit'] = limit
            if order_column and order_type:
                query['order_column'] = order_column
                query['order_type'] = order_type

            repos = list(self.conn.swr.repositories(**query))
        self.exit_json(
            changed=False,
            repositories=repos
        )


def main():
    module = SwrRepositoryInfoModule()
    module()


if __name__ == "__main__":
    main()
