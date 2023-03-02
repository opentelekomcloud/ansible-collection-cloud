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
module: bandwidth
short_description: Manage VPC bandwidth
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.13.1"
author: "Gubina Polina (@Polina-Gubina)"
description: Manage VPC bandwidth resource from the OTC.
options:
  name:
    description: Bandwidth name of id.
    type: str
    required: true
  size:
    description:
      - Specifies the bandwidth size. The shared bandwidth has a minimum\
      limit, which may vary depending on sites. The value ranges from 5 Mbit/s\
      to 1000 Mbit/s by default. If a decimal fraction (for example 10.2) or\
      a character string (for example "10") is specified, the specified value\
      will be automatically converted to an integer. The minimum increment \
      for bandwidth adjustment varies depending on the bandwidth range.\
      The minimum increment is 1 Mbit/s if the allowed bandwidth ranges from\
      0 Mbit/s to 300 Mbit/s (with 300 Mbit/s included). The minimum increment\
      is 50 Mbit/s if the allowed bandwidth ranges from 300 Mbit/s to 1000\
      Mbit/s (with 1000 Mbit/s included). The minimum increment is 500 Mbit/s\
      if the allowed bandwidth is greater than 1000 Mbit/s.
    type: int
  state:
    description: Whether resource should be present or absent.
    choices: [present, absent]
    type: str
    default: present
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
bandwidth:
  description: VPC bandwidth object.
  type: complex
  returned: On Success.
  contains:
    name:
      description: Specifies the bandwidth name.
      type: str
    size:
      description: Specifies the bandwidth size.
      type: int
    id:
      description:
        - Specifies the bandwidth ID, which uniquely\
         identifies the bandwidth.
      type: str
    share_type:
      description:
        - Specifies whether the bandwidth is shared or dedicated.
        - The value can be PER or WHOLE.
        - WHOLE means shared bandwidth, PER means dedicated bandwidth.
      type: str
    publicip_info:
      description: Specifies information about the EIP that uses the bandwidth.
      type: list
      elements: dict
      contains:
        publicip_id:
          description:
            - Specifies the ID of the EIP that uses the bandwidth.
          type: str
        publicip_address:
          description:
            - Specifies the obtained EIP if only IPv4 EIPs are available.
          type: str
        ip_version:
          description:
            - Specifies the IP address version. 4 means IPv4, 6 means IPv6.
          type: str
        publicip_type:
          description:
            - Specifies the EIP type.
          type: str
    tenant_id:
      description: Specifies the project ID.
      type: str
    bandwidth_type:
      description: Specifies the bandwidth type. The default value for the\
       shared bandwidth is share.
      type: str
    charge_mode:
      description: Specifies that the bandwidth is billed by bandwidth.\
       The value can be traffic.
      type: str
    billing_info:
      description:
        - Specifies the bill information. If billing_info is specified,\
        the bandwidth is in yearly/monthly billing mode.
      type: str
    status:
      description: Specifies the bandwidth status. Can be FREEZED and NORMAL.
      type: str
'''

EXAMPLES = '''
# Assign bandwidth:
- opentelekomcloud.cloud.bandwidth:
    name: "test-bandwidth"
    size: 15

# Update bandwidth:
- opentelekomcloud.cloud.bandwidth:
    name: "test-bandwidth"
    size: 10

# Delete bandwidth:
- opentelekomcloud.cloud.bandwidth:
    name: "test-bandwidth"
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class Bandwidth(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        size=dict(type='int', required=False),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def _system_state_change(self, bandwidth):
        state = self.params['state']
        changed = False
        if state == 'present' and not bandwidth:
            changed = True
        elif state == 'absent' and bandwidth:
            changed = True
        return changed

    def _require_update(self, bandwidth):
        changed = False
        if bandwidth:
            if self.params['size']:
                if self.params['size'] != bandwidth['size']:
                    return True
        return changed

    def run(self):
        query = {}

        state = self.params['state']
        bandwidth = self.conn.vpc.find_bandwidth(
            name_or_id=self.params['name'], ignore_missing=True)

        if self.ansible.check_mode:
            changed = (self._system_state_change(bandwidth)
                       or self._require_update(bandwidth))
            self.exit_json(changed=changed)

        if not bandwidth:
            if state == 'absent':
                self.exit(changed=False)
            query['name'] = self.params['name']
            if self.params['size']:
                query['size'] = self.params['size']
            new_bandwidth = self.conn.vpc.assign_bandwidth(**query)
            self.exit_json(changed=True, bandwidth=new_bandwidth)

        query['bandwidth'] = bandwidth.id

        if state == 'absent':
            self.conn.vpc.delete_bandwidth(**query)
            self.exit(changed=True)
        if not self._require_update(bandwidth):
            self.exit_json(changed=False)
        if self.params['size']:
            query['size'] = self.params['size']
        new_bandwidth = self.conn.vpc.update_bandwidth(**query)
        self.exit_json(changed=True, bandwidth=new_bandwidth)


def main():
    module = Bandwidth()
    module()


if __name__ == '__main__':
    main()
