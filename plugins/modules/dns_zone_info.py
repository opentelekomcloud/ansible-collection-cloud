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
short_description: Get DNS Zone Infos
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get NAT gateway info from the OTC.
options:
  zone:
    description:
      - DNS Zone ID
    type: str
    required: true
  priority:
    description:
      - Priority of a name server
    type: str
  address:
    description:
      - IP address of a DNS Server
    type: str
  hostname:
    description:
      - Hostname of a DNS server
    type: str


requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
dns_zones:
    description: List of dictionaries describing NAT gateways.
    type: complex
    returned: On Success.
    contains:
        zone:
            description: Specifies the DNS zone
            type: str
            sample: "fe40808272701cbe0172cbca17f91882"
        priority:
            description: Priority of a name server
            type: str
            sample: "1"
        address:
            description: IP address of a DNS server
            type: str
            sample: "100.138.123.199"
        hostname:
            description: Hostname of a DNS server
            type: str
            sample: "Myhostname"
'''

EXAMPLES = '''
# Get configs versions.
- nat_gateway_info:
  register: gw

- nat_gateway_info:
    gateway: "my_gateway"
  register: gw

- nat_gateway_info:
    spec: "1"
  register: gw

- nat_gateway_info:
    status: "ACTIVE"
    spec: "1"
  register: gw

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSZoneInfoModule(OTCModule):
    argument_spec = dict(
        zone_type=dict(required=True),
        zone_id=dict(required=False),
        name=dict(required=False),
        status=dict(required=False),
        description=dict(required=False),
        email=dict(required=False),
        ttl=dict(required=False, type=int),
        serial=dict(required=False, type=int),
        record_num=dict(required=False, type=int),
        pool_id=dict(required=False),
        project_id=dict(required=False),
        created_at=dict(required=False),
        updated_at=dict(required=False),
        links=dict(required=False),
        routers=dict(required=False)
    )

    def run(self):

        data = []
        query = {}

        if self.params['zone_type']:
            query['zone_type'] = self.params['zone_type']

        for raw in self.conn.dns.zones(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        output = data

        i=0
        while i<len(data):
            if self.params['status']:
                if data[i]['status'] != self.params['status']:
                    del output[i]
                    i=0
                    continue
            if self.params['record_num']:
                if data[i]['record_num'] != self.params['record_num']:
                    del output[i]
                    i=0
                    continue
            if self.params['name']:
                if data[i]['name'] != self.params['name']:
                    del output[i]
                    i=0
                    continue
            if self.params['zone_id']:
                if data[i]['zone_id'] != self.params['zone_id']:
                    del output[i]
                    i=0
                    continue
            if self.params['description']:
                if data[i]['description'] != self.params['description']:
                    del output[i]
                    i=0
                    continue
            
            i=i+1

        self.exit(
            changed=False,
            dns_zones=data
        )


def main():
    module = DNSZoneInfoModule()
    module()


if __name__ == '__main__':
    main()
