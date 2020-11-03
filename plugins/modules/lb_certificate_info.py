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
module: lb_certificate_info
short_description: Get elb certificate info from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Get Enhanced Load Balancer certificate from the OTC.
options:
  name:
    description:
      - Optional name or id of the certificate
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
elb_certificates:
  description: Dictionary describing certificates.
  type: complex
  returned: On Success.
  contains:
    id:
      description: Specifies the certificate ID.
      type: str
      sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
    name:
      description: Specifies the certificate name.
      type: str
      sample: "elb_test"
    description:
      description: Provides supplementary information about the certificate.
      type: str
    type:
      description: Specifies the certificate type.
      type: str
      sample: "server"
    domain:
      description: Specifies the domain name associated with the server certificate.
      type: str
      sample: "server.domain"
    private_key:
      description: Specifies the private key of the server certificate in PEM format.
      type: str
    certificate:
      description: Specifies the public key of the certificate used to authenticate the client.
      type: str
    create_time:
      description: Specifies the time when the certificate was created.
      type: str
    update_time:
      description: Specifies the time when the certificate was updated.
      type: str
'''

EXAMPLES = '''
# Get a lb certificate info.
- lb_certificate_info:
    state: present
    name: certificate-test
  register: lb_cert
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LoadBalancerCertificateInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False)
    )

    otce_min_version = '0.10.0'

    def run(self):
        data = []

        if self.params['name']:
            raw = self.conn.elb.find_certificate(name_or_id=self.params['name'], ignore_missing=True)
            if raw:
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)
        else:
            for raw in self.conn.elb.certificates():
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit_json(
            changed=False,
            elb_certificates=data
        )


def main():
    module = LoadBalancerCertificateInfoModule()
    module()


if __name__ == '__main__':
    main()
