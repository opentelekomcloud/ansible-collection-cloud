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