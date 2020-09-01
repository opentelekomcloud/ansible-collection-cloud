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
module: nat_gateway_info
short_description: Get NAT gateways
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Tino Schreiber (@tischrei)"
description:
  - Get NAT gateway info from the OTC.
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
as_configs:
    description: List of dictionaries describing NAT gateways.
    type: complex
    returned: On Success.
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        name:
            description: Name (version) of the datastore.
            type: str
            sample: "10.0"
'''

EXAMPLES = '''
# Get configs versions.
- nat_gateway_info:
  register: gw

- as_config_info:
    name: my_gateway
  register: gw
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class NATGatewayInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
        id=dict(required=False),
        admin_state_up=dict(required=False),
        created_at=dict(required=False),
        description=dict(required=False),
        internal_network_id=dict(required=False),
        router_id=dict(required=False),
        spec=dict(required=False),
        status=dict(required=False),
        project_id=dict(required=False)
    )

    def run(self):
        name_filter = self.params['name']
        id_filter = self.params['id']
        admin_state_up_filter = self.params['admin_state_up']
        created_at_filter = self.params['created_at']
        description_filter = self.params['description']
        internal_network_id_filter = self.params['internal_network_id']
        router_id_filter = self.params['router_id']
        spec_filter = self.params['spec']
        status_filter = self.params['status']
        project_id_filter = self.params['project_id']

        data = []

        for raw in self.conn.nat.gateways():
            if (name_filter and raw.name != name_filter):
                continue
            if (id_filter and raw.id != id_filter):
                continue
            if ((admin_state_up_filter and not raw.admin_state_up) or
                    (not admin_state_up_filter and raw.admin_state_up)):
                continue
            if (created_at_filter and raw.created_at != created_at_filter):
                continue
            if (description_filter and raw.description
                    != description_filter):
                continue
            if (internal_network_id_filter and raw.internal_network_id
                    != internal_network_id_filter):
                continue
            if (router_id_filter and raw.router_id != router_id_filter):
                continue
            if (spec_filter and raw.spec != spec_filter):
                continue
            if (status_filter and raw.status != status_filter):
                continue
            if (project_id_filter and raw.project_id != project_id_filter):
                continue
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            nat_gateways=data
        )


def main():
    module = NATGatewayInfoModule()
    module()


if __name__ == '__main__':
    main()
