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
module: server_group_info
short_description: Lists server groups
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.5.0"
author: "Tino Schreiber (@tischrei)"
description:
  - List server groups
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
server_groups:
    description: List of dictionaries describing server groups.
    type: complex
    returned: On Success.
    contains:
        id:
            description: ID of the server group
            type: str
            sample: "d90e55ba-23bd-4d97-b722-8cb6fb485d69"
        member_ids:
            description: The list of members in the server group
            type: list
            elements: str
        metadata:
            description: The metadata associated with the server group
            type: str
        name:
            description: Name of the server group.
            type: str
            sample: "my-sg"
        policies:
            description: The list of policies supported by the server group
            type: list
            elements: str
        policy:
            description: The policy field represents the name of the policy
            type: str
        project_id:
            description: The project ID who owns the server group
            type: str
            sample: "d90e55ba-23bd-4d97-b722-8cb6fb485d69"
        rules:
            description: The rules, which is a dict, can be applied to the policy
            type: list
            elements: dict
        user_id:
            description: The user ID who owns the server group
            type: str
            sample: "d90e55ba-23bd-4d97-b722-8cb6fb485d69"
'''

EXAMPLES = '''
# Get all server groups of a project
- opentelekomcloud.cloud.server_group_info:
  register: server_groups
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class ServerGroupInfoModule(OTCModule):
    argument_spec = {}
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        data = []

        for raw in self.conn.compute.server_groups():
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            server_groups=data
        )


def main():
    module = ServerGroupInfoModule()
    module()


if __name__ == "__main__":
    main()
