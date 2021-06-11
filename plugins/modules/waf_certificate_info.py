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
module: waf_certificate_info
short_description: Get WAF certificate info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Artem Goncharov (@gtema)"
description:
  - Get WAF Certificate info from the OTC or list all certificates.
options:
  name:
    description:
      - Name or ID of the certificate.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
waf_certificate_info:
    description: List of dictionaries describing Certificates matching query.
    type: complex
    returned: On Success.
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        name:
            description: Certificate name
            type: str
        timestamp:
            description: Certificate upload timestamp
            type: int
        expire_time:
            description: Expiration timestamp
            type: int
'''

EXAMPLES = '''
# Get Certificates.
- waf_certificate_info:
  register: cert
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class WafCertificateInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    otce_min_version = '0.8.0'

    def run(self):

        data = []

        if self.params['name']:
            raw = self.conn.waf.find_certificate(
                self.params['name'], ignore_missing=True)
            if raw:
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)
        else:
            for raw in self.conn.waf.certificates():
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit(
            changed=False,
            waf_certificates=data
        )


def main():
    module = WafCertificateInfoModule()
    module()


if __name__ == '__main__':
    main()
