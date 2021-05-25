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
    choices: ['ACTIVE', 'ERROR', 'DISABLE', 'FREEZE', 'PENDING_CREATE', 'PENDING_UPDATE', 'PENDING_DELETE']
    type: str
  type:
    description:
      - Type of the record sets to be queried.
    choices: ['A', 'AAAA', 'MX', 'CNAME', 'TXT', 'NS']
    type: str
  name:
    description:
      - Names of record sets to be queried.
    type: str
  id:
    description:
      - IDs of record sets to be queried.
    type: str
  records:
    description:
      - Value included in the values of record sets to be queried.
    type: str
  soft_key:
    description:
      - Sorting condition of the record set list.
    choices: ['name', 'type']
    type: str
  soft_dir:
    description:
      - Sorting order of the record set list.
    choices: ['desc', 'asc']
    type: str
  zone_type:
    description:
      - Zone type of the record set to be queried.
    choices: ['public', 'private']
    type: str

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
recordsets:
    description: List of existing recordsets.
    type: complex
    returned: On Success.
    contains:
        created_at:
            description: timestamp when recordset has been created.
            type: str
            sample: "2021-05-24T15:27:19.335"
        description:
            description: Cluster Metadata dictionary.
            type: str
            sample:
        id:
            description: IDs of record sets to be queried.
            type: str
            sample:
        is_default:
            description: o_O.
            type: boolean
            sample:
        name:
            description: Names of record sets to be queried.
            type: str
            sample:
        project_id:
            description: o_O.
            type: str
            sample:
        records:
            Value included in the values of record sets to be queried.
            type: list
        status:
            description: Status of the record sets to be queried..
            type: dict
        ttl:
            description: Cluster status dictionary.
            type: int
        type:
            description: Zone type of the record set to be queried.
            type: str
        updated_at:
            description: Cluster status dictionary.
            type: str
        zone_name:
            description: Cluster status dictionary.
            type: str

'''

EXAMPLES = '''
# Get configs versions.
- cce_cluster_info:
    name: my_cluster
    status: available
  register: data
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
        records=dict(required=False),
        soft_key=dict(required=False, choices=['name', 'type']),
        soft_dir=dict(required=False, choices=['desc', 'asc']),
        zone_type=dict(required=False, choices=['public', 'private'])
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
                    self.fail_json(msg="Zone not found")
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
        if self.params['records']:
            query['records'] = self.params['records']
        if self.params['soft_dir']:
            query['soft_dir'] = self.params['soft_dir']
        if self.params['zone_type']:
            query['zone_type'] = self.params['zone_type']
        if self.params['soft_key']:
            query['soft_key'] = self.params['soft_key']

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
