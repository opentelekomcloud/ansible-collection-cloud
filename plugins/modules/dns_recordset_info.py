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
short_description: Getting info about DNS Recordsets
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.1"
author: "Yustina Kvrivishvili (@YustinaKvr)"
description:
  - Get DNS record set info from the OTC.
options:
  zone:
    description:
      - ID or name of the required zone.
    type: str
  recordset:
    description:
      - ID or name of the existing record set.
    type: str
  tags:
    description:
      - Resource tag.
    type: str
  status:
    description:
      - Status of the record sets to be queried.
    choices: ['active', 'error', 'disable', 'freeze', 'pending_create', 'pending_update', 'pending_delete']
    type: str
  type:
    description:
      - Type of the record sets to be queried.
    choices: ['a', 'aaaa', 'mx', 'cname', 'txt', 'ns']
    type: str
  name:
    description:
      - Names of record sets to be queried.
    type: str
  id:
    description:
      - IDs of record sets to be queried.
    type: str

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
dns_recordset:
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
      type: dict
      sample: 2.2.2.2
'''

EXAMPLES = '''
#Get info about choosen DNS recordset.
- opentelekomcloud.cloud.dns_recordset_info:
    zone: "{{ dns_zo.zone.id }}"
  register: recordsets
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSRecordsetInfoModule(OTCModule):

    argument_spec = dict(
        zone=dict(required=False),
        recordset=dict(required=False),
        tags=dict(required=False),
        status=dict(required=False, choices=['active', 'error', 'disable', 'freeze', 'pending_create', 'pending_update', 'pending_delete']),
        type=dict(required=False, choices=['a', 'aaaa', 'mx', 'cname', 'txt', 'ns']),
        name=dict(required=False),
        id=dict(required=False),
    )
    module_kwargs = dict(
        required_if=[
            ('recordset', not None,
             ['zone'])
        ]
    )

    def run(self):

        data = []
        query = {}

        if self.params['zone']:
            try:
                query['zone'] = self.conn.dns.find_zone(name_or_id=self.params['zone'], ignore_missing=False).id
            except self.sdk.exceptions.ResourceNotFound:
                self.fail_json(msg="Zone not found")
            if self.params['recordset']:
                try:
                    query['recordset'] = self.conn.dns.find_recordset(zone=query['zone'], name_or_id=self.params['recordset'], ignore_missing=False).id
                except self.sdk.exceptions.ResourceNotFound:
                    self.fail_json(msg="Recordset not found")
        if self.params['tags']:
            query['tags'] = self.params['tags']
        if self.params['status']:
            query['status'] = self.params['status'].upper()
        if self.params['type']:
            query['type'] = self.params['type'].upper()
        if self.params['name']:
            query['name'] = self.params['name']
        if self.params['id']:
            query['id'] = self.params['id']

        for raw in self.conn.dns.recordsets(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            dns_recordset=data
        )


def main():
    module = DNSRecordsetInfoModule()
    module()


if __name__ == '__main__':
    main()
