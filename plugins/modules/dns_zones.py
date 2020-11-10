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
module: dns_zones
short_description: Get DNS PTR Records
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
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
zone:
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


class DNSZonesModule(OTCModule):
    argument_spec = dict(
        description=dict(required=False),
        email=dict(required=False),
        name=dict(required=True),
        router_id=dict(required=False),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        ttl=dict(required=False, type='int'),
        zone_type=dict(required=True)
    )

    def run(self):
        changed = False
        data = []
        query = {}

        # find_zone doesn't support searching for private zones with name
        # As a result we use it only to search in public zones
        if self.params['zone_type'] == 'public':
            zo = self.conn.dns.find_zone(
                name_or_id=self.params['name'],
                ignore_missing=True
            )
            if zo:
                zone_id = zo.id
                zone_ceck = True
            else:
                zone_check = False
                if self.params['state'] == 'absent':
                    self.exit(
                        changed=False,
                        message=('No Zone found with name: %s' %
                                self.params['name'])
                    )


        # For private Zones we list all zones and then filter by name
        if self.params['zone_type'] == 'private':
            query['zone_type'] = self.params['zone_type']
            for raw in self.conn.dns.zones(**query):
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)
            # Query parameter name is not supported, so we need to filter it by hand
            i = 0
            while i < len(data):
                if data[i]['name'] != self.params['name']:
                    del data[i]
                    i = 0
                    continue
                i = i+1
            # As we remove datasets we need to check wether there's the correct one left to obtain the ID
            if len(data) != 0:    
                zone_id = data[0]['id']
                zone_check = True
            else:
                zone_check = False
                if self.params['state'] == 'absent':
                    self.exit(
                        changed=False,
                        message=('No Zone found with name: %s' %
                                self.params['name'])
                    )

        # We now have the zone_id to work with
        if self.params['state'] == 'absent':
            changed = False
            # No check for zone_id necessary as we checked it
            self.conn.dns.delete_zone(
                zone=zone_id
            )
            changed = True

        if self.params['state'] == 'present':
            attrs = {}
            changed = False

            if zone_check == False:
                # Check if VPC exists
                if self.params['zone_type'] == 'private':
                    ro = self.conn.network.find_router(
                        name_or_id=self.params['router_id'],
                        ignore_missing=True
                    )
                    if ro: 
                        # Somehow the API wants a dict wiuth router_id in it
                        routerdict = {
                            'router_id': ro.id
                        }
                        attrs['router'] = routerdict
                    else:
                        self.exit(
                        changed=False,
                        message=('No Router found with name or id: %s' %
                                self.params['router'])
                    )
                attrs['zone_type'] = self.params['zone_type']
                if self.params['description']:
                    attrs['description'] = self.params['description']
                if self.params['email']:
                    attrs['email'] = self.params['email']
                if self.params['ttl']:
                    attrs['ttl'] = self.params['ttl']
                attrs['name'] = self.params['name']

                zone = self.conn.dns.create_zone(**attrs)
                self.exit(changed=True, zone=zone.to_dict())

            if zone_check == True:
                if self.params['description']:
                    attrs['description'] = self.params['description']
                if self.params['email']:
                    attrs['email'] = self.params['email']
                if self.params['ttl']:
                    attrs['ttl'] = self.params['ttl']
                attrs['zone'] = zone_id

                zone = self.conn.dns.update_zone(**attrs)
                self.exit(changed=True, zone=zone.to_dict())

def main():
    module = DNSZonesModule()
    module()

if __name__ == '__main__':
    main()
