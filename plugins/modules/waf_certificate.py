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
module: waf_certificate
short_description: Manage WAF certificates
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Artem Goncharov (@gtema)"
description:
  - Manage WAF certificates.
options:
  name:
    description: Certificate name or ID
    type: str
    required: true
  content:
    description: Certificate content (line breaks must be as \n)
    type: str
    required: true
  key:
    description: Private key for the certificate (line breaks must be as \n)
    type: str
    required: true
  state:
    choices: [present, absent]
    default: present
    description: Certificate state
    type: str


requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
waf_certificate:
    description: Certificate data.
    type: complex
    returned: On Success.
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        name:
            description: Name of the certificate.
            type: str
            sample: "test"
'''

EXAMPLES = '''
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class WafCertificateModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True, type='str'),
        content=dict(type='str', no_log=True),
        key=dict(type='str', no_log=True),
        state=dict(type='str', choices=['present', 'absent'],
                   default='present')
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['content', 'key']),
        ]
    )

    otce_min_version = '0.8.0'

    def _system_state_change(self, obj):
        state = self.params['state']
        if state == 'present':
            if not obj:
                return True
        elif state == 'absent' and obj:
            return True
        return False

    def run(self):
        name = self.params['name']

        changed = False

        certificate = self.conn.waf.find_certificate(
            name_or_id=name)

        if self.ansible.check_mode:
            self.exit(changed=self._system_state_change(certificate))

        if self.params['state'] == 'absent':
            changed = False

            if certificate:
                self.conn.waf.delete_certificate(certificate)
                changed = True

            self.exit(changed=changed)

        elif self.params['state'] == 'present':

            if certificate:
                self.exit(changed=False)

            key = self.params['key'].strip()
            content = self.params['content'].strip()

            cert = self.conn.waf.create_certificate(
                name=self.params['name'],
                content=content,
                key=key)
            data = cert.to_dict()
            data.pop('location')
            data.pop('content')
            data.pop('key')
            self.exit(changed=True, waf_certificate=data)


def main():
    module = WafCertificateModule()
    module()


if __name__ == "__main__":
    main()
