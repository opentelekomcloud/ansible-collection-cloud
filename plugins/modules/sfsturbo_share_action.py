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
module: sfsturbo_share_action
short_description: Action on sfs turbo share from Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
author: "Polina Gubina (@polina-gubina)"
version_added: "0.10.0"
description:
   - Extend capacity and change security group for share from
     Open Telekom Cloud.
options:
   id:
     description: Id of the share.
     required: false
     type: str
   name:
     description: Name of the share.
     required: false
     type: str
   new_size:
     description: New capacity size.
     required: false
     type: int
   security_group:
     description: Name or id of the security group.
     required: false
     type: str
   timeout:
     description:
       - Specifies the timeout.
     type: int
     default: 350
requirements: ["openstacksdk", "otcextensions"]
'''

EXAMPLES = '''
- name: Extend capacity vpc
  opentelekomcloud.cloud.sfsturbo_share_action:
    name: "share-test"
    new_size: 200

- name: Change security group
  opentelekomcloud.cloud.vpc:
    name: "share-test"
    security_group: default

'''

RETURN = '''
share:
    description: Share object.
    type: complex
    returned: On Success.
    contains:
      id:
        description: Specifies the ID of the SFS Turbo file system.
        type: str
      name:
        description: Specifies the name of the SFS Turbo file system.
        type: str
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SFSTurboShareAction(OTCModule):
    argument_spec = dict(
        id=dict(required=False),
        name=dict(required=False),
        new_size=dict(required=False, type='int'),
        security_group=dict(required=False),
        timoeut=dict(default=350, type='int')
    )
    module_kwargs = dict(
        required_if=[
            ('id', None, ['name']),
            ('name', None, ['id'])
        ],
        supports_check_mode=True
    )

    def build_update(self, share, security_group_id):
        if self.params['new_size']:
            if int(float(share.avail_capacity)) != self.params['new_size']:
                return True
        if security_group_id:
            if share.security_group_id != security_group_id:
                return True
        return False

    def run(self):

        name = self.params['name']
        id = self.params['id']
        new_size = self.params['new_size']
        security_group = self.params['security_group']
        timeout = self.params['timeout']
        security_group_id = None

        changed = False

        name_or_id = (id if id else name)
        share = self.conn.sfsturbo.find_share(name_or_id, ignore_missing=True)
        if not share:
            self.fail_json(msg='Share {0} not found'.format(name_or_id))

        if security_group:
            sec_group = self.conn.network.find_security_group(
                name_or_id=security_group, ignore_missing=True
            )
            if not sec_group:
                self.fail_json(msg='Security group {0} not found'.format(
                    security_group))
            security_group_id = sec_group.id

        is_need_update = self.build_update(share, security_group_id)

        if self.ansible.check_mode:
            self.exit(share=share, changed=is_need_update)

        if is_need_update:
            if new_size:
                share = self.conn.sfsturbo.extend_capacity(share=share.id,
                                                           new_size=new_size)
                self.conn.sfsturbo.wait_for_extend_capacity(share,
                                                            wait=timeout)
                changed = True

            if security_group_id:
                share = self.conn.sfsturbo.change_security_group(
                    share, security_group_id)
                self.conn.sfsturbo.wait_for_change_security_group(share,
                                                                  wait=timeout)
                changed = True

        self.exit(share=share, changed=changed)


def main():
    module = SFSTurboShareAction()
    module()


if __name__ == '__main__':
    main()
