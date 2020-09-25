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
module: vpc_peering
short_description: Add/Update/Delete vpc peering connection from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Polina Gubina (@polina-gubina)"
description:
  - Add or Remove vpc peering from the OTC.
options:
  name:
    description: Name that has to be given to the vpc peering connection
    required: true
    type: str
  state:
    description: Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
  local_router:
    description: Name or ID of the local router.
    type: str
  project_id_local:
    description: Specifies the ID of the project to which a local VPC belongs.
    type:  str
  peer_router:
    description: Name or ID of the peer router.
    type: str
  project_id_peer:
    description: Specifies the ID of the project to which a peer VPC belongs.
    type: str
  new_name:
    description: Specifies a new name to an existing vpc peering.
    type: str
  description:
    description: Provides supplementary information about the VPC peering connection.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
id:
    description: Specifies the VPC peering connection ID.
    returned: On success when C(state=present)
    type: str
    sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
name:
    description: Specifies the VPC peering connection name.
    returned: On success when C(state=present)
    type: str
    sample: "vpc_peering1"
status:
    description: Specifies the VPC peering connection status.
    returned: On success when C(state=present)
    type: str
    sample: "accepted"
request_vpc_info:
    description: Dictionary describing the local vpc.
    returned: On success when C(state=present)
    type: complex
    contains:
        vpc_id:
            description: Specifies the ID of a VPC involved in a VPC peering connection.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        project_id:
            description: Specifies the ID of the project to which a VPC involved in the VPC peering connection belongs.
            type: str
            sample: "45007a7e-ee4f-4d13-8283-b4da2e037c69"
accept_vpc_info:
    description: Dictionary describing the local vpc.
    returned: On success when C(state=present)
    type: complex
    contains:
        vpc_id:
            description: Specifies the ID of a VPC involved in a VPC peering connection.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        project_id:
            description: Specifies the ID of the project to which a VPC involved in the VPC peering connection belongs.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
description:
    description: Provides supplementary information about the VPC peering connection.
    returned: On success when C(state=present)
    type: str
    sample: ""
created_at:
    description: Specifies the time (UTC) when the VPC peering connection is created.
    returned: On success when C(state=present)
    type: str
    sample: "2020-09-13T20:38:02"
updated_at:
    description: Specifies the time (UTC) when the VPC peering connection is updated.
    returned: On success when C(state=present)
    type: str
    sample: "2020-09-13T20:38:02"
'''

EXAMPLES = '''
# Create a vpc peering.
- vpc_peering:
    name: "peering1"
    local_router: "local-router"
    project_id_local: "959db9b6017d4a1fa1c6fd17b6820f55"
    peer_router: "peer-router"
    project_id_peer: "959db9b6017d4a1fa1c6fd17b6820f55"

# Change name of the vpc peering
- vpc_peering:
    name: "peering1"
    new_name: "peering2"
    local_router: "local-router"
    project_id_local: "959db9b6017d4a1fa1c6fd17b6820f55"
    peer_router: "peer-router"
    project_id_peer: "959db9b6017d4a1fa1c6fd17b6820f55"

# Delete a load balancer(and all its related resources)
- vpc_peering:
    name: "peering2"
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VPCPeeringModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True, type='str'),
        state=dict(default='present', choices=['absent', 'present']),
        local_router=dict(type='str'),
        project_id_local=dict(type='str'),
        peer_router=dict(type='str'),
        project_id_peer=dict(type='str'),
        new_name=dict(type='str'),
        description=dict(type='str', default="")
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['local_router', 'project_id_local', 'peer_router', 'project_id_peer'])
        ]
    )

    def _system_state_change(self, obj):
        state = self.params['state']
        if state == 'present':
            if not object:
                return True
        elif state == 'absent' and obj:
            return True
        return False

    def _check_peering(self, local_vpc_id, peer_vpc_id):

        result = True
        peerings = []

        for raw in self.conn.vpc.peerings():
            dt = raw.to_dict()
            dt.pop('location')
            peerings.append(dt)

        if peerings:
            for peering in peerings:
                if (peering['local_vpc_info']['vpc_id'] == local_vpc_id and peering['peer_vpc_info']['vpc_id'] == peer_vpc_id) or \
                        (peering['local_vpc_info']['vpc_id'] == peer_vpc_id and peering['peer_vpc_info']['vpc_id'] == local_vpc_id):
                    result = False

        return result

    def run(self):
        name = self.params['name']
        local_router = self.params['local_router']
        project_id_local = self.params['project_id_local']
        peer_router = self.params['peer_router']
        project_id_peer = self.params['project_id_peer']
        new_name = self.params['new_name']
        description = self.params['description']

        changed = False
        vpc_peering = None

        try:
            vpc_peering = self.conn.vpc.find_peering(name)
        except self.sdk.exceptions.ResourceNotFound:
            pass

        if self.ansible.check_mode:
            self.exit_json(changed=self._system_state_change(vpc_peering))

        if new_name:
            attrs = {'name': new_name}
            if vpc_peering:
                updated_vpc_peering = self.conn.vpc.update_peering(vpc_peering, **attrs)
                changed = True
                self.exit_json(
                    changed=changed,
                    vpc_peering=updated_vpc_peering
                )
            else:
                self.fail_json(
                    msg="A VPC peering with this name doesn't exist"
                )

        if self.params['state'] == 'present':

            local_vpc = self.conn.network.find_router(local_router)
            peer_vpc = self.conn.network.find_router(peer_router)

            local_vpc_id = local_vpc['id']
            peer_vpc_id = peer_vpc['id']

            if not vpc_peering:

                attrs = {
                    'name': name
                }

                local_vpc = {'vpc_id': local_vpc_id, 'project_id': project_id_local}
                attrs['local_vpc_info'] = local_vpc
                peer_vpc = {'vpc_id': peer_vpc_id, 'project_id': project_id_peer}
                attrs['peer_vpc_info'] = peer_vpc

                if description:
                    attrs['description'] = self.params['description']

                if self._check_peering(local_vpc_id, peer_vpc_id):
                    vpc_peering = self.conn.vpc.create_peering(**attrs)
                    changed = True

                    self.exit_json(
                        changed=changed,
                        vpc_peering=vpc_peering
                    )
                else:
                    self.fail_json(
                        msg="A VPC peering connection already exists between the two VPCs."
                    )
            else:
                self.fail_json(
                    msg="VPC peering with this name already exists"
                )

        elif self.params['state'] == 'absent':
            if vpc_peering:
                self.conn.vpc.delete_peering(vpc_peering)
                changed = True
                self.exit_json(
                    changed=changed,
                    result="Resource was deleted"
                )

            else:
                self.fail_json(
                    msg="Resource with this name doesn't exist"
                )


def main():
    module = VPCPeeringModule()
    module()


if __name__ == '__main__':
    main()
