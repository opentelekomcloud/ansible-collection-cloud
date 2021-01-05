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
module: anti_ddos_optional_policies_info
short_description: Get Anti-DDoS optional defense policies info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.4.0"
author: "Irina Pereiaslavskaia (@irina-pereiaslavskaia)"
description:
  - Get optional Anti-DDoS defense policies from the OTC.
options: {}
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
anti_ddos_optional_policies_info:
  description: Lists of defense policies info.
  type: complex
  returned: On Success
  contains:
    traffic_limited_list:
      description: List of traffic limits.
      type: complex
      returned: On Success
      contains:
        traffic_pos_id:
          description: Position ID of traffic.
          type: int
          sample: 1
        traffic_per_second:
          description: Threshold of traffic per second (Mbit/s).
          type: int
          sample: 10
        packet_per_second:
          description: Threshold of number of packets per second.
          type: int
          sample: 2000
    http_limited_list:
      description: List of HTTP limits
      type: complex
      returned: On Success
      contains:
        http_request_pos_id:
          description: Position ID of number of HTTP requests
          type: int
          sample: 1
        http_packet_per_second:
          description: Threshold of number of HTTP requests per second
          type: int
          sample: 10000
    connection_limited_list:
      description: List of limits of numbers of connections
      type: complex
      returned: On Success
      contains:
        cleaning_access_pos_id:
          description: Position ID of access limit during cleaning
          type: int
          sample: 1
        new_connection_limited:
          description: Number of new connections of a source IP address
          type: int
          sample: 80
        total_connection_limited:
          description: Total number of connections of a source IP address
          type: int
          sample: 700
    extend_ddos_config:
      description: Information about Anti-DDoS defense policies set by users.
      type: complex
      returned: On Success
      contains:
        new_connection_limited:
          description: Number of new connections of a source IP address
          type: int
          sample: 80
        total_connection_limited:
          description: Total number of connections of a source IP address
          type: int
          sample: 700
        http_packet_per_second:
          description: Threshold of number of HTTP requests per second
          type: int
          sample: 10000
        traffic_per_second:
          description: Threshold of traffic per second (Mbit/s).
          type: int
          sample: 10
        packet_per_second:
          description: Threshold of number of packets per second.
          type: int
          sample: 2000
        setID:
          description: Position ID
          type: int
          sample: 33
'''

EXAMPLES = '''
# Querying Optional Anti-DDoS Defense Policies
- opentelekomcloud.cloud.anti_ddos_optional_policies_info:
  register: anti_ddos_optional_policies_info
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class AntiDDoSOptionalPoliciesInfoModule(OTCModule):
    argument_spec = dict()

    def run(self):

        data = []

        for raw in self.conn.anti_ddos.configs():
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(changed=False, anti_ddos_optional_policies_info=data)


def main():
    module = AntiDDoSOptionalPoliciesInfoModule()
    module()


if __name__ == '__main__':
    main()
