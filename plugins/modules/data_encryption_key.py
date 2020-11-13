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
module: data_encryption_key
short_description: Add/Delete data encryption key from the OTC
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.2.0"
author: "Polina Gubina (@Polina-Gubina)"
description:
  - Add or Remove data encryption key in OTC.
options:
  key_id:
    description:
      - ID of a CMK.
    required: true
    type: str
  encryption_context:
    description:
      - Key-value pairs with a maximum length of 8192 characters. \
      This parameter is used to record resource context information,\
      excluding sensitive information, to ensure data integrity.
      -  If this parameter is specified during encryption, it is also required for decryption.
    required: false
    type: dict
  datakey_length:
    description:
      - Number of bits of a key. The value is 512.
      - Mandatory for creating.
    type: str
  sequence:
    description:
      - 36-byte serial number of a request message.
    required: false
    type: str
  plaintext_free:
    description:
      - Create a plaintext-free DEK, that is, the returned result of this API includes only the plaintext of the DEK.
    required: false
    choices: ['yes', 'no']
    default: 'no'
    type: str
  plain_free:
    description:
      - Create a plaintext-free DEK, that is, the returned result of this API includes only the plaintext of the DEK.
      - Mandatory for encrypting.
    required: false
    choices: ['yes', 'no']
    default: 'no'
    type: str
  datakey_plain_length:
    description:
      - Number of bytes of a DEK in plaintext. The value is 64.
      - Mandatory for encrypting.
    type: str
  cipher_text:
    description:
      - This parameter indicates the hexadecimal character string of the DEK ciphertext and the metadata.
       The value is the cipher_text value in the encryption result of a DEK.
      - Mandatory for decrypting.
    type: str
  datakey_cipher_length:
    description:
      - Number of bytes of a key. The value is 64.
      - Mandatory for decrypting.
    type: str
  encrypt:
    description:
      - Encrypt a DEK using a specified CMK.
    choices: ['yes', 'no']
    default: 'no'
    type: str
  decrypt:
    description:
      - Decrypt a DEK using a specified CMK.
    choices: ['yes', 'no']
    default: 'no'
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
key_id:
    description: CMK ID.
    returned: On success when C(state=present)
    type: str
    sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
plain_text:
    description: The plaintext of a DEK is expressed in hexadecimal format, and two characters indicate one byte.
    returned: On success when C(state=present)
    type: str
    sample: ""
cipher_text:
    description:  The ciphertext of a DEK is expressed in hexadecimal format, and two characters indicate one byte.
    returned: On success when C(state=present)
    type: str
    sample: ""
'''

EXAMPLES = '''
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VPCPeeringInfoModule(OTCModule):
    argument_spec = dict(
        key_id=dict(required=True),
        encryption_context=dict(required=False),
        datakey_length=dict(required=True),
        sequence=dict(required=False),
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        key = self.params['key']
        encryption_context = self.params['key_description']
        datakey_length = self.params['origin']
        sequence = self.params['sequence']


        attrs = {'key': key, }

        if self.params['key_description']:
            attrs['key_description'] = key_description

        if self.params['origin']:
            attrs['origin'] = origin

        if self.params['sequence']:
            attrs['sequence'] = sequence

        key = self.conn.kms.create_key(**attrs)
        self.exit(changed=True, key=key)


def main():
    module = VPCPeeringInfoModule()
    module()


if __name__ == '__main__':
    main()
