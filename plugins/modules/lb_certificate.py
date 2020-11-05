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
module: lb_certificate
short_description: Manage ELB certificates
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Manage ELB certificates.
options:
  name:
    description: Certificate name or ID.
    type: str
    required: true
  admin_state_up:
    description: Specifies the administrative status of the certificate.
    type: bool
  description:
    description: Provides supplementary information about the certificate.
    type: str
  type:
    description: Specifies the certificate type.
    choices: [server, client]
    type: str
  domain:
    description: Specifies the domain name associated with the server certificate.
    type: str
  certificate:
    description: Certificate content or path to file with content. Required for creation.
    type: str
  private_key:
    description: Private key for the certificate or path to file with key. Required for creation.
    type: str
  state:
    choices: [present, absent]
    default: present
    description: Certificate state
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
elb_certificate:
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
        admin_state_up:
            description: Administrative status of the certificate.
            type: bool
        description:
            description: Supplementary information about the certificate.
            type: str
        type:
            description: Certificate type.
            type: str
        domain:
            description: Domain name associated with the server certificate.
            type: str
        private_key:
            description: Private key of the server certificate in PEM format.
            type: str
        certificate:
            description: Public key of the server certificate or CA certificate used to authenticate the client.
            type: str
        expire_time:
            description: Expiration timestamp
            type: int
            sample: 1630488473000
        create_time:
            description: Certificate creation time
            type: int
            sample: 1630488473000
        update_time:
            description: Certificate update time
            type: int
            sample: 1630488473000
'''

EXAMPLES = '''
# Create lb certificate.
- lb_certificate:
    state: present
    name: certificate-test
    certificate: {{ dummy-cert }}
    type: client
  register: lb_cert
'''

import os

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LoadBalancerCertificateModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True, type='str'),
        certificate=dict(type='str', no_log=True),
        private_key=dict(type='str', no_log=True),
        admin_state_up=dict(type='str'),
        description=dict(type='str'),
        type=dict(type='str', choices=['server', 'client'], default='server'),
        domain=dict(type='str', default=None),
        state=dict(type='str', choices=['present', 'absent'],
                   default='present')
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['content', 'private_key']),
        ]
    )

    otce_min_version = '0.10.0'

    @staticmethod
    def _is_path(path):
        if os.path.isfile(path):
            return True
        return False

    @staticmethod
    def _read_content(path):
        with open(path, 'r') as file:
            content = file.read()
        return content.strip()

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
        attrs = {}
        certificate = self.conn.elb.find_certificate(
            name_or_id=name)

        if self.ansible.check_mode:
            self.exit(changed=self._system_state_change(certificate))

        if self.params['state'] == 'absent':
            changed = False

            if certificate:
                self.conn.elb.delete_certificate(certificate)
                changed = True

            self.exit(changed=changed)

        elif self.params['state'] == 'present':
            name_filter = self.params['name']
            admin_state_filter = self.params['admin_state_up']
            description_filter = self.params['description']
            type_filter = self.params['type']
            domain_filter = self.params['domain']
            private_key_filter = self.params['private_key'].strip()
            certificate_filter = self.params['certificate'].strip()

            if name_filter:
                attrs['name'] = name_filter
            if type_filter:
                attrs['type'] = type_filter
            if admin_state_filter:
                attrs['admin_state_up'] = admin_state_filter
            if description_filter:
                attrs['description'] = description_filter
            if domain_filter:
                attrs['domain'] = domain_filter

            if self._is_path(private_key_filter):
                key = self._read_content(private_key_filter)
            else:
                key = private_key_filter

            if self._is_path(certificate_filter):
                content = self._read_content(certificate_filter)
            else:
                content = certificate_filter

            if type_filter == 'server':
                if not private_key_filter:
                    self.fail_json(msg='private_key mandatory when type is set to server.')
            if not content and not certificate:
                self.fail_json(msg='certificate is mandatory field.')

            if certificate:
                changed = True

                mattrs = {}
                if name_filter:
                    if certificate.name != name_filter:
                        mattrs['name'] = name_filter
                if admin_state_filter:
                    if certificate.admin_state_up != admin_state_filter:
                        mattrs['admin_state_up'] = admin_state_filter
                if description_filter:
                    if certificate.description != description_filter:
                        mattrs['description'] = description_filter
                if type_filter:
                    if certificate.type != type_filter:
                        mattrs['type'] = type_filter
                if domain_filter:
                    if certificate.domain != domain_filter:
                        mattrs['domain'] = domain_filter
                if key:
                    if certificate.private_key != key:
                        mattrs['private_key'] = key
                if content:
                    if certificate.certificate != content:
                        mattrs['certificate'] = content

                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                certificate = self.conn.elb.update_certificate(certificate, mattrs)
                self.exit_json(
                    changed=changed,
                    member=certificate.to_dict(),
                    id=certificate.id)

            cert = self.conn.elb.create_certificate(
                certificate=content,
                private_key=key,
                **attrs)
            data = cert.to_dict()
            data.pop('location')
            data.pop('content')
            data.pop('key')
            self.exit(changed=True, elb_certificate=data)


def main():
    module = LoadBalancerCertificateModule()
    module()


if __name__ == "__main__":
    main()
