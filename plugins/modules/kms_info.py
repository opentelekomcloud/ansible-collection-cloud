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
module: kms_info
short_description: Get info about KMS keys.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.12.5"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Get KMS key info from the OTC.
options:
  name:
    description:
      - name or ID of the CMK to be queried.
    type: str
  key_state:
    description:
      - State of a CMK, values from 1 to 5.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
keys:
    description:
        - Info about about a CMK.
    returned: On Success
    type: complex
    contains:
        key_id:
          description: CMK ID.
          type: str
          sample: "0d0466b0-e727-4d9c-b35d-f84bb474a37f"
        creation_date:
          description: Time when a key is created.
          type: str
          sample: "1638806642000"
        default_key_flag:
          description: Identification of a Master Key.
          type: str
          sample: "0"
        domain_id:
          description: User domain ID.
          type: str
          sample: "b168fe00ff56492495a7d22974df2d0b"
        key_alias:
          description: Alias of a CMK.
          type: str
          sample: "do-not-delete-pls"
        key_description:
          description: Description of a CMK.
          type: str
          sample: ""
        key_state:
          description: State of a CMK.
          type: str
          sample: "2"
        key_type:
          description: Type of a CMK.
          type: str
          sample: "1"
        realm:
          description: Region where a CMK resides.
          type: str
          sample: "eu-de"
        scheduled_deletion_date:
          description: Time when a key will be deleted as scheduled.
          type: str
          sample: ""
'''

EXAMPLES = '''
# Get info about KMS keys
- opentelekomcloud.cloud.kms_info:
    name: "kms-test-123"
  register: result
'''

import re
from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule

UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)


class KMSInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
        key_state=dict(required=False, no_log=False),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    otce_min_version = '0.26.0'

    def run(self):

        data = []
        query = {}

        if self.params['key_state']:
            query['key_state'] = self.params['key_state']

        if self.params['name']:
            if UUID_PATTERN.match(self.params['name']):
                raw = self.conn.kms.get_key(self.params['name'])
                if raw:
                    dt = raw.to_dict()
                    dt.pop('location')
                    data.append(dt)
            else:
                raw = self.conn.kms.find_key(
                    alias=self.params['name'],
                    ignore_missing=True)
                if raw:
                    dt = raw.to_dict()
                    dt.pop('location')
                    data.append(dt)
        else:
            for raw in self.conn.kms.keys(**query):
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit(
            changed=False,
            keys=data
        )


def main():
    module = KMSInfoModule()
    module()


if __name__ == '__main__':
    main()
