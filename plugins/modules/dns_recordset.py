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
  description:
    description:
      - Description of the Record
    type: str
  records:
    description:
      - IP Records of the entry. Type is a list
    type: list
    elements: str
    required: true
  recordset_name:
    description:
      - Can be name or ID of the recordset. When creating a new one please enter a name
    type: str
    required: true
  state:
    description:
      - State, either absent or present
    type: str
    choices: [present, absent]
    default: present
  ttl:
    description:
      - Cache duration (in second) on a local DNS server
    type: int
  type:
    description:
      - Record set type
    type: str
  zone_id:
    description:
      - Zone ID of the recordset
    type: str
    required: true

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
recordset:
    description: Get DNS PTR Records
    type: complex
    returned: On Success.
    contains:
        description:
            description: Description of the Record
            type: str
            sample: "MyRecord123"
        id:
            description: ID
            type: str
            sample: "fe80804323f2065d0175980e81617c10"
        records:
            description: IP Records of the entry. Type is a list
            type: str
            sample: "[
                1.3.1.2,
                121.111.111.111,
                145.145.145.145
            ]"
        name:
            description: Name
            type: str
            sample: "test.test2."
        status:
            description: Resource status
            type: str
            sample: "ACTIVE"
        ttl:
            description: Cache duration (in second) on a local DNS server
            type: int
            sample: 300
        type:
            description: Recordset Type
            type: str
            sample: "A"
        zone_name:
            description: Zone Name
            type: str
            sample: "test."

'''

EXAMPLES = '''
# Creating / Updating a recordset:
- name: Testing
  opentelekomcloud.cloud.dns_recordset:
    zone_id: fe80829272374c340174d8e94bb9562c
    recordset_name: "test.test2."
    state: present
    ttl: 400
    type: A
    records:
      - "1.3.1.2"
      - "121.111.111.111"
      - "145.145.145.145"

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSRecordsetModule(OTCModule):
    argument_spec = dict(
        description=dict(required=False),
        records=dict(required=True, type='list', elements='str'),
        recordset_name=dict(required=True),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        ttl=dict(required=False, type='int'),
        type=dict(required=False),
        zone_id=dict(required=True)
    )

    def run(self):
        changed = False
        data = []

        zo = self.conn.dns.find_zone(
            name_or_id=self.params['zone_id'],
            ignore_missing=True
        )
        if not zo:
            self.exit(
                changed=False,
                failed=True,
                message=('No Zone found with name or id: %s' %
                         self.params['zone_id'])
            )

        rs = self.conn.dns.find_recordset(
            name_or_id=self.params['recordset_name'],
            zone=zo.id,
            ignore_missing=True
        )

        # recordset deletion
        if self.params['state'] == 'absent':
            changed = False
            if rs:
                self.conn.dns.delete_recordset(
                    recordset=rs.id,
                    zone=zo.id
                )
                changed = True

        if self.params['state'] == 'present':
            attrs = {}

            # Modify recordset
            if rs:
                if self.params['records']:
                    for item in self.params['records']:
                        if item not in rs.records:
                            # user is intended to overwrite whole recordset
                            attrs['records'] = self.params['records']
                            break

                if self.params['description'] and (self.params['description'] != rs.description):
                    attrs['description'] = self.params['description']
                if self.params['ttl'] and (self.params['ttl'] != rs.ttl):
                    attrs['ttl'] = self.params['ttl']

                if attrs:
                    attrs['recordset'] = rs.id
                    attrs['zone_id'] = zo.id
                    recordset = self.conn.dns.update_recordset(**attrs)
                    self.exit(changed=True, recordset=recordset.to_dict())

            # create recordset
            if not rs:
                attrs['name'] = self.params['recordset_name']
                if self.params['description']:
                    attrs['description'] = self.params['description']
                if self.params['type']:
                    attrs['type'] = self.params['type']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('Type is mandatory for recordset creation')
                    )
                if self.params['ttl']:
                    attrs['ttl'] = self.params['ttl']
                if self.params['records']:
                    attrs['records'] = self.params['records']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No records specified for recordset '
                                 'creation.')
                    )

                rset = self.conn.dns.create_recordset(zone=zo.id, **attrs)
                self.exit(changed=True, recordset=rset.to_dict())

        self.exit(
            changed=changed
        )


def main():
    module = DNSRecordsetModule()
    module()


if __name__ == '__main__':
    main()
