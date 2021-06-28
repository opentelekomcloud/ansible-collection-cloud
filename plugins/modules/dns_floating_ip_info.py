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
module: dns_floating_ip_info
short_description: Query the PTR record of an EIP.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.1"
author: "Yustina Kvrivishvili (@YustinaKvr)"
description:
  - Query the PTR record of an EIP.
options:
  region:
    description:
      - Region of the tenant.
    required: true
    type: str
  floatingip_id:
    description:
      - EIP ID.
    required: true
    type: str
  enterprise_project_id:
    description:
      - Specifies the ID of the enterprise project associated with the PTR record.
    type: str
  tags:
    description:
      - Resource tag. The format is as follows: key1,value1|key2,value2.
    type: str
  status:
    description:
      - Resource status.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
dns_recordset:
  description: List of dictionaries describing PTR record and its metadata.
  type: complex
  returned: On Success.
  contains:
    id:
      description: PTR record ID, which is in {region}:{floatingip_id} format
      type: str
      sample: "region_id:c5504932-bf23-4171-b655-b87a6bc59334"
    ptrdname:
      description: Domain name of the PTR record.
      type: str
      sample: "www.example.com."
    description:
      description: PTR record description.
      type: str
      sample: "Description for this PTR record"
    address:
      description: EIP.
      type: str
      sample: "10.154.52.138"
    ttl:
      description: PTR record cache duration (in second) on a local DNS server. The value ranges\
       from 1 to 2147483647. The default value is 300.
      type: int
      sample: 300
    status:
      description: Resource status.
      type: str
      sample: "ACTIVE"
    action:
      description: Requested operation on the resource.
      type: str
      sample: "CREATE"
    links:
      description: Requested operation on the resource.
      type: obj
      sample: "CREATE"
'''
from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DNSRecordsetInfoModule(OTCModule):

    argument_spec = dict(
        region=dict(required=True),
        floatingip_id=dict(required=True),
        enterprise_project_id=dict(required=False),
        tags=dict(required=False),
        status=dict(required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
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
                    recordset = self.conn.dns.find_recordset(
                        zone=query['zone'], name_or_id=self.params['name'],
                        ignore_missing=False)
                    dt = recordset.to_dict()
                    dt.pop('location')
                    data.append(dt)

                    self.exit(
                        changed=False,
                        dns_recordset=data
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
            dns_recordset=data
        )


def main():
    module = DNSRecordsetInfoModule()
    module()


if __name__ == '__main__':
    main()
