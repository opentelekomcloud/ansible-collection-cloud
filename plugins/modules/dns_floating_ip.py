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
module: dns_floating_ip
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


class DNSFloatingIpModule(OTCModule):
    argument_spec = dict(
        floating_ip=dict(required=True),
        ptrdname=dict(required=False),
        description=dict(required=False),
        ttl=dict(required=False, type='int'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )

    def run(self):
        changed = False
        data = []

        fl = self.conn.network.find_ip(
            name_or_id=self.params['floating_ip'],
            ignore_missing=True
        )
        if not fl:
            self.exit(
                changed=False,
                message=('No floating IP found with name or id: %s' %
                         self.params['floating_ip'])
            )
        if self.params['state'] == 'absent':
            changed = False
            # Set eu-de: in front of the id to comly with the API. Nothing else as eu-de is available currently
            self.conn.dns.unset_floating_ip(floating_ip = ('eu-de:' + fl.id))
            changed = True

        if self.params['state'] == 'present':
            attrs = {}
            if not self.params['ptrdname']:
              self.exit(
                changed=False,
                message=('No ptrdname specified but required for creation')
            )
            else:
              attrs['ptrdname'] = self.params['ptrdname']
            if self.params['description']:
              attrs['description'] = self.params['description']
            if self.params['ttl']:
              attrs['ttl'] = self.params['ttl']
            
            #get_floating_ip doesn't support ignore_missing and throws an error when there's nothing found. So we need to catch the error
            try:
              self.conn.dns.get_floating_ip(floating_ip = ('eu-de:' + fl.id))
            except:
              output = self.conn.dns.set_floating_ip(floating_ip = ('eu-de:' + fl.id), **attrs)
              self.exit(
                changed = True,
                ptr = output.to_dict()
              )
            else:
              output = self.conn.dns.update_floating_ip(floating_ip = ('eu-de:' + fl.id), **attrs)
              self.exit(
                changed = True,
                ptr = output.to_dict()
              )
              
        self.exit(
            changed=changed
        )


def main():
    module = DNSFloatingIpModule()
    module()


if __name__ == '__main__':
    main()
