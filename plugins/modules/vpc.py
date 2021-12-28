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
module: vpc
short_description: Create or delete vpc from Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
author: "Polina Gubina (@polina-gubina)"
description:
   - Create or Delete vpc from OpenStack.
options:
   state:
     description: Indicate desired state of the resource
     choices: ['present', 'absent']
     default: present
     type: str
   name:
     description: Name to be give to the router.
     required: false
     type: str
   description:
     description: Provides supplementary information about the VPC.
     required: false
     type: str
   cidr:
     description:
        - Specifies the available IP address ranges for subnets in the VPC.
        - If cidr is not specified, the default value is left blank.
        - The value must be in CIDR format, for example, 192.168.0.0/16.
     required: false
     type: str
   routes:
     description: Specifies the route list.
     required: false
     type: list
     elements: dict
     suboptions:
       destination:
         description:
           - Specifies the destination network segment of a route.
           - The value must be in the CIDR format. Currently, only the value
            0.0.0.0/0 is supported.
         type: str
         required: false
       nexthop:
         description:
           - Specifies the next hop of a route.
           - The value must be an IP address and must belong to the subnet
            in the VPC. Otherwise, this value does not take effect.
         type: str
         required: false
   enable_shared_snat:
     description: Specifies whether the shared SNAT function is enabled.
     required: false
     type: bool
requirements: ["openstacksdk", "otcextensions"]
'''

EXAMPLES = '''
- name: Create vpc
  opentelekomcloud.cloud.vpc:
    name: "vpc-test"
    cidr: "192.168.0.0/24"
    state: present

- name: Update vpc
  opentelekomcloud.cloud.vpc:
    name: "vpc-test"
    description: "New description"

- name: Delete vpc
  opentelekomcloud.cloud.vpc:
    name: "vpc-test"
    state: absent
'''

RETURN = '''
vpc:
    description: Dictionary describing the vpc.
    returned: On success when I(state) is 'present'
    type: complex
    contains:
        id:
            description: Vpc ID.
            type: str
            sample: "474acfe5-be34-494c-b339-50f06aa143e4"
        name:
            description: Vpc name.
            type: str
            sample: "vpc-test"
        description:
            description: Provides supplementary information about the VPC.
            type: str
            sample: ""
        status:
            description: The vpc status. Can be 'CREATING' or 'OK'.
            type: str
            sample: "OK"
        cidr:
            description:
                - Specifies the available IP address ranges for subnets in the VPC.
                - Possible values are 10.0.0.0/8~24, 172.16.0.0/12~24, 192.168.0.0/16~24.
                - Must be in CIDR format.
            type: str
            sample: "192.168.0.0/24"
        routes:
            description: Specifies the route information.
            type: list
            elements: dict
            contains:
                destination:
                    description:
                        - Specifies the destination network segment of a route.
                        - The value must be in the CIDR format. Currently, only the value \
                        0.0.0.0/0 is supported.
                    type: str
                nexthop:
                    description:
                        - Specifies the next hop of a route.
                        - The value must be an IP address and must belong to the subnet in the VPC.
                         Otherwise, this value does not take effect.
                    type: str
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VpcModule(OTCModule):
    argument_spec = dict(
        state=dict(default='present', choices=['absent', 'present']),
        name=dict(required=False),
        description=dict(required=False),
        cidr=dict(required=False),
        routes=dict(type='list', elements='dict', required=False),
        enable_shared_snat=dict(type='bool', required=False)
    )

    def run(self):

        query = {}
        state = self.params['state']
        name = self.params['name']
        description = self.params['description']
        cidr = self.params['cidr']
        routes = self.params['routes']
        enable_shared_snat = self.params['enable_shared_snat']

        if name:
            query['name'] = name
        if description:
            query['description'] = description
        if cidr:
            query['cidr'] = cidr

        vpc = None
        if name:
            vpc = self.conn.vpc.find_vpc(name, ignore_missing=True)

        if state == 'present':
            if self.ansible.check_mode:
                self.exit(changed=True)

            if not vpc:
                new_vpc = self.conn.vpc.create_vpc(**query)
                if routes or enable_shared_snat is not None:
                    query_update = {}
                    if routes:
                        query_update['routes'] = routes
                    if enable_shared_snat is not None:
                        query_update['enable_shared_snat'] = enable_shared_snat
                    new_vpc = self.conn.vpc.update_vpc(vpc=new_vpc, **query_update)
                self.exit(changed=True, vpc=new_vpc)

            else:
                if routes:
                    query['routes'] = routes
                if enable_shared_snat is not None:
                    query['enable_shared_snat'] = enable_shared_snat
                updated_vpc = self.conn.vpc.update_vpc(vpc=vpc, **query)
                self.exit(changed=True, vpc=updated_vpc)
        else:
            if vpc:
                if not self.ansible.check_mode:
                    self.conn.vpc.delete_vpc(vpc.id)
                self.exit(changed=True)
            else:
                self.exit(changed=False)


def main():
    module = VpcModule()
    module()


if __name__ == '__main__':
    main()
