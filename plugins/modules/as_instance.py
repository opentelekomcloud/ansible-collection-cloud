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
module: as_instance
short_description: Managing Instances in an AS Group.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.0"
author: "Irina Pereiaslavskaia (@irina-pereiaslavskaia)"
description:
  - This interface is used to manage Instances in an AS Group.
options:
  scaling_group:
    description:
      - Specifies the auto-scaling group name or ID.
    type: str
    required: true
  scaling_instances:
    description:
      - Specifies the instance names or IDs.
    type: list
    elements: str
    required: true
  instance_delete:
    description:
      - Specifies whether an instance is deleted when it is removed from the AS group.
    choices: [yes, no]
    type: str
    default: "no"
  action:
    description:
      - Specifies an action to be performed on instances in batches.
    choices: [add, remove, protect, unprotect]
    type: str
  state:
    description:
      - Whether resource should be present or absent.
    choices: [present, absent]
    type: str
    default: "present"
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
# This module does not return anything.
'''

EXAMPLES = '''
# Remove Instance in an AS Group
- opentelekomcloud.cloud.as_instance:
    scaling_group: "test_group"
    scaling_instance: "89af599d-a8ab-4c29-a063-0b719ed77e8e"
    state: "absent"
  register: as_instance
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class ASInstanceModule(OTCModule):
    argument_spec = dict(
        scaling_group=dict(type='str', required=True),
        scaling_instances=dict(type='list', elements='str', required=True),
        instance_delete=dict(type='str', choices=['yes', 'no'], default='no'),
        action=dict(type='str', choices=['add', 'remove', 'protect', 'unprotect']),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode = True
    )

    def _is_group_in_inservice_state(self, group):
        if group.status == 'INSERVICE':
            return True
        else:
            return False

    def _get_max_number_of_instances(self, group):
        return group.max_instance_number

    def _get_min_number_of_instances(self, group):
        return group.min_instance_number

    def _get_current_instance_number(self, group):
        return group.current_instance_number

    def _is_instance_in_inservice_state(self, instance):
        if instance.lifecycle_state == 'INSERVICE':
            return True
        else:
            return False

    def _get_instances_for_adding(self, as_instances):
        instances = []
        for as_instance in as_instances:
            instance = self.sdk.compute.find_server(
                name_or_id=as_instance
            )
            if instance:
                instances.append(instance)
        return instances

    def _get_instances_for_removing_or_protecting(self, group, as_instances):
        instances = []
        for as_instance in as_instances:
            instance = self.conn.auto_scaling.find_instance(
                group=group,
                name_or_id=as_instance
            )
            if instance and self._is_instance_in_inservice_state(instance):
                instances.append(instance)
            elif not instance and len(as_instances) == 1:
                self.fail(
                    changed=False,
                    msg='Instance %s not found' % instance
                )
        return instances

    def run(self):
        as_group = self.params['scaling_group']
        as_instances = self.params['scaling_instances']
        instance_delete = self.params['instance_delete']
        action = self.params['action']
        state = self.params['state']

        try:
            group = self.conn.auto_scaling.find_group(
                name_or_id=as_group,
                ignore_missing=False
            )

        except self.sdk.exceptions.ResourceNotFound:
            self.fail(
                changed=False,
                msg='Scaling group %s not found' % as_group
            )

        if state == 'present':

            if action is None:
                self.exit(
                    changed=False,
                    msg='Instances not changed'
                )
            elif action.upper() == 'REMOVE':
                self.fail(
                    changed=False,
                    msg='Action is incompatible with this state'
                )
            else:
                instances = self._get_instances_for_removing_or_protecting(group, as_instances)
                self.conn.auto_scaling.batch_instance_action(
                    group=group,
                    instances=instances,
                    action=action.upper()
                )
                self.exit(
                    changed = True,
                    msg = 'Action %s was done' % action.upper()
                )

        else:

            instances = self._get_instances_for_removing_or_protecting(group, as_instances)
            if action is None:
                if len(as_instances) == 1:
                    if len(instances) == 1:
                        self.conn.auto_scaling.remove_instance(
                            instance=instances[0],
                            delete_instance=instance_delete
                        )
                        self.exit(
                            changed=True,
                            msg='Instance %s was removed' % as_instances[0]
                        )
                    else:
                        self.fail(
                            changed=False,
                            msg='Instance is not in INSERVICE state'
                        )
                else:
                    self.exit(
                        changed=False,
                        msg='Instances not changed'
                    )
            elif action.upper() == 'REMOVE':
                self.conn.auto_scaling.batch_instance_action(
                    group=group,
                    instances=instances,
                    action=action.upper()
                )
                self.exit(
                    changed=True,
                    msg='Action %s was done' % action.upper()
                )
            else:
                self.fail(
                    changed=False,
                    msg='Action is incompatible with this state'
                )


def main():
    module = ASInstanceModule()
    module()


if __name__ == '__main__':
    main()
