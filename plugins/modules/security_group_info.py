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
module: security_group_info
short_description: Lists security groups
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Tino Schreiber (@tischrei)"
description:
  - List security groups
options:
  description:
    description:
      - Description of the security group
    type: str
  project_id:
    description:
      - Specifies the project id as filter criteria
    type: str
  name:
    description:
      - Name or id of the security group.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
security_groups:
    description: List of dictionaries describing security groups.
    type: complex
    returned: On Success.
    contains:
        created_at:
            description: Creation time of the security group
            type: str
            sample: "yyyy-mm-dd hh:mm:ss"
        description:
            description: Description of the security group
            type: str
            sample: "My security group"
        id:
            description: ID of the security group
            type: str
            sample: "d90e55ba-23bd-4d97-b722-8cb6fb485d69"
        name:
            description: Name of the security group.
            type: str
            sample: "my-sg"
        project_id:
            description: Project ID where the security group is located in.
            type: str
            sample: "25d24fc8-d019-4a34-9fff-0a09fde6a567"
        security_group_rules:
            description: Specifies the security group rule list
            type: list
            sample: [
                {
                    "id": "d90e55ba-23bd-4d97-b722-8cb6fb485d69",
                    "direction": "ingress",
                    "protocol": null,
                    "ethertype": "IPv4",
                    "description": null,
                    "remote_group_id": "0431c9c5-1660-42e0-8a00-134bec7f03e2",
                    "remote_ip_prefix": null,
                    "tenant_id": "bbfe8c41dd034a07bebd592bf03b4b0c",
                    "port_range_max": null,
                    "port_range_min": null,
                    "security_group_id": "0431c9c5-1660-42e0-8a00-134bec7f03e2"
                },
                {
                    "id": "aecff4d4-9ce9-489c-86a3-803aedec65f7",
                    "direction": "egress",
                    "protocol": null,
                    "ethertype": "IPv4",
                    "description": null,
                    "remote_group_id": null,
                    "remote_ip_prefix": null,
                    "tenant_id": "bbfe8c41dd034a07bebd592bf03b4b0c",
                    "port_range_max": null,
                    "port_range_min": null,
                    "security_group_id": "0431c9c5-1660-42e0-8a00-134bec7f03e2"
                }
            ]
        updated_at:
            description: Update time of the security group
            type: str
            sample: "yyyy-mm-dd hh:mm:ss"
'''

EXAMPLES = '''
# Get specific security group
- opentelekomcloud.cloud.security_group_info:
    name: "{{ my_sg }}"
  register: sg

# Get all security groups
- opentelekomcloud.cloud.security_group_info:
  register: sg
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SecurityGroupInfoModule(OTCModule):
    argument_spec = dict(
        description=dict(required=False),
        name=dict(required=False),
        project_id=dict(required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        data = []
        query = {}

        if self.params['name']:
            sg = self.conn.network.find_security_group(
                name_or_id=self.params['name'],
                ignore_missing=True)
            if sg:
                query['id'] = sg.id
            else:
                self.exit(
                    changed=False,
                    security_groups=[],
                    message=('No security group found with name or id: %s' %
                             self.params['name'])
                )

        if self.params['description']:
            query['description'] = self.params['description']
        if self.params['project_id']:
            query['project_id'] = self.params['project_id']

        for raw in self.conn.network.security_groups(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            security_groups=data
        )


def main():
    module = SecurityGroupInfoModule()
    module()


if __name__ == "__main__":
    main()
