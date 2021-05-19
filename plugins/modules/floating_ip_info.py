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
module: floating_ip_info
short_description: Get information about floating ips
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.1"
author: "Polina Gubina (@Polina-Gubina)"
description:
  - Get a generator of floating ips info from the OTC.
options:
  description:
    description:
      - The description of a floating IP.
    type: str
  fixed_ip_address:
    description:
      - The fixed IP address associated with a floating IP address.
    type: str
  floating_ip_address:
    description:
      -  The IP address of a floating IP.
    type: str
  floating_network:
    description:
      - The name or id of the network associated with a floating IP.
    type: str
  port:
    description:
      - The name or id of the port to which a floating IP is associated.
    type: str
  project_id:
    description:
      - The ID of the project a floating IP is associated with.
    type: str
  vpc:
    description:
      - The name or id of an associated vpc.
    type: str
  status:
    description:
      - The status of a floating IP, which can be ``ACTIVE``or ``DOWN``.
    choices: ['ACTIVE', 'DOWN']
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
floating_ips:
  description: The VPC peering connection object list.
  type: complex
  returned: On Success.
  contains:
    created_at:
      description: Creation time of the floating ip.
      type: str
      sample: "2020-09-30T09:59:01Z"
    description:
      description: The description of a floating IP.
      type: str
      sample: "The description"
    dns_domain:
      description: The DNS domain.
      type: str
      sample: str
    dns_name:
      description: The DNS name.
      type: str
      sample: "{tenant_id: 76889f64a23945ab887012be95acf, vpc_id: 4dae5bac-0925-4d5b-add8-cb6667b8}"
    fixed_ip_address:
      description: The fixed IP address associated with a floating IP address.
      type: dict
      sample: str
    floating_ip_address:
      description: The IP address of a floating IP.
      type: str
      sample: ""
    floating_network_id:
      description: The id of the network associated with a floating IP.
      type: str
      sample: "76889f64a23945ab887012be95acf"
    id:
      description: Id of the floating ip.
      type: str
      sample: "99089f64a23945ab887012be95acf"
    name:
      description: Name of the floating ip.
      type: str
      sample: ""
    port_details:
      description: The details of the port that this floating IP associates \
        with. Present if ``fip-port-details`` extension is loaded.
      type: str
      sample: ""
    port_id:
      description: The port ID.
      type: str
      sample: "76889f64a23945ab887012be95acf"
    project_id:
      description: The ID of the project this floating IP is associated with.
      type: str
      sample: "34289f64a23945ab887012be95acf"
    qos_policy_id:
      description: The ID of the QoS policy attached to the floating IP.
      type: str
      sample: "76889f64a23945ab887012be95acf"
    revision_number:
      description: Revision number.
      type: str
      sample: ""
    router_id:
      description: The id of an associated router.
      type: str
      sample: "76889f64a23945ab887012be95acf"
    status:
      description: The status of a floating IP, which can be ``ACTIVE``or ``DOWN``.\
        Can be 'ACTIVE' and 'DOWN'.
      type: str
      sample: "ACTIVE"
    subnet_id:
      description: The id of the subnet the floating ip associated with.
      type: str
      sample: "76889f64a23945ab887012be95acf"
    tags:
      description: List of tags.
      type: str
      sample: 
    updated_at:
      description: Timestamp at which the floating IP was last updated.
      type: str
      sample: "2020-09-13T20:37:01"
'''

EXAMPLES = '''
# 
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class FloatingIPInfoModule(OTCModule):
    argument_spec = dict(
        description=dict(required=False),
        fixed_ip_address=dict(required=False),
        floating_ip_address=dict(required=False),
        floating_network=dict(required=False),
        port=dict(required=False),
        project_id=dict(required=False),
        vpc=dict(required=False),
        status=dict(required=False, choices=['ACTIVE', 'DOWN']),
    )

    def run(self):

        description = self.params['description']
        fixed_ip_address = self.params['fixed_ip_address']
        floating_ip_address = self.params['floating_ip_address']
        floating_network = self.params['floating_network']
        port = self.params['port']
        project_id = self.params['project_id']
        vpc = self.params['vpc']
        status = self.params['status']

        data = []
        query = {}
        if description:
            query['description'] = description
        if fixed_ip_address:
            query['fixed_ip_address'] = fixed_ip_address
        if floating_ip_address:
            query['floating_ip_address'] = floating_ip_address
        if floating_network:
            try:
                query['floating_network_id'] = self.conn.network.find_network(name_or_id=floating_network,\
                                                                              ignore_missing=False).id
            except self.sdk.exceptions.ResourceNotFound:
                self.fail_json(msg="floating_network not found")
        if port:
            try:
                query['port_id'] = self.conn.network.find_port(name_or_id=port, ignore_missing=False).id
            except self.sdk.exceptions.ResourceNotFound:
                self.fail_json(msg="port not found")
        if project_id:
            query['project_id'] = project_id
        if vpc:
            try:
                query['router_id'] = self.conn.network.find_router(name_or_id=vpc, ignore_missing=False).id
            except self.sdk.exceptions.ResourceNotFound:
                self.fail_json(msg="vpc not found")
        if status:
            query['status'] = status

        for raw in self.conn.network.ips(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit_json(
            changed=False,
            floating_ips=data
        )


def main():
    module = FloatingIPInfoModule()
    module()


if __name__ == '__main__':
    main()
