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
module: dns_nameserver_info
short_description: Get info about DNS nameservers.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.12.2"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Get DNS nameservers info from the OTC.
options:
  zone:
    description:
      - ID or name of the required zone. If name had been provided, only public zone could be\
        returned. If private zone is required, only ID should be passed.
    type: str
    required: true
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
nameservers:
  description: List of dictionaries describing nameservers.
  type: complex
  returned: On Success.
  contains:
    hostname:
      description: Host name of a name server.
      type: str
      sample: "ns1.example.com."
    address:
      description: IP address of a DNS server (Private Zone only).
      type: str
      sample: "100.125.0.81"
    priority:
      description: Priority of a name server.
      type: int
'''

EXAMPLES = '''
#Get info about choosen DNS recordset.
- opentelekomcloud.cloud.dns_nameserver_info:
    zone: "ff80808275f5fc0f017e886898315ee9"
  register: nameservers
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSNameserverInfoModule(OTCModule):

    argument_spec = dict(
        zone=dict(required=True),
    )
    module_kwargs = dict(
        supports_check_mode=True,
    )

    def run(self):

        data = []
        query = {}

        if self.params['zone']:
            try:
                query['zone'] = self.conn.dns.find_zone(
                    name_or_id=self.params['zone'], ignore_missing=False).id
            except self.sdk.exceptions.ResourceNotFound:
                self.fail_json(msg="Zone not found")

        for raw in self.conn.dns.nameservers(**query):
            dt = raw.to_dict()
            dt.pop('location')
            dt.pop('name')
            dt.pop('id')
            data.append(dt)

        self.exit(
            changed=False,
            nameservers=data
        )


def main():
    module = DNSNameserverInfoModule()
    module()


if __name__ == '__main__':
    main()
