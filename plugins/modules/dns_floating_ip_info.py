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
module: dns_floating_ip_info
short_description: Get DNS PTR Records
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Get DNS PTR Records from the OTC.
options:
  address:
    description:
      - EIP address
    type: str
  description:
    description:
      - Description of the Record
    type: str
  id:
    description:
      - PTR record ID
    type: str
  ptrdname:
    description:
      - Domain name of the PTR record
    type: str
  status:
    description:
      - Resource status
    type: str
  ttl:
    description:
      - PTR record cache duration (in second) on a local DNS server
    type: int

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
ptr_records:
    description: Get DNS PTR Records
    type: complex
    returned: On Success.
    contains:
        address:
            description: EIP address
            type: str
            sample: "100.138.123.199"
        description:
            description: Description of the Record
            type: str
            sample: "MyRecord123"
        id:
            description: PTR record id
            type: str
            sample: "eu-de:fe864230-d3bc-4391-8a32-394c3e9ca22d"
        ptrdname:
            description: Domain name of the PTR record
            type: str
            sample: "example.com"
        status:
            description: Resource status
            type: str
            sample: "ACTIVE"
        ttl:
            description: PTR record cache duration (in second) on a local DNS server
            type: int
            sample: 300

'''

EXAMPLES = '''
# Get Nameserver Info about a zone:
- name: Getting Info
  dns_floating_ip_info:
    description: "Test"

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSFloatingIpInfoModule(OTCModule):
    argument_spec = dict(
        address=dict(required=False),
        description=dict(required=False),
        id=dict(required=False),
        ptrdname=dict(required=False),
        status=dict(required=False),
        ttl=dict(required=False, type='int')
    )

    def run(self):

        data = []

        for raw in self.conn.dns.floating_ips():
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        # Filter data by deleting all entries without the right criteria
        i = 0
        while i < len(data):
            if self.params['address']:
                if data[i]['address'] != self.params['address']:
                    del data[i]
                    i = 0
                    continue
            if self.params['id']:
                if data[i]['id'] != self.params['id']:
                    del data[i]
                    i = 0
                    continue
            if self.params['ptrdname']:
                if data[i]['ptrdname'] != self.params['ptrdname']:
                    del data[i]
                    i = 0
                    continue
            if self.params['ttl']:
                if data[i]['ttl'] != self.params['ttl']:
                    del data[i]
                    i = 0
                    continue
            if self.params['description']:
                if data[i]['description'] != self.params['description']:
                    del data[i]
                    i = 0
                    continue
            if self.params['status']:
                if data[i]['status'] != self.params['status']:
                    del data[i]
                    i = 0
                    continue
            i = i + 1

        self.exit(
            changed=False,
            ptr_records=data
        )


def main():
    module = DNSFloatingIpInfoModule()
    module()


if __name__ == '__main__':
    main()
