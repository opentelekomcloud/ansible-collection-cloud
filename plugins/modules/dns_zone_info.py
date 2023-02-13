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
module: dns_zone_info
short_description: Get DNS Zones info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.13.1"
author: "Vladimir Vshivkov (@vladimirvshivkov)"
description:
    - Get DNS Zones info from the OTC.
options:
  name:
    description:
      - Zone Name
    type: str
    required: true
  zone_type:
    description:
      - Zone Type, either public or private
    type: str

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
zone:
  description: Modify DNS Zones
  type: complex
  returned: On Success.
  contains:
    description:
      description: Description of the Zone
      type: str
      sample: "MyZone123"
    email:
      description: assigned E-Mail of the Zone
      type: str
      sample: "mail@mail.com"
    id:
      description: Zone ID
      type: str
      sample: "fe80804323f2065d0175980e81617c10"
    name:
      description: Name of the zone
      type: str
      sample: "test.test2."
    router:
      description: Assigned VPC
      type: list
      sample: "[
        router_id: 79c32783-e560-4e3a-95b1-5a0756441e12,
        router_region: eu-de,
        status: PENDING_CREATE
        ]"
    status:
      description: Resource status
      type: str
      sample: "PENDING_CREATE"
    ttl:
      description: Cache duration (in second) on a local DNS server
      type: int
      sample: 300
    zone_type:
      description: Zone Type, either public or private
      type: str
      sample: "private"
'''

EXAMPLES = '''
# Get a Zone:
- name: Testing
  opentelekomcloud.cloud.dns_zone_info:
    name: "test.com."
    zone_type: private
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSZonesInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        zone_type=dict()
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        query = {
            'type': self.params['zone_type'],
            'name_or_id': self.params['name']
        }

        zone = self.conn.dns.find_zone(**query)
        self.exit(changed=True, zone=zone.to_dict())


def main():
    module = DNSZonesInfoModule()
    module()


if __name__ == '__main__':
    main()
