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
module: log_group
short_description: Manage LTS group
extends_documentation_fragment: opentelekomcloud.cloud.otc
author: "Polina Gubina (@polina-gubina)"
version_added: "0.11.0"
description:
   - Manage (create, update or delete) Open Telekom Cloud LTS group.
options:
  state:
    description: Indicate desired state of the resource.
    choices: ['present', 'absent']
    default: present
    type: str
  name:
    description:
      - Specifies the log group name. Mandatory for create.
    type: str
  id:
    description:
      - Specifies the log group ID. Mandatory for update.
    type: str
  ttl_in_days:
    description:
      - Log retention duration, in days (fixed to 7 days).
    type: int
requirements: ['openstacksdk', 'otcextensions>=0.24.5']
'''

EXAMPLES = '''
- name: Create log group
  opentelekomcloud.cloud.log_group:
    name: "test-log-group"
    ttl_in_days: 5
  register: vpc

- name: Update log group
  opentelekomcloud.cloud.log_group:
    id: "27b78d92-cee1-4646-b831-e3b90a7fa714"
    ttl_in_days: 7

- name: Delete log group
  opentelekomcloud.cloud.log_group:
    id: "27b78d92-cee1-4646-b831-e3b90a7fa714"
    state: absent
'''

RETURN = '''
log_group:
    description: Created log group resource.
    returned: On success when I(state=present)
    type: complex
    contains:
        log_group_id:
            description: Specifies the resource identifier in the form of UUID.
            type: str
            sample: "0f21367c-022d-433e-8ddb-1c31a65a05b8"
        log_group_name:
            description: Specifies the log group.
            type: str
        creation_time:
            description: Time when a log group was created.
            type: str
        ttl_in_days:
            description: Log retention duration, in days (fixed to 7 days).
            type: int
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LogGroupModule(OTCModule):
    argument_spec = dict(
        state=dict(default='present', choices=['absent', 'present']),
        name=dict(type='str', required=False),
        id=dict(type='str', required=False),
        ttl_in_days=dict(type='int', required=False),
    )

    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['ttl_in_days']),
        ],
        supports_check_mode=True
    )

    def run(self):

        state = self.params['state']
        name = self.params['name']
        id = self.params['id']

        if not name and not id:
            self.fail_json(msg='name or id is mandatory')

        existing = self.get_log_group_by_name_or_id(name=name, id=id)

        if state == 'present':
            ttl_in_days = self.params['ttl_in_days']
            log_group = None
            if existing:
                if existing:
                    if existing.ttl_in_days != ttl_in_days:
                        if self.ansible.check_mode:
                            self.exit_json(changed=True)
                        log_group = self.conn.lts.update_group(
                            group=existing.id, ttl_in_days=ttl_in_days)
                    else:
                        self.exit_json(changed=False)
            else:
                if not name:
                    self.fail_json(msg='name is mandatory for creation')
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                log_group = self.conn.lts.create_group(log_group_name=name,
                                                       ttl_in_days=ttl_in_days)
            self.exit(changed=True, log_group=log_group)
        elif state == 'absent':
            if not existing:
                self.exit(changed=False)
            if self.ansible.check_mode:
                self.exit_json(changed=True)
            self.conn.lts.delete_group(group=existing.id)
            self.exit(changed=True)

    def get_log_group_by_name_or_id(self, name=None, id=None):
        for group in self.conn.lts.groups():
            if name:
                if group.name == name:
                    return group
            elif id:
                if group.id == id:
                    return group
        return None


def main():
    module = LogGroupModule()
    module()


if __name__ == '__main__':
    main()
