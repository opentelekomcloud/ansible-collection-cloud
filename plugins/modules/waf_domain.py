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
  name:
    description: Specifies the domain name.
    required: true
    type: str
  certificate:
    description: Specifies the certificate.
    type: str
  server:
    description: Specifies the origin server information.
    type: list
    elements: dict
  proxy:
    description: Specifies whether a proxy is configured.
    type: bool
  sip_header_name:
    description: Specifies the type of the source IP header.
    choices: [default, cloudflare, akamai, custom]
    type: str
  sip_header_list:
    description: Specifies the HTTP request header
     for identifying the real source IP address.
    type: list
    elements: str
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
    name: test.domain.name
    server: [
      {
        client_protocol: HTTP,
        server_protocol: HTTP,
        address: 192.168.0.100,
        port: 8888
      }
    ]
  state: absent

# Delete Domain.
- waf_domain:
  state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class WafDomainModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True, type='str'),
        certificate=dict(required=False),
        server=dict(required=False, type='list', elements='dict'),
        proxy=dict(required=False, type='bool'),
        sip_header_name=dict(required=False, choices=['default', 'cloudflare', 'akamai', 'custom']),
        sip_header_list=dict(required=False, type='list', elements='str'),
        state=dict(default='present', choices=['absent', 'present']),
    )

    otce_min_version = '0.9.0'

    def _system_state_change(self, domain):
        state = self.params['state']
        if state == 'present':
            if not domain:
                return True
        elif state == 'absent' and domain:
            return True
        return False

    def _check_server_client_protocol(self, server: list):
        for srv in server:
            if srv['client_protocol'] == 'HTTPS':
                return True
        return False

    def run(self):
        name_filter = self.params['name']

        domain = None
        changed = False

        domain = self.conn.waf.find_domain(name_or_id=name_filter)

        if self.params['state'] == 'absent':
            changed = False

            if domain:
                self.conn.waf.delete_domain(domain)
                changed = True

        elif self.params['state'] == 'present':
            query = {}
            certificate_filter = self.params['certificate']
            server_filter = self.params['server']
            proxy_filter = self.params['proxy']
            sip_header_name_filter = self.params['sip_header_name']
            sip_header_list_filter = self.params['sip_header_list']

            if name_filter:
                query['name'] = name_filter

            if certificate_filter:
                try:
                    res = self.conn.waf.find_certificate(name_or_id=certificate_filter)
                    query['certificate_id'] = res.id
                except self.sdk.exceptions.ResourceNotFound:
                    self.fail_json(msg='certificate not found.')

            if server_filter:
                for srv in server_filter:
                    srv['client_protocol'] = srv['client_protocol'].upper()
                    srv['server_protocol'] = srv['server_protocol'].upper()
                if self._check_server_client_protocol(server_filter):
                    if not certificate_filter:
                        self.fail_json(msg='certificate should by specified'
                                           ' when client_protocol is equal to HTTPS.')
                query['server'] = server_filter
            if not server_filter and not domain:
                self.fail_json(msg='server should by specified when state is set to present.')

            if proxy_filter:
                query['proxy'] = proxy_filter
                if not sip_header_name_filter and not sip_header_list_filter:
                    self.fail_json(msg='sip_header_name and sip_header_list'
                                       ' should by specified when proxy is set to true.')
                else:
                    query['sip_header_name'] = sip_header_name_filter
                    query['sip_header_list'] = sip_header_list_filter
            if not proxy_filter and not domain:
                self.fail_json(msg='proxy should by specified when state is set to present.')

            if domain:
                # check attrs
                if certificate_filter:
                    if domain.certificate.id != query['certificate_id']:
                        domain = self.conn.waf.update_domain(domain, **query)
                self.exit(
                    changed=True,
                    waf_domain=domain.to_dict()
                )

            domain = self.conn.waf.create_domain(**query)
            self.exit(
                changed=True,
                waf_domain=domain.to_dict()
            )

        self.exit(changed=changed)


def main():
    module = WafDomainModule()
    module()


if __name__ == '__main__':
    main()
