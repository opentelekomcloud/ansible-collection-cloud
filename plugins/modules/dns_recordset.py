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
module: dns_recordset
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


class DNSRecordsetModule(OTCModule):
    argument_spec = dict(
        zone_id=dict(required=True),
        recordset_name=dict(required=True),
        description=dict(required=False),
        type=dict(required=False),
        ttl=dict(required=False, type='int'),
        records=dict(required=False, type='list'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )

    def run(self):
        changed = False
        data = []

        zo = self.conn.dns.find_zone(
            name_or_id = self.params['zone_id'],
            ignore_missing = True
        )
        if not zo:
            self.exit(
                changed=False,
                message=('No Zone found with name or id: %s' %
                         self.params['zone_id'])
            )
       
            
        if self.params['state'] == 'absent':
            changed = False
            rs = self.conn.dns.find_recordset(
                name_or_id = self.params['recordset_name'],
                zone = zo.id,
                ignore_missing = True
            )
            if not rs:
              self.exit(
                  changed=False,
                  message=('No Recordset found with name or id: %s' %
                           self.params['recordset_name'])
              )
            self.conn.dns.delete_recordset(
                recordset = rs.id,
                zone = zo.id
            )
            changed = True

        if self.params['state'] == 'present':
          attrs = {}
          attrs['name'] = self.params['recordset_name']
          if self.params['description']:
            attrs['description'] = self.params['description']
          if self.params['type']:
            attrs['type'] = self.params['type']
          else:
            self.exit(
                  changed=False,
                  message=('No type specified!')
              )
          if self.params['ttl']:
            attrs['ttl'] = self.params['ttl']
          if self.params['records']:
            attrs['records'] = []
            i = 0
            while i < len(self.params['records']):
              attrs['records'].append(self.params['records'][i])
              i = i+1
            # raise Exception(self.params['records'], len(self.params['records']), '    ', attrs['records'][1])
          else:
            self.exit(
                  changed=False,
                  message=('No records specified!')
              )

          rset = self.conn.dns.create_recordset(zone = zo.id , **attrs)
          self.exit(changed=True, rset=rset.to_dict())




        self.exit(
            changed=changed
        )


def main():
    module = DNSRecordsetModule()
    module()


if __name__ == '__main__':
    main()
