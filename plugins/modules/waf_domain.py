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
module: waf_domain
short_description: Add/Modify/Delete WAF domain
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Add/Modify/Delete WAF domain from the OTC.
options:
  hostname:
    description: Specifies the domain name.
    type: str
  certificate_id:
    description: Specifies the certificate ID.
    type: str
  client_protocol:
    description: Protocol type of the client.
    type: str
  server_protocol:
    description: Protocol used by WAF to
     forward client requests to the server.
    type: str
  address:
    description: Public IP address or domain name
     of the web server that the client accesses
    type: str
  port:
    description: Port number used by the web server.
    type: int
  proxy:
    description: Specifies whether a proxy is configured.
    type: bool
    default: False
  sip_header_name:
    description: Specifies the type of the source IP header.
    type: str
  sip_header_list:
    description: Specifies the HTTP request header
     for identifying the real source IP address. 
    type: str
  state:
    description:
      - Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
waf_domain:
  description: List of dictionaries describing domains matching query.
  type: complex
  returned: On Success.
  contains:
    id:
      description: Specifies the instance ID.
      type: str
    hostname:
      description: Specifies the domain name.
      type: str
    cname:
      description: Specifies the CNAME value.
      type: str
      sample: "efec1196267b41c399f2980ea4048517.waf.cloud.com."
    policy_id:
      description: Specifies the policy ID.
      type: str
    protect_status:
      description: Specifies the WAF mode.
      type: int
    access_status:
      description: Specifies whether a domain name is connected to WAF.
      type: int
    protocol:
      description: Specifies the protocol type.
      type: str
    certificate_id:
      description: Specifies the certificate ID.
      type: str
    server:
      description: Specifies the origin server information.
      type: dict
    proxy:
      description: Specifies whether a proxy is configured.
      type: bool
    timestamp:
      description: Specifies the time when a domain name is created.
      type: str
'''

EXAMPLES = '''
# Create Domain.
- waf_domain:

# Modify Domain.
- waf_domain:
    instance_id: "id"
    client_protocol: HTTP
    server_protocol: HTTP
    address: 192.168.0.100
    port: 8888
  state: absent
  
# Delete Domain.
- waf_domain:
  state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class WafDomainModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
    )

    otce_min_version = '0.8.0'

    def run(self):

        data = []

        for raw in self.conn.waf.find_domain(offset=0, limit=-1):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            waf_domains=data
        )


def main():
    module = WafDomainModule()
    module()


if __name__ == '__main__':
    main()
