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
module: deh_host_info
short_description: Get Dedicated host info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Tino Schreiber (@tischrei)"
description:
  - Get Dedicated host info.
options:
  availability_zone:
    description:
      - Availability zone of the Dedicated host.
    type: str
  changes_since:
    description:
      - Filters the response by date and timestamp when the DeH status
      - changes.
    type: str
  flavor:
    description:
      - Flavor of the Dedicated host.
    type: str
  host:
    description:
      - Name or ID of the Dedicated host.
    type: str
  host_type:
    description:
      - Type of the dedicated host
    type: str
  host_type_name:
    description:
      - Specifies the name of the host type.
    type: str
  instance_uuid:
    description:
      - Specifies the ID of a running VM on this Dedicated host.
    type: str
  released_at:
    description:
      - Specifies the time when the DeH is released.
    type: str
  status:
    description:
      - Specifies the status (state) of the Dedicated Host
    type: str
    choices: ["available", "fault", "released"]
  tags:
    description:
      - Specifies the tags of the Dedicated Host
    type: list
    elements: str

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
deh_hosts:
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


class DehHostInfoModule(OTCModule):
    argument_spec = dict(
        availability_zone=dict(required=False),
        changes_since=dict(required=False),
        flavor=dict(required=False),
        host=dict(required=False),
        host_type=dict(required=False),
        host_type_name=dict(required=False),
        instance_uuid=dict(required=False),
        released_at=dict(required=False),
        status=dict(required=False, choices=["available",
                                             "fault",
                                             "released"]),
        tags=dict(required=False, type='list', elements='str')
    )

    def run(self):

        data = []
        query = {}

        if self.params['host']:
            deh = self.conn.deh.find_host(
                name_or_id=self.params['host'],
                ignore_missing=True)
            if deh:
                query['id'] = deh.id
            else:
                self.exit(
                    changed=False,
                    deh_hosts=[],
                    message=('No DEH host found with name or id: %s' %
                             self.params['host'])
                )

        if self.params['availability_zone']:
            query['availability_zone'] = self.params['availability_zone']
        if self.params['changes_since']:
            query['changes_since'] = self.params['changes_since']
        if self.params['flavor']:
            query['flavor'] = self.params['flavor']
        if self.params['host_type']:
            query['host_type'] = self.params['host_type']
        if self.params['host_type_name']:
            query['host_type_name'] = self.params['host_type_name']
        if self.params['instance_uuid']:
            query['instance_uuid'] = self.params['instance_uuid']
        if self.params['released_at']:
            query['released_at'] = self.params['released_at']
        if self.params['status']:
            query['status'] = self.params['status']
        if self.params['tags']:
            query['tags'] = self.params['tags']

        for raw in self.conn.deh.hosts(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            deh_hosts=data
        )


def main():
    module = DehHostInfoModule()
    module()


if __name__ == '__main__':
    main()
