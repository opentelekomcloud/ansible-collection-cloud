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
module: security_group
short_description: Add/Delete security groups from an OpenTelekomCloud cloud.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.9.0"
author: "Vladimir Vshivkov (@enrrou)"
description:
   - Add or Remove security groups from an OpenTelekomCloud cloud.
options:
   name:
     description:
        - Name that has to be given to the security group. This module
          requires that security group names be unique.
     required: true
     type: str
   description:
     description:
        - Long description of the purpose of the security group
     type: str
   state:
     description:
       - Should the resource be present or absent.
     choices: [present, absent]
     default: present
     type: str
   project:
     description:
        - Unique name or ID of the project.
     required: false
     type: str
requirements:
    - "python >= 3.6"
    - "openstacksdk"
    - "otcextensions"
'''

EXAMPLES = '''
# Create a security group
- opentelekomcloud.cloud.security_group:
    cloud: otc
    state: present
    name: foo
    description: security group for foo servers

# Update the existing 'foo' security group description
- opentelekomcloud.cloud.security_group:
    cloud: otc
    state: present
    name: foo
    description: updated description for the foo security group

# Create a security group for a given project
- opentelekomcloud.cloud.security_group:
    cloud: otc
    state: present
    name: foo
    project: myproj
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SecurityGroupModule(OTCModule):

    argument_spec = dict(
        name=dict(required=True),
        description=dict(default=''),
        state=dict(default='present', choices=['absent', 'present']),
        project=dict(default=None),
    )

    def _needs_update(self, secgroup):
        """Check for differences in the updatable values.

        NOTE: We don't currently allow name updates.
        """
        if secgroup['description'] != self.params['description']:
            return True
        return False

    def _system_state_change(self, secgroup):
        state = self.params['state']
        if state == 'present':
            if not secgroup:
                return True
            return self._needs_update(secgroup)
        if state == 'absent' and secgroup:
            return True
        return False

    def run(self):

        name = self.params['name']
        state = self.params['state']
        description = self.params['description']
        project = self.params['project']

        if project is not None:
            proj = self.conn.get_project(project)
            if proj is None:
                self.fail_json(msg='Project %s could not be found' % project)
            project_id = proj['id']
        else:
            project_id = self.conn.current_project_id

        if project_id:
            filters = {'tenant_id': project_id}
        else:
            filters = None

        secgroup = self.conn.get_security_group(name, filters=filters)

        if self.ansible.check_mode:
            self.exit(changed=self._system_state_change(secgroup))

        changed = False
        if state == 'present':
            if not secgroup:
                kwargs = {}
                if project_id:
                    kwargs['project_id'] = project_id
                secgroup = self.conn.create_security_group(name, description,
                                                           **kwargs)
                changed = True
            else:
                if self._needs_update(secgroup):
                    secgroup = self.conn.update_security_group(
                        secgroup['id'], description=description)
                    changed = True
            self.exit(
                changed=changed, id=secgroup['id'], secgroup=secgroup)

        if state == 'absent':
            if secgroup:
                self.conn.delete_security_group(secgroup['id'])
                changed = True
            self.exit(changed=changed)


def main():
    module = SecurityGroupModule()
    module()


if __name__ == '__main__':
    main()
