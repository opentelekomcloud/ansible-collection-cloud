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
   enabled_shared_snat:
     description: Specifies whether the shared SNAT function is enabled.
     required: false
     type: bool
requirements: ["openstacksdk", "otcextensions"]
'''

EXAMPLES = '''
'''

RETURN = '''
router:
    description: Dictionary describing the router.
    returned: On success when I(state) is 'present'
    type: complex
    contains:
        id:
            description: Router ID.
            type: str
            sample: "474acfe5-be34-494c-b339-50f06aa143e4"
        name:
            description: Router name.
            type: str
            sample: "router1"
        admin_state_up:
            description: Administrative state of the router.
            type: bool
            sample: true
        status:
            description: The router status.
            type: str
            sample: "ACTIVE"
        tenant_id:
            description: The tenant ID.
            type: str
            sample: "861174b82b43463c9edc5202aadc60ef"
        external_gateway_info:
            description: The external gateway parameters.
            type: dict
            sample: {
                      "enable_snat": true,
                      "external_fixed_ips": [
                         {
                           "ip_address": "10.6.6.99",
                           "subnet_id": "4272cb52-a456-4c20-8f3c-c26024ecfa81"
                         }
                       ]
                    }
        routes:
            description: The extra routes configuration for L3 router.
            type: list
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VpcModule(OTCModule):
    argument_spec = dict(
        state=dict(default='present', choices=['absent', 'present']),
        name=dict(required=False),
        description=dict(required=False),
        cidr=dict(required=False),
        routes=dict(required=False),
        enabled_shared_snat=dict(required=False)
    )

    def run(self):

        query = {}
        state = self.params['state']
        name = self.params['name']
        description = self.params['description']
        cidr = self.params['cidr']
        routes = self.params['routes']
        enabled_shared_snat = self.params['enabled_shared_snat']

        if name:
            query['name'] = name
        if description:
            query['description'] = description
        if cidr:
            query['cidr'] = cidr

        vpc = None
        if name:
            vpc = self.conn.vpc.find_vpc(name_or_id=name)

        if state == 'present':
            if self.ansible.check_mode:
                self.exit(changed=True)

            if not vpc:
                new_vpc = self.conn.vpc.create_vpc(**query)
                self.exit(changed=True, vpc=new_vpc)
            else:
                if routes:
                    query['routes'] = routes
                if enabled_shared_snat:
                    query['enabled_shared_snat'] = enabled_shared_snat
                updated_vpc = self.conn.vpc.update_vpc(vpc=vpc, **query)
                self.exit(changed=True, vpc=updated_vpc)
        else:
            if vpc:
                if self.ansible.check_mode:
                    self.exit(changed=True)
                self.conn.network.delete_router(vpc.id)
                self.exit(changed=True)
            else:
                self.exit(changed=False)

def main():
    module = VpcModule()
    module()


if __name__ == '__main__':
    main()
