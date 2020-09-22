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
module: vpc peering 
short_description: Add/Delete vpc peering connection from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
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
  local_vpc_id:
    description: ID of the local vpc.
    type: str
    sample: "59007a7e-ee4f-4d13-8283-b4da2e037c69"
  project_id_local_vpc:
    description: Specifies the ID of the project to which a local VPC belongs.
    type:  str
    sample: "89007a7e-ee4f-4d13-8283-b4da2e037c69"
  peer_vpc_id:
    description: ID of the peer vpc.
    type: str
    sample: "69007a7e-ee4f-4d13-8283-b4da2e037c69"
  project_id_peer_vpc:
    description: Specifies the ID of the project to which a peer VPC belongs.
    type: str
    sample: "90007a7e-ee4f-4d13-8283-b4da2e037c69"
  new name:
    description: Specifies a new name to an existing vpc peering.
    type: str
    sample: "New_name_for_vpc_peering_1"
  description:
    description: Provides supplementary information about the VPC peering connection.
    type: str
    sample: ""
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
id:
    description: Specifies the VPC peering connection ID.
    type: str
    sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
name:
    description: Specifies the VPC peering connection name.
    type: str
    sample: "vpc_peering1"
status:
    description: Specifies the VPC peering connection status.
    type: str
    sample: "accepted"
request_vpc_info:
    description: Dictionary describing the local vpc.
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
    type: str
    sample: ""
created_at:
    description: Specifies the time (UTC) when the VPC peering connection is created.
    type: str
    sample: "2020-09-13T20:38:02"
updated_at:
    description: Specifies the time (UTC) when the VPC peering connection is updated.
    type: str
    sample: "2020-09-13T20:38:02"
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class VPCPeeringModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True, type='str'),
        state=dict(default='present', choices=['absent', 'present']),
        local_vpc_id=dict(type='str'),
        project_id_local_vpc=dict(type='str'),
        peer_vpc_id=dict(type='str'),
        project_id_peer_vpc=dict(type='str'),
        new_name=dict(type='str'),
        description=dict(type='str', default="")
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['local_vpc_id', 'project_id_local_vpc', 'peer_vpc_id', 'project_id_peer_vpc'])
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

    def _check_peering(self):

        result = True

        local_vpc_id = self.params['local_vpc_id']
        peer_vpc_id = self.params['peer_vpc_id']

        peerings = []

        for raw in self.conn.vpc.peerings():
            dt = raw.to_dict()
            dt.pop('location')
            peerings.append(dt)

        if peerings:
            for peering in peerings:
                if (peering['local_vpc_info']['vpc_id'] == local_vpc_id and peering['peer_vpc_info']['vpc_id'] == peer_vpc_id) or\
                        (peering['local_vpc_info']['vpc_id'] == peer_vpc_id and peering['peer_vpc_info']['vpc_id'] == local_vpc_id):
                    result = False

        return result

    def run(self):
        name = self.params['name']
        local_vpc_id = self.params['local_vpc_id']
        project_id_local_vpc = self.params['project_id_local_vpc']
        peer_vpc_id = self.params['peer_vpc_id']
        project_id_peer_vpc = self.params['project_id_peer_vpc']
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

            if not vpc_peering:

                attrs = {
                    'name': name
                }

                local_vpc = {'vpc_id': local_vpc_id, 'project_id': project_id_local_vpc}
                attrs['local_vpc_info'] = local_vpc
                peer_vpc = {'vpc_id': peer_vpc_id, 'project_id': project_id_peer_vpc}
                attrs['peer_vpc_info'] = peer_vpc

                if description:
                    attrs['description'] = self.params['description']

                if self._check_peering():
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
                    msg="Resource with this name already exists"
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
