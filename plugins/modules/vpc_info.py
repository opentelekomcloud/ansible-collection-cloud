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
module: vpc_info
short_description: Get vpc info from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.11.1"
author: "Polina Gubina(@polina-gubina)"
description:
  - Get vpc from the OTC.
options:
  name_or_id:
    description:
      - Name or id of the vpc.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
vpcs:
  description: Dictionary describing vpcs.
  type: complex
  returned: On Success.
  contains:
    id:
      description: Specifies the ID of the vpc.
      type: str
      sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
    name:
      description: Specifies the vpc name.
      type: str
      sample: "vpc-test"
    description:
      description: Provides supplementary information about the vpc.
      type: str
      sample: "vpc for testing"
    cidr:
      description: Specifies the available IP address ranges for subnets in the VPC.
      type: str
      sample: "10.0.0.0/8"
    status:
      description: Specifies the VPC status.
      type: str
      sample: "CREATING"
    routes:
      description: Specifies the route information.
      type: list
    enable_shared_snat:
      description: Specifies whether the shared SNAT function is enabled. The value true\
       indicates that the function is enabled, and the value false indicates that the function is not enabled.
      type: bool
'''

EXAMPLES = '''
# Get all vpcs
- opentelekomcloud.cloud.vpc_info:
  register: vpc_info
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VpcInfoModule(OTCModule):
    argument_spec = dict(
        name_or_id=dict(required=False)
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        data = []

        if self.params['name_or_id']:
            raw = self.conn.vpc.find_vpc(name_or_id=self.params['name_or_id'])
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)
        else:
            for raw in self.conn.vpc.vpcs():
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit_json(
            changed=False,
            vpcs=data
        )


def main():
    module = VpcInfoModule()
    module()


if __name__ == '__main__':
    main()
