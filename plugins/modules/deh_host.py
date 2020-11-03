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
module: deh_host
short_description: Manage Dedicated Hosts on Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Tino Schreiber (@tischrei)"
description:
  - Manage Dedicated Hosts on Open Telekom Cloud
options:
  auto_placement:
    description:
      - Specifies whether to allow an ECS to be placed on any available DeH if
      - its DeH ID is not specified during its creation.
    type: str
    default: 'on'
    choices: ['on', 'off']
  availability_zone:
    description:
      - Specifies the Availability zone to which the Dedicated host belongs.
      - Mandatory for DeH creation.
    type: str
  host_type:
    description:
      - Specifies the DeH type.
      - Mandatory for DeH creation.
    type: str
  id:
    description:
      - ID of the DeH.
      - Parameter is usable for update or deletion of a DeH host.
    type: str
  name:
    description:
      - Name or ID of the DeH.
      - Mandatory for DeH creation.
    type: str
  quantity:
    description:
      - Number of DeHs to allocate.
    type: int
    default: 1
  tags:
    description:
      - Specifies the DeH tags.
    type: list
    elements: dict
  state:
    choices: [present, absent]
    default: present
    description: Instance state
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
deh_host:
    description: Dictionary of DeH hosts
    returned: changed
    type: list
    sample: [
      {
          "allocated_at": "2020-09-30T09:38:15Z",
          "auto_placement": "on",
          "availability_zone": "az01",
          "available_memory": 334848,
          "available_vcpus": 71,
          "dedicated_host_ids": null,
          "host_properties": {
              "available_instance_capacities": [
                  {
                      "flavor": "s2.8xlarge.2",
                      "id": null,
                      "location": null,
                      "name": null
                  },
                  {
                      "flavor": "s2.8xlarge.1",
                      "id": null,
                      "location": null,
                      "name": null
                  }
              ],
              "cores": 12,
              "host_type": "s2-medium",
              "host_type_name": "s2-medium",
              "id": null,
              "location": null,
              "memory": 335872,
              "name": null,
              "sockets": 2,
              "vcpus": 72
          },
          "host_type": null,
          "id": "9b20bd80-c1aa-438c-a499-f5b5308ac123",
          "instance_total": 1,
          "instance_uuids": [
              "a0c4d7d6-a2ae-4519-92d9-f0780e6f1123"
          ],
          "name": "deh-name",
          "project_id": "16d53a84a13b49529d2e2c3646691123",
          "quantity": null,
          "released_at": "",
          "state": "available",
          "tags": [
                {
                    "mytag": "myvalue",
                    "yourtag": "yourvalue"
                }
          ]
      }
    ]
'''

EXAMPLES = '''
# Query all DeH hosts
- opentelekomcloud.cloud.deh_host_info:
    cloud: "{{ test_cloud }}"
  register: deh

# Query specific Dedicated host by ID
- opentelekomcloud.cloud.deh_host_info:
    cloud: "{{ test_cloud }}"
    host: "9b20bd80-c1aa-438c-a499-f5b5308ac123"
  register: deh

# Query DeH hosts with flavor s2-medium
- opentelekomcloud.cloud.deh_host_info:
    cloud: "{{ test_cloud }}"
    host_type: "s2-medium"
  register: deh

# Query all parameters
- opentelekomcloud.cloud.deh_host_info:
    cloud: "{{ test_cloud }}"
    availability_zone: az01
    flavor: s2.medium.8
    instance_uuid: a0c4d7d6-a2ae-4519-92d9-f0780e6f1123
    host: "9b20bd80-c1aa-438c-a499-f5b5308ac123"
    released_at: ""
    tags: [mytag, yourtag]
    host_type: "s2-medium"
    host_type_name: "s2-medium"
  register: deh

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DehHostModule(OTCModule):
    argument_spec = dict(
        auto_placement=dict(required=False,
                            default='on',
                            choices=['on', 'off']),
        availability_zone=dict(required=False),
        host_type=dict(required=False),
        id=dict(required=False),
        name=dict(required=False),
        quantity=dict(required=False, type='int', default=1),
        tags=dict(required=False, type='list', elements='dict'),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )

    def _system_state_change(self, obj):
        state = self.params['state']
        if state == 'present':
            if not obj:
                return True
        elif state == 'absent' and obj:
            return True
        return False

    def run(self):
        changed = False
        hosts = []
        host = ''

        # The following stuff needs to be done due to missing implementation
        # of proper API to use find method.
        if self.params['id']:
            host = self.conn.deh.get_host(host=self.params['id'])
        else:
            for obj in self.conn.deh.hosts(name=self.params['name']):
                if obj:
                    hosts.append(obj)
                    break
            # Check is necessary to avoid Modification of DeH resources
            # with the same prefix like
            # self.params['name'] = 'test'
            # and
            # hosts[0].name = 'test-host'
            # which would result in modification of wrong host.
            if hosts and (self.params['name'] == hosts[0].name):
                host = self.conn.deh.get_host(host=hosts[0].id)

        if self.ansible.check_mode:
            self.exit(changed=self._system_state_change(host))

        # Host deletion
        if self.params['state'] == 'absent':
            changed = False

            if host:
                self.conn.deh.delete_host(host)
                changed = True

        # Host creation and modification
        elif self.params['state'] == 'present':
            changed = False
            attrs = {}

            if host:
                # DeH host modification
                if self.params['auto_placement'] and (self.params['auto_placement'] != host.auto_placement):
                    attrs['auto_placement'] = self.params['auto_placement']
                if self.params['name'] and (self.params['name'] != host.name):
                    attrs['name'] = self.params['name']
                if attrs:
                    host = self.conn.deh.update_host(host=host, **attrs)
                    host = host.to_dict()
                    host.pop('location')
                    self.exit(changed=True, deh_host=host)
            else:
                # DeH host creation
                if not self.params['name'] or not self.params['availability_zone'] or not self.params['host_type']:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('One of the mandatory paramaters: name, '
                                 'availability_zone or host_type '
                                 'is missing for DeH allocation.')
                    )
                attrs['name'] = self.params['name']
                if self.params['auto_placement']:
                    attrs['auto_placement'] = self.params['auto_placement']
                attrs['availability_zone'] = self.params['availability_zone']
                attrs['host_type'] = self.params['host_type']
                if self.params['quantity']:
                    attrs['quantity'] = self.params['quantity']
                if self.params['tags']:
                    attrs['tags'] = self.params['tags']
                host = self.conn.deh.create_host(**attrs)
                if host:
                    host = host.to_dict()
                    host.pop('location')
                else:
                    self.exit(
                        changed=changed,
                        failed=True,
                        message=('Host creation failed.')
                    )
                self.exit(changed=True, deh_host=host)
        self.exit(changed=changed)


def main():
    module = DehHostModule()
    module()


if __name__ == "__main__":
    main()
