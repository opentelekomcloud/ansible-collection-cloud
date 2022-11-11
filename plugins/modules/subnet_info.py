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
module: subnet_info
short_description: Get subnet info from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.11.1"
author: "Polina Gubina(@polina-gubina)"
description:
  - Get subnet from the OTC.
options:
  name_or_id:
    description:
      - Name or id of the subnet.
    type: str
  vpc:
    description:
      - Name or id of the vpc subnets should be listed within.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
subnets:
  description: Dictionary describing subnets.
  type: complex
  returned: On Success.
  contains:
    id:
      description: Specifies the ID of the subnet.
      type: str
    name:
      description: Specifies the subnets name.
      type: str
    description:
      description: Provides supplementary information about the subnet.
      type: str
    cidr:
      description: Specifies the subnet CIDR block.
      type: str
    gateway_ip:
      description: Specifies the subnet gateway address.
      type: str
    dhcp_enable:
      description: Specifies whether the DHCP function is enabled for the subnet.
      type: bool
    primary_dns:
      description: Specifies the IP address of DNS server 1 on the subnet.
      type: str
    secondary_dns:
      description: Specifies the IP address of DNS server 2 on the subnet.
      type: str
    dnsList:
      description: Specifies the IP address list of DNS servers on the subnet.
      type: list
    availability_zone:
      description: Identifies the AZ to which the subnet belongs.
      type: str
    vpc_id:
      description: Specifies the ID of the VPC to which the subnet belongs.
      type: str
    status:
      description: Specifies the status of the subnet.
      type: str
    neutron_network_id:
      description: Specifies the ID of the corresponding network (OpenStack Neutron API).
      type: str
    neutron_subnet_id:
      description: Specifies the ID of the corresponding subnet (OpenStack Neutron API).
      type: str
    extra_dhcp_opts:
      description: Specifies the NTP server address configured for the subnet.
      type: list
      elements: dict
      contains:
        opt_value:
          description: Specifies the NTP server address configured for the subnet.
          type: str
        opt_name:
          description: Specifies the NTP server address name configured for the subnet.
          type: str
'''

EXAMPLES = '''
# Get all subnets
- opentelekomcloud.cloud.subnet_info:
  register: subnet_info
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SubnetInfoModule(OTCModule):
    argument_spec = dict(
        name_or_id=dict(required=False),
        vpc=dict(required=False)
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        data = []

        if self.params['name_or_id']:
            raw = self.conn.vpc.find_subnet(name_or_id=self.params['name_or_id'])
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)
        else:
            query = {}
            if self.params['vpc']:
                vpc = self.conn.vpc.find_vpc(name_or_id=self.params['vpc'])
                query['vpc_id'] = vpc.id
            for raw in self.conn.vpc.subnets(**query):
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit_json(
            changed=False,
            subnets=data
        )


def main():
    module = SubnetInfoModule()
    module()


if __name__ == '__main__':
    main()
