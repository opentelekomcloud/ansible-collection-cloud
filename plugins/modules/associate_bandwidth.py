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
module: associate_bandwidth
short_description: Add or remove eip to shared bandwidth
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.13.1"
author: "Gubina Polina (@Polina-Gubina)"
description: Add or remove eip to shared bandwidth
options:
  name:
    description: Bandwidth name of id.
    type: str
    required: true
  size:
    description:
      - Specifies size which will be allocated for removed eip.\
      After an EIP is removed from a shared bandwidth, a dedicated\
      bandwidth will be allocated to the EIP, and you  will be billed\
      for the dedicated bandwidth.
    type: int
  publicip_id:
    description:
      - Specifies the ID of the EIP to be added or removed from\
       shared bandwidth.
    type: str
    required: true
  publicip_type:
    description:
      - Specifies the EIP type.
      - publicip_id is an IPv4 port. If publicip_type is not specified, the \
      default value is 5_bgp.
    type: str
    choices: ['5_bgp', '5_mailbgp', '5_gray']
  charge_mode:
    description:
        - After an EIP is removed from a shared bandwidth, a dedicated\
         bandwidth will be allocated to the EIP, and you will be billed for\
         the dedicated bandwidth. Specifies whether the dedicated bandwidth\
         used by the EIP that has been removed from a shared bandwidth is\
         billed by traffic or by bandwidth.
        - Mandatory for removing eip from a shared bandwidth.
    type: str
    choices: ['bandwidth', 'traffic']
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
      description: Specifies the bandwidth ID, which uniquely\
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
# Add eip to bandwidth:
opentelekomcloud.cloud.bandwidth:
  name: "test-bandwidth"
  publicip_id: "42d922af-18be-4e6d-804e-18f8c8871471"

# Remove eip from bandwidth:
opentelekomcloud.cloud.bandwidth:
  name: "new-bandwidth"
  publicip_id: "42d922af-18be-4e6d-804e-18f8c8871471"
  charge_mode: "traffic"
  size: 10
  state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class Bandwidth(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        size=dict(type='int', required=False),
        publicip_id=dict(type='str', required=True),
        publicip_type=dict(type='str',
                           choices=['5_bgp', '5_mailbgp', '5_gray'],
                           required=False),
        charge_mode=dict(type='str',
                         choices=['bandwidth', 'traffic'], required=False),
        state=dict(type='str',
                   choices=['present', 'absent'], default='present'),
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'absent', ['charge_mode', 'size'])
        ],
        supports_check_mode=True
    )

    def _system_state_change(self, bandwidth):
        changed = False
        publicip_id = self.params['publicip_id']
        publicip_ids = [dict['publicip_id']
                        for dict in bandwidth.publicip_info]
        current = publicip_id in publicip_ids
        if self.params['state'] == 'present' and not current:
            changed = True
        if self.params['state'] == 'absent' and current:
            changed = True
        return changed

    def run(self):
        query = {}

        state = self.params['state']
        bandwidth = self.conn.vpc.find_bandwidth(
            name_or_id=self.params['name'])
        if not bandwidth:
            self.fail_json(
                msg='bandwidth {0} not found'.format(self.params['name']))

        changed = self._system_state_change(bandwidth)
        if self.ansible.check_mode:
            self.exit_json(changed=changed)

        if not changed:
            self.exit_json(changed=False)

        query['bandwidth'] = bandwidth.id

        if state == 'present':
            if self.params['publicip_type']:
                publicip_type = self.params['publicip_type']
            else:
                publicip_type = '5_bgp'
            query['publicip_info'] = [
                {'publicip_id': self.params['publicip_id'],
                 'publicip_type': publicip_type}
            ]
            new_bandwidth = self.conn.vpc.add_eip_to_bandwidth(**query)
            self.exit_json(changed=True, bandwidth=new_bandwidth)
        else:
            query['charge_mode'] = self.params['charge_mode']
            query['size'] = self.params['size']
            query['publicip_info'] = [
                {'publicip_id': self.params['publicip_id']}
            ]
            new_bandwidth = self.conn.vpc.remove_eip_from_bandwidth(**query)
            self.exit_json(changed=True, bandwidth=new_bandwidth)


def main():
    module = Bandwidth()
    module()


if __name__ == '__main__':
    main()
