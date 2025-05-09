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
module: dns_recordset_info
short_description: Get info about DNS recordsets.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.1"
author: "Yustina Kvrivishvili (@YustinaKvr)"
description:
  - Get DNS recordset info from the OTC.
options:
  zone:
    description:
      - ID or name of the required zone. If name had been provided, only public zone could be\
        returned. If private zone is required, only ID should be passed.
    type: str
  name:
    description:
      - ID or name of the existing record set. if zone is set we try to search recordsets in this\
        zone, otherwise we list all recordsets and filter them by name.
    type: str
  tags:
    description:
      - Resource tag.
    type: str
  status:
    description:
      - Status of the recordsets to be queried.
    choices: [active, error, disable, freeze, pending_create, pending_update, pending_delete]
    type: str
  type:
    description:
      - Type of the recordsets to be queried.
    choices: [a, aaaa, mx, cname, txt, ns, srv, caa, ptr]
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
recordset:
  description: List of dictionaries describing recordset and its metadata.
  type: complex
  returned: On Success.
  contains:
    created_at:
      description: Timestamp when recordset had been created
      type: str
      sample: "2021-05-24T15:27:19.335"
    description:
      description: Description of the recordset.
      type: str
      sample: "null"
    id:
      description: IDs of record sets to be queried.
      type: str
      sample: "ff80808275f5fb9c01799efcd1307062"
    is_default:
      description: Whether the record set is created by default.
      type: bool
      sample: false
    name:
      description: Name of the recordset.
      type: str
      sample: "recordset.test.zone."
    project_id:
      description: Project ID of the record set.
      type: str
      sample: "5dd3c0b24cdc4d31952c49589182a89d"
    records:
      description: Record set value.
      type: list
      sample: ["2.2.2.2", "1.1.1.1"]
'''

EXAMPLES = '''
# Get info about choosen DNS recordset.
- opentelekomcloud.cloud.dns_recordset_info:
    zone: "ff80808275f5fc0f017e886898315ee9"
    name: "ff80808275f5fc0f017e886898315ee2"
  register: recordsets
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSRecordsetInfoModule(OTCModule):

    argument_spec = dict(
        zone=dict(required=False),
        name=dict(required=False),
        tags=dict(required=False),
        status=dict(required=False, choices=['active', 'error', 'disable', 'freeze',
                                             'pending_create', 'pending_update', 'pending_delete']),
        type=dict(required=False, choices=['a', 'aaaa', 'mx', 'cname', 'txt', 'ns', 'srv', 'caa',
                                           'ptr'])
    )
    module_kwargs = dict(
        supports_check_mode=True,
        required_if=[('name', not None, ['zone'])]
    )

    def run(self):

        data = []
        query = {}
        recordset = None

        if self.params['zone']:
            try:
                query['zone'] = self.conn.dns.find_zone(
                    name_or_id=self.params['zone'], ignore_missing=False).id
            except self.sdk.exceptions.ResourceNotFound:
                self.fail_json(msg="Zone not found")
            if self.params['name']:
                try:
                    query['name_or_id'] = self.params['name']
                    if self.params['type']:
                        query['type'] = self.params['type']

                    recordset = self.conn.dns.find_recordset(
                        ignore_missing=False, **query)
                    dt = recordset.to_dict()
                    dt.pop('location')
                    data.append(dt)

                    self.exit(
                        changed=False,
                        recordset=data
                    )
                except self.sdk.exceptions.ResourceNotFound:
                    self.fail_json(msg="Recordset not found")
        if self.params['name']:
            query['name'] = self.params['name']
        if self.params['tags']:
            query['tags'] = self.params['tags']
        if self.params['status']:
            query['status'] = self.params['status'].upper()
        if self.params['type']:
            query['type'] = self.params['type'].upper()

        for raw in self.conn.dns.recordsets(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            recordset=data
        )


def main():
    module = DNSRecordsetInfoModule()
    module()


if __name__ == '__main__':
    main()
