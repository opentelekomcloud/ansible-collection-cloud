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
      - Description of the Zone
    type: str
  email:
    description:
      - E-Mail Address
    type: str
  name:
    description:
      - Zone Name
    type: str
    required: true
  router:
    description:
      - VPC ID or name, required when creating an private Zone
    type: str
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
  zone_type:
    description:
      - Zone Type, either public or private
    type: str
    choices: [public, private]
    default: public

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
zone:
    description: Modfiy DNS Zones
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
# Creating / Updating a Zone:
- name: Testing
  opentelekomcloud.cloud.dns_zones:
    name: "test.com."
    state: present
    zone_type: private
    router: 79c32783-e560-4e3a-95b1-5a0756441e12
    description: test2
    ttl: 5000
    email: mail2@mail2.test


'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSZonesModule(OTCModule):
    argument_spec = dict(
        description=dict(required=False),
        email=dict(required=False),
        name=dict(required=True),
        router=dict(required=False),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        ttl=dict(required=False, type='int'),
        zone_type=dict(type='str', choices=['public', 'private'], default='public')
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
                zone_check = True
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
                i = i + 1
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

            if zone_check is False:
                # Check if VPC exists
                if self.params['zone_type'] == 'private':
                    ro = self.conn.network.find_router(
                        name_or_id=self.params['router'],
                        ignore_missing=True
                    )
                    if ro:
                        # Somehow the API wants a dict with router_id in it
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

            if zone_check is True:
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
