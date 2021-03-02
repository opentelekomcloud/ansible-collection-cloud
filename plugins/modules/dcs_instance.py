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
module: dcs_instance
short_description: Manage DCS Instances on Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Manage DCS Instances on Open Telekom Cloud
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
    description: Dictionary of DeH host
    returned: changed
    type: dict
    sample: {
        deh_host: {
          "allocated_at": null,
          "auto_placement": "on",
          "availability_zone": "eu-de-01",
          "available_memory": null,
          "available_vcpus": null,
          "dedicated_host_ids": [
              "6d113075-038c-403c-b9cd-fc567f1fd123"
          ],
          "host_properties": null,
          "host_type": "s2-medium",
          "id": null,
          "instance_total": null,
          "instance_uuids": null,
          "name": "deh-host",
          "project_id": null,
          "quantity": 1,
          "released_at": null,
          "status": null,
          "tags": [
              {
                  "key": "key1",
                  "value": "value1"
              },
              {
                  "key": "key2",
                  "value": "value2"
              }
          ]
        }
    }
'''

EXAMPLES = '''
# Allocate Dedicated host
- opentelekomcloud.cloud.deh_host:
    cloud: otc
    availability_zone: eu-de-01
    host_type: s2-medium
    name: "{{ deh_host_name }}"
    state: present
    quantity: 1
    tags:
      - key: key1
        value: value1
      - key: key2
        value: value2
  register: deh

# Modify Dedicated Host
- opentelekomcloud.cloud.deh_host:
    cloud: otc
    id: "{{ deh.deh_host.dedicated_host_ids[0] }}"
    auto_placement: off
  when:
    - deh is defined
  register: deh
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DehHostModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
        id=dict(required=False),
        description=dict(required=False),
        engine=dict(required=False, default='Redis'),
        engine_version=dict(required=False, default='3.0'),
        capacity=dict(required=False, type='int', default=2),
        password=dict(required=False),
        vpc_id=dict(required=False),
        security_group_id=dict(required=False),
        subnet_id=dict(required=False),
        available_zones=dict(required=False, type='list'),
        product_id=dict(required=False),
        instance_backup_policy=dict(required=False, type='dict'),
        maintain_begin=dict(required=False),
        maintain_end=dict(required=False),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        changed = False
        query = {}
        if self.params['id']:
            nameid = self.params['id']
        elif self.params['name']:
            nameid = self.params['name']
        else:
            self.exit(
                changed=False,
                message=('No Name or ID provided, but required!'),
                failed=True
            )

        instance = self.conn.dcs.find_instance(
            name_or_id=nameid,
            ignore_missing=True
        )

        # Instance Deletion
        if self.params['state'] == 'absent':
            if instance:
                if self.ansible.check_mode:
                    self.exit(changed=True)
                dcs_instance = self.conn.dcs.delete_instance(instance.id)
                self.exit(changed=True, dcs_instance=dcs_instance)

        if self.params['state'] == 'present':
            attrs = {}
            # Modifying an Instance
            if instance:
                # Scaling up
                if instance.to_dict()['capacity'] < self.params['capacity']:
                    if self.ansible.check_mode:
                        self.exit(changed=True)
                    dcs_instance = self.conn.dcs.extend_instance(instance.id, self.params['capacity'])
                    self.exit(changed=True, dcs_instance=dcs_instance.to_dict(), message='Scaling instance up, ignoring other params')
                elif instance.to_dict()['capacity'] > self.params['capacity']:
                    self.exit(
                        changed=False,
                        message=('''When extending an DCS Instance the capacity needs to be larger!
                                The Instance has a capacity of %s and new provided capacity was %s'''
                                 % (instance.to_dict()['capacity'], self.params['capacity'])),
                        failed=True
                    )
                # Changing other params
                elif instance.to_dict()['capacity'] == self.params['capacity']:
                    changed = False
                    if instance.to_dict()['name'] != self.params['name']:
                        changed = True
                        attrs['name'] = self.params['name']
                    if instance.to_dict()['description'] != self.params['description']:
                        changed = True
                        attrs['description'] = self.params['description']
                    if instance.to_dict()['security_group_id'] != self.params['security_group_id']:
                        changed = True
                        attrs['security_group_id'] = self.params['security_group_id']
                    if (instance.to_dict()['maintain_begin'] != self.params['maintain_begin']) and \
                       (instance.to_dict()['maintain_end'] != self.params['maintain_end']):
                        changed = True
                        attrs['maintain_begin'] = self.params['maintain_begin']
                        attrs['maintain_end'] = self.params['maintain_end']
                    elif (instance.to_dict()['maintain_begin'] != self.params['maintain_begin']) or \
                         (instance.to_dict()['maintain_end'] != self.params['maintain_end']):
                        self.exit(
                            changed=False,
                            message=('''You need to specify maintain_begin and maintain_end when trying to change one of them'''),
                            failed=True
                        )
                    # The Query API currently will always give a NULL response for backup_policy so this will always result in "changed"
                    # There's no way to go around this
                    if instance.to_dict()['backup_policy'] != self.params['instance_backup_policy']:
                        changed = True
                        instance_backup_policy_var = self.params['instance_backup_policy']
                        # In case the user didn't specify timezone_offset or something we need to give the API an null type so it won't throw an error
                        try:
                            var = (instance_backup_policy_var['periodical_backup_plan']['timezone_offset'])
                        except Exception:
                            instance_backup_policy_var['periodical_backup_plan']['timezone_offset'] = None
                        try:
                            var = (instance_backup_policy_var['save_days'])
                        except Exception:
                            instance_backup_policy_var['save_days'] = None
                        try:
                            var = (instance_backup_policy_var['backup_type'])
                        except Exception:
                            instance_backup_policy_var['backup_type'] = None

                        attrs['instance_backup_policy'] = {
                            "save_days": instance_backup_policy_var['save_days'],
                            "backup_type": instance_backup_policy_var['backup_type'],
                            "periodical_backup_plan": {
                                "begin_at": instance_backup_policy_var['periodical_backup_plan']['begin_at'],
                                "period_type": instance_backup_policy_var['periodical_backup_plan']['period_type'],
                                "backup_at": instance_backup_policy_var['periodical_backup_plan']['backup_at'],
                                "timezone_offset": instance_backup_policy_var['periodical_backup_plan']['timezone_offset']
                            }
                        }

                    if self.ansible.check_mode:
                        self.exit(changed=True)
                    dcs_instance = self.conn.dcs.update_instance(instance.id, **attrs)
                    self.exit(changed=True, dcs_instance=dcs_instance.to_dict())

            # Creating a new Instance
            if not instance:
                if self.params['name']:
                    name_var = self.params['name']
                else:
                    self.exit(
                        changed=False,
                        message=('No name param provided, but required!'),
                        failed=True
                    )
                if self.params['engine']:
                    engine_var = self.params['engine']
                else:
                    self.exit(
                        changed=False,
                        message=('No engine param provided, but required!'),
                        failed=True
                    )
                if self.params['engine_version']:
                    engine_version_var = self.params['engine_version']
                else:
                    self.exit(
                        changed=False,
                        message=('No engine_version param provided, but required!'),
                        failed=True
                    )
                if self.params['capacity']:
                    capacity_var = self.params['capacity']
                else:
                    self.exit(
                        changed=False,
                        message=('No capacity param provided, but required!'),
                        failed=True
                    )
                if self.params['password']:
                    password_var = self.params['password']
                else:
                    self.exit(
                        changed=False,
                        message=('No password param provided, but required!'),
                        failed=True
                    )
                if self.params['vpc_id']:
                    vpc_id_var = self.params['vpc_id']
                else:
                    self.exit(
                        changed=False,
                        message=('No vpc_id param provided, but required!'),
                        failed=True
                    )
                if self.params['security_group_id']:
                    security_group_id_var = self.params['security_group_id']
                else:
                    self.exit(
                        changed=False,
                        message=('No security_group_id param provided, but required!'),
                        failed=True
                    )
                if self.params['subnet_id']:
                    subnet_id_var = self.params['subnet_id']
                else:
                    self.exit(
                        changed=False,
                        message=('No subnet_id param provided, but required!'),
                        failed=True
                    )
                if self.params['available_zones']:
                    available_zones_var = self.params['available_zones']
                else:
                    self.exit(
                        changed=False,
                        message=('No available_zones param provided, but required!'),
                        failed=True
                    )
                if self.params['product_id']:
                    product_id_var = self.params['product_id']
                else:
                    self.exit(
                        changed=False,
                        message=('No product_id param provided, but required!'),
                        failed=True
                    )
                if self.params['maintain_begin'] and self.params['maintain_end']:
                    maintain_begin_var = self.params['maintain_begin']
                    maintain_end_var = self.params['maintain_end']
                else:
                    maintain_begin_var = None
                    maintain_end_var = None

                attrs = {
                    "name": self.params['name'],
                    "description": self.params['description'],
                    "engine": engine_var,
                    "engine_version": engine_version_var,
                    "capacity": capacity_var,
                    "password": password_var,
                    "vpc_id": vpc_id_var,
                    "security_group_id": security_group_id_var,
                    "subnet_id": subnet_id_var,
                    "available_zones": available_zones_var,
                    "product_id": product_id_var,
                    "maintain_begin": maintain_begin_var,
                    "maintain_end": maintain_end_var,
                }
                if self.params['instance_backup_policy']:
                    instance_backup_policy_var = self.params['instance_backup_policy']
                    # In case the user didn't specify timezone_offset or something we need to give the API an null type so it won't throw an error
                    try:
                        var = (instance_backup_policy_var['periodical_backup_plan']['timezone_offset'])
                    except Exception:
                        instance_backup_policy_var['periodical_backup_plan']['timezone_offset'] = None
                    try:
                        var = (instance_backup_policy_var['save_days'])
                    except Exception:
                        instance_backup_policy_var['save_days'] = None
                    try:
                        var = (instance_backup_policy_var['backup_type'])
                    except Exception:
                        instance_backup_policy_var['backup_type'] = None

                    attrs['instance_backup_policy'] = {
                        "save_days": instance_backup_policy_var['save_days'],
                        "backup_type": instance_backup_policy_var['backup_type'],
                        "periodical_backup_plan": {
                            "begin_at": instance_backup_policy_var['periodical_backup_plan']['begin_at'],
                            "period_type": instance_backup_policy_var['periodical_backup_plan']['period_type'],
                            "backup_at": instance_backup_policy_var['periodical_backup_plan']['backup_at'],
                            "timezone_offset": instance_backup_policy_var['periodical_backup_plan']['timezone_offset']
                        }
                    }
                if self.ansible.check_mode:
                    self.exit(changed=True)
                dcs_instance = self.conn.dcs.create_instance(**attrs)
                self.exit(changed=True, dcs_instance=dcs_instance.to_dict())

        self.exit(
            changed=changed
        )


def main():
    module = DehHostModule()
    module()


if __name__ == "__main__":
    main()
