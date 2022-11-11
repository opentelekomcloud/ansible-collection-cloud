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
module: subnet
short_description: Manage VPC subnet
extends_documentation_fragment: opentelekomcloud.cloud.otc
author: "Anton Kachurin (@outcatcher)"
version_added: "0.11.0"
description:
   - Manage (create, update or delete) Open Telekom Cloud VPC subnet.
options:
  state:
    description: Indicate desired state of the resource.
    choices: ['present', 'absent']
    default: present
    type: str
  name:
    description:
      - Specifies the subnet name or ID.
      - When creating a new subnet, the value can contain 1 to 64 characters,
        including letters, digits, underscores (_), hyphens (-), and periods (.).
    type: str
    required: true
  description:
    description:
      - Provides supplementary information about the subnet.
      - The value can contain no more than 255 characters and cannot contain angle brackets (< or >).
    type: str
  cidr:
    description:
      - Specifies the subnet CIDR block.
      - The value must be within the VPC CIDR block.
      - The value must be in CIDR format. The subnet mask cannot be greater than 28.
    type: str
  gateway_ip:
    description:
      - Specifies the gateway of the subnet.
      - The value must be an IP address in the subnet.
      - The value must be a valid IP address.
    type: str
  dhcp_enable:
    description:
      - Specifies whether DHCP is enabled for the subnet.
      - The value can be true (enabled) or false (disabled).
      - If this parameter is left blank, the system automatically sets it to true by default.
       If this parameter is set to false, newly created ECSs cannot obtain IP addresses, and
       usernames and passwords cannot be injected using Cloud-init.
    type: bool
  primary_dns:
    type: str
    description:
      - Specifies the IP address of DNS server 1 on the subnet.
      - The value must be an IP address.
  secondary_dns:
    type: str
    description:
      - Specifies the IP address of DNS server 2 on the subnet.
      - The value must be an IP address.
  dns_list:
    description:
      - Specifies the DNS server address list of a subnet.
      - This field is required if use more than two DNS servers.
      - This parameter value is the superset of both I(primary_dns) and I(secondary_dns).
    type: list
    elements: str
    aliases: ['dnsList']
  availability_zone:
    description: Specifies the AZ to which the subnet belongs.
    type: str
  vpc:
    description: Specifies the name or ID of the VPC to which the subnet belongs.
    required: true
    type: str
    aliases: ['vpc_id']
  extra_dhcp_opts:
    description: Specifies the NTP server address configured for the subnet.
    type: list
    elements: dict
    suboptions:
      opt_value:
        description:
          - Specifies the NTP server address configured for the subnet.
          - The option ntp for opt_name indicates the NTP server configured for the subnet.
           Currently, only IPv4 addresses are supported. A maximum of four IP addresses can be
           configured, and each address must be unique. Multiple IP addresses must be separated
           using commas (,). The option null for opt_name indicates that no NTP server is configured
           for the subnet. The parameter value cannot be an empty string.
        type: str
      opt_name:
        description:
          - Specifies the NTP server address name configured for the subnet.
        type: str
        required: true
        choices: ['ntp']
requirements: ['openstacksdk', 'otcextensions>=0.24.5']
'''

EXAMPLES = '''
- name: Create VPC
  opentelekomcloud.cloud.vpc:
    name: "vpc-test"
    cidr: "192.168.0.0/16"
  register: vpc

- name: Create subnet
  opentelekomcloud.cloud.subnet:
    name: "test-subnet"
    vpc_id: "{{ vpc.vpc.id }}"
    cidr: "192.168.0.0/16"
    gateway_ip: "192.168.0.1"
    dns_list:
      - "100.125.4.25"
      - "100.125.129.199"

- name: Update subnet
  opentelekomcloud.cloud.subnet:
    name: "test-subnet"
    vpc_id: "{{ vpc.vpc.id }}"
    dns_list:
      - "100.125.4.25"
      - "1.1.1.1"
    dhcp_enable: false

- name: Delete subnet
  opentelekomcloud.cloud.subnet:
    name: "test-subnet"
    vpc_id: "{{ vpc.vpc.id }}"
    state: absent
'''

RETURN = '''
subnet:
    description: Created subnet resource.
    returned: On success when I(state=present)
    type: complex
    contains:
        id:
            description: Specifies the resource identifier in the form of UUID.
            type: str
            sample: "0f21367c-022d-433e-8ddb-1c31a65a05b8"
        name:
            description: Specifies the subnet name.
            type: str
            sample: "test-subnet"
        description:
            description: Provides supplementary information about the subnet.
            type: str
        cidr:
            description: Specifies the subnet CIDR block.
            type: str
        gateway_ip:
            description: Specifies the gateway of the subnet.
            type: str
        dhcp_enable:
            description: Specifies whether the DHCP function is enabled for the subnet.
            type: bool
        primary_dns:
            description: Specifies the IP address of DNS server 1 on the subnet.
            type: str
        secondary_dns:
            description: Specifies the IP address of DNS server 2 on the subnet.
            type: str
        dns_list:
            description: Specifies the DNS server address list of a subnet.
            type: list
            elements: str
        availability_zone:
            description: Specifies the AZ to which the subnet belongs, which can be
              obtained from endpoints.
            type: str
        vpc_id:
            description: Specifies the ID of the VPC to which the subnet belongs.
            type: str
        neutron_network_id:
            description: Specifies the ID of the corresponding network (OpenStack Neutron API).
            type: str
            sample: "0f21367c-022d-433e-8ddb-1c31a65a05b8"
        neutron_subnet_id:
            description: Specifies the ID of the corresponding subnet (OpenStack Neutron API).
            type: str
            sample: "235f5393-a5e0-4b7a-9655-70eb3c13e2fe"
        extra_dhcp_opts:
            description: Specifies the NTP server address configured for the subnet.
            type: list
            elements: dict
            sample: [
                {
                    "opt_value": "10.100.0.33,10.100.0.34",
                    "opt_name": "ntp"
                }
            ]
'''

import copy

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SubnetModule(OTCModule):
    argument_spec = dict(
        state=dict(default='present', choices=['absent', 'present']),
        name=dict(type='str', required=True),
        vpc=dict(type='str', required=True, aliases=['vpc_id']),
        description=dict(type='str'),
        cidr=dict(type='str'),
        gateway_ip=dict(type='str'),
        dhcp_enable=dict(type='bool'),
        primary_dns=dict(type='str'),
        secondary_dns=dict(type='str'),
        dns_list=dict(type='list', elements='str', aliases=['dnsList']),
        availability_zone=dict(type='str'),
        extra_dhcp_opts=dict(type='list', elements='dict', options=dict(
            opt_value=dict(type='str'),
            opt_name=dict(type='str', required=True, choices=['ntp'])
        ))
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    _update_fields = {'dns_list', 'primary_dns', 'secondary_dns', 'extra_dhcp_opts'}
    _update_forbidden = {'cidr', 'gateway_ip'}

    def run(self):
        vpc = self.conn.vpc.find_vpc(self.params['vpc'])
        self.params['vpc'] = vpc.id
        subnet = self.find_vpc_subnet()

        data = copy.deepcopy(self.params)
        data['vpc_id'] = data.pop('vpc')
        state = data.pop('state')

        has_changes = self._changed(subnet, data)
        if self.ansible.check_mode:
            self.exit(changed=has_changes, subnet=subnet)

        if state == 'present':
            if subnet is None:
                self.sdk.resource.wait_for_status(
                    self.conn.vpc,
                    vpc, 'OK',
                    None, 1, 5
                )
                subnet = self.conn.vpc.create_subnet(**data)
            elif has_changes:
                err_fields = {}
                for field in self._update_forbidden:
                    val = data.get(field, None)
                    if val is not None:
                        err_fields[field] = val
                if err_fields:
                    self.fail(
                        f'updating subnet fields {err_fields} is not '
                        f'supported (subnet: {subnet})')
                update_data = {}
                for field in self._update_fields:
                    if data[field] is not None:
                        update_data[field] = data[field]
                subnet = self.conn.vpc.update_subnet(
                    subnet,
                    name=subnet.name,
                    **update_data,
                )
            subnet = self.sdk.resource.wait_for_status(
                self.conn.vpc,
                subnet, 'ACTIVE',
                None, 2, 20
            )
            self.exit(changed=has_changes, subnet=subnet)
        elif state == 'absent':
            if subnet:
                self.conn.vpc.delete_subnet(subnet, ignore_missing=True)
                self.sdk.resource.wait_for_delete(self.conn.vpc, subnet, 2, 60)
            self.exit(changed=has_changes)

    def _changed(self, state, expected):
        expected_removed = self.params['state'] == 'absent'
        actual_missing = state is None
        if expected_removed:
            return not actual_missing
        elif actual_missing:
            return True

        if _total_dns_list(state) != _total_dns_list(expected):
            return True

        for field in self.argument_spec:  # check only against possible arguments
            if field not in expected:
                continue
            if expected[field] is None:  # ignore not set fields
                continue
            if field in ['dns_list', 'primary_dns', 'secondary_dns']:
                continue
            if field in ['vpc', 'vpc_id']:
                field = 'vpc_id'  # as `vpc` should be an ID too at this place
            if state.get(field, None) != expected[field]:
                self.log(
                    f'There is a difference in field {field}. Expected '
                    f'{expected[field]}, got {state[field]}')
                return True
        return False

    def find_vpc_subnet(self):
        name = self.params['name']
        vpc_id = self.params['vpc']

        try:
            # first, try to find subnet by ID
            return self.conn.vpc.get_subnet(name)
        except (self.sdk.exceptions.ResourceNotFound,
                # in case id is not a UUID (e.g. us subnet name):
                self.sdk.exceptions.BadRequestException):
            subnets = self.conn.vpc.subnets(vpc_id=vpc_id)
            subnets = [s for s in subnets if s.name == name and s.vpc_id == vpc_id]
            if len(subnets) == 0:
                return None
            if len(subnets) > 1:
                self.fail(
                    msg=(
                        f'More than one subnet with name {name} is found '
                        f'in vpc {vpc_id}. Please use ID instead.'
                    )
                )
            return subnets[0]


def _total_dns_list(obj: dict) -> set:
    if obj is None:
        return set()

    dns_list = obj.get('dns_list', []) or []
    dns_set = set(dns_list)
    dns_set.add(obj['primary_dns'])
    dns_set.add(obj['secondary_dns'])
    dns_set.discard(None)
    return dns_set


def main():
    module = SubnetModule()
    module()


if __name__ == '__main__':
    main()
