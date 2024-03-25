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
module: log_stream
short_description: Manage LTS stream
extends_documentation_fragment: opentelekomcloud.cloud.otc
author: "Polina Gubina (@polina-gubina)"
version_added: "0.11.0"
description:
   - Manage (create or delete) Open Telekom Cloud LTS stream.
options:
  state:
    description: Indicate desired state of the resource.
    choices: ['present', 'absent']
    default: present
    type: str
  log_group_id:
    description:
      - Specifies the log group id.
    type: str
    required: True
  name:
    description:
      - Specifies the log group stream. Mandatory for create.
    type: str
  id:
    description:
      - Specifies the log stream ID. Mandatory for update.
    type: str
requirements: ['openstacksdk', 'otcextensions']
'''

EXAMPLES = '''
- name: Create log stream
  opentelekomcloud.cloud.log_stream:
    name: "test-log-stream"
    log_group_id: "27b78d92-cee1-4646-b831-e3b90a7fa714"
  register: vpc

- name: Delete log stream
  opentelekomcloud.cloud.log_stream:
    log_group_id: "27b78d92-cee1-4646-b831-e3b90a7fa714"
    id: "48b12d92-rte4-4646-b831-r5b90a7fa739"

'''

RETURN = '''
log_stream:
    description: Created log stream resource.
    returned: On success when I(state=present)
    type: complex
    contains:
        log_stream_id:
            description: Specifies the resource identifier in the form of UUID.
            type: str
            sample: "0f21367c-022d-433e-8ddb-1c31a65a05b8"
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LogStreamModule(OTCModule):
    argument_spec = dict(
        state=dict(default='present', choices=['absent', 'present']),
        log_group_id=dict(type='str', required=True),
        name=dict(type='str', required=False),
        id=dict(type='str', required=False)
    )

    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['name']),
        ],
        supports_check_mode=True
    )

    def run(self):

        state = self.params['state']
        name = self.params['name']
        id = self.params['id']
        log_group_id = self.params['log_group_id']

        if not name and not id:
            self.fail_json(msg='name or id is mandatory')

        existing = self.get_log_stream_by_name_or_id(log_group_id=log_group_id,
                                                     name=name, id=id)

        if state == 'present':
            if existing:
                self.exit(changed=False)
            else:
                if not name:
                    self.fail_json(msg='name is mandatory for creation')
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                log_stream = self.conn.lts.create_stream(log_stream_name=name,
                                                         log_group=log_group_id)
                self.exit(changed=True, log_stream=log_stream)
        elif state == 'absent':
            if not existing:
                self.exit(changed=False)
            if self.ansible.check_mode:
                self.exit_json(changed=True)
            self.conn.lts.delete_stream(log_group=log_group_id,
                                        log_stream=existing.id)
            self.exit(changed=True)

    def get_log_stream_by_name_or_id(self, log_group_id, name=None, id=None):
        for stream in self.conn.lts.streams(log_group=log_group_id):
            if name:
                if stream.name == name:
                    return stream
            elif id:
                if stream.id == id:
                    return stream
        return None


def main():
    module = LogStreamModule()
    module()


if __name__ == '__main__':
    main()
