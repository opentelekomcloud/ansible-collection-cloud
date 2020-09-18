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
    description: Certificate name or ID.
    type: str
    required: true
  content:
    description: Certificate content. Required for creation.
    type: str
  private_key:
    description: Private key for the certificate. Required for creation.
    type: str
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
        expire_time:
            description: Expiration timestamp
            type: int
            sample: 1630488473000
        timestamp:
            description: Certificate creation time
            type: int
            sample: 1630488473000
'''

EXAMPLES = '''
'''

import os
from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class WafCertificateModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True, type='str'),
        content=dict(type='str', no_log=False),
        private_key=dict(type='str', no_log=False),
        state=dict(type='str', choices=['present', 'absent'],
                   default='present')
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['content', 'private_key']),
        ]
    )

    otce_min_version = '0.8.0'

    @staticmethod
    def _is_path(path):
        if os.path.isfile(path):
            return True
        return False

    @staticmethod
    def _read_content(path):
        with open(path, 'r') as file:
            content = file.read()
        return content

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
            private_key_filter = self.params['private_key'].strip()
            content_filter = self.params['content'].strip()

            if certificate:
                self.exit(changed=False)

            if self._is_path(private_key_filter):
                self.fail_json(msg='read: %s' % self._read_content(private_key_filter))
                key = self._read_content(private_key_filter)
            else:
                key = private_key_filter

            if self._is_path(content_filter):
                content = self._read_content(content_filter)
            else:
                content = content_filter

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
