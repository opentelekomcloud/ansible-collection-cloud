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
    type: bool
    default: 'no'
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
  timeout:
    description:
      - The duration in seconds that module should wait.
    default: 200
    type: int
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
        instance_delete=dict(type='bool', default=False),
        action=dict(type='str', choices=['add', 'remove', 'protect', 'unprotect']),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        timeout=dict(type='int', default=200)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def _system_state_change(self, instances, as_instances, state, action):
        if state == 'present':
            if action is None:
                return False
            elif action == 'remove':
                return False
            elif action == 'add':
                if instances:
                    return True
                else:
                    return False
            else:
                if instances:
                    return True
                else:
                    return False
        else:
            if instances:
                if action is None:
                    if len(as_instances) == 1:
                        if len(instances) == 1:
                            return True
                        else:
                            return False
                    else:
                        return False
                elif action == 'remove':
                    return True
                else:
                    return False

    def _is_group_in_inservice_state(self, group):
        if group.status.upper() == 'INSERVICE':
            return True
        else:
            return False

    def _is_instance_in_inservice_state(self, instance):
        if instance.lifecycle_state.upper() == 'INSERVICE':
            return True
        else:
            return False

    def _max_number_of_instances_for_adding(self, group):
        return group.max_instance_number - group.current_instance_number

    def _max_number_of_instances_for_removing(self, group):
        return group.current_instance_number - group.min_instance_number

    def _max_number_of_instances_for_protecting(self, group):
        return group.current_instance_number

    def _slice_list(self, init_list, part_size):
        return [init_list[i:i + part_size]
                for i in range(0, len(init_list), part_size)]

    def _get_instances_for_adding(self, group, as_instances):
        instances = []
        max_instances = self._max_number_of_instances_for_adding(group)
        for as_instance in as_instances:
            instance_ecs = self.sdk.compute.find_server(
                name_or_id=as_instance
            )
            instance_as_group = self.conn.auto_scaling.find_instance(
                group=group,
                name_or_id=as_instance
            )
            if (instance_ecs and
                    instance_ecs.availability_zone in group.availability_zones
                    and instance_as_group is None):
                instances.append(instance_ecs.id)
        if len(instances) <= max_instances:
            instances = self._slice_list(instances, 10)
        return instances

    def _get_instances_for_removing(self, group, as_instances):
        instances = []
        max_instances = self._max_number_of_instances_for_removing(group)
        for as_instance in as_instances:
            instance = self.conn.auto_scaling.find_instance(
                group=group,
                name_or_id=as_instance
            )
            if instance and self._is_instance_in_inservice_state(instance):
                instances.append(instance)
        if len(instances) <= max_instances:
            instances = self._slice_list(instances, 10)
        return instances

    def _get_instances_for_protection(self, group, as_instances):
        instances = []
        max_instances = self._max_number_of_instances_for_protecting(group)
        for as_instance in as_instances:
            instance = self.conn.auto_scaling.find_instance(
                group=group,
                name_or_id=as_instance
            )
            if instance and self._is_instance_in_inservice_state(instance):
                instances.append(instance)
        if len(instances) <= max_instances:
            instances = self._slice_list(instances, 10)
        return instances

    def _get_instances(self, as_group, as_instances, state, action):
        instances = []
        if state == 'present':
            if action == 'add':
                instances = self._get_instances_for_adding(
                    group=as_group,
                    as_instances=as_instances
                )
            elif action == 'protect' or action == 'unprotect':
                instances = self._get_instances_for_protection(
                    group=as_group,
                    as_instances=as_instances
                )
        else:
            if action == 'remove' or action is None:
                instances = self._get_instances_for_removing(
                    group=as_group,
                    as_instances=as_instances
                )
        return instances

    def _batch_instances_action(self, instances, group, timeout,
                                action, instance_delete=False):
        for instance_group in instances:
            self.conn.auto_scaling.batch_instance_action(
                group=self._wait_for_group_inservice_status(
                    as_group=group,
                    timeout=timeout
                ),
                instances=instance_group,
                action=action,
                delete_instance=instance_delete
            )

    def _is_instance_delete(self, instance_delete):
        if instance_delete == 'yes':
            return True
        else:
            return False

    def _wait_for_group_inservice_status(self, as_group, timeout):
        for count in self.sdk.utils.iterate_timeout(
            timeout=timeout,
            message="Timeout waiting for inservice state for group"
        ):
            group = self.conn.auto_scaling.get_group(as_group)
            if self._is_group_in_inservice_state(group):
                return group
            else:
                continue

    def run(self):
        as_group = self.params['scaling_group']
        as_instances = self.params['scaling_instances']
        instance_delete = self.params['instance_delete']
        action = self.params['action']
        state = self.params['state']
        timeout = self.params['timeout']

        try:
            group = self.conn.auto_scaling.find_group(
                name_or_id=as_group,
                ignore_missing=False
            )

        except self.sdk.exceptions.ResourceNotFound:
            self.fail(
                changed=False,
                msg='Scaling group {0} not found'.format(as_group)
            )

        max_adding = self._max_number_of_instances_for_adding(group)
        max_removing = self._max_number_of_instances_for_removing(group)
        max_protecting = self._max_number_of_instances_for_protecting(group)

        if as_instances:
            instances = self._get_instances(
                as_group=group,
                as_instances=as_instances,
                state=state,
                action=action
            )

            if self.ansible.check_mode:
                self.exit(
                    changed=self._system_state_change(
                        instances, as_instances, state, action
                    )
                )

            if state == 'present':

                if action is None:
                    self.exit(
                        changed=False,
                        msg='Instances not changed'
                    )
                elif action == 'remove':
                    self.fail(
                        changed=False,
                        msg='Action is incompatible with this state'
                    )
                elif action == 'add':
                    if not instances:
                        msg = 'Instances not found or Number of instances is ' \
                              'greater than maximum.Only {0} instances can ' \
                              'be added'.format(max_adding)
                        self.fail(
                            changed=False,
                            msg=msg
                        )
                    else:
                        self._batch_instances_action(
                            instances=instances,
                            group=group,
                            timeout=timeout,
                            action=action
                        )
                        self.exit(
                            changed=True,
                            msg='Action {0} was done'.format(action.upper())
                        )
                else:
                    if not instances:
                        msg = 'Instances not found or Number of instances is ' \
                              'greater then current. Only {0} instances can be ' \
                              'protect or unprotect'.format(max_protecting)
                        self.fail(
                            changed=False,
                            msg=msg
                        )
                    else:
                        self._batch_instances_action(
                            instances=instances,
                            group=group,
                            timeout=timeout,
                            action=action
                        )
                        self.exit(
                            changed=True,
                            msg='Action {0} was done'.format(action.upper())
                        )

            else:

                if not instances:
                    msg = 'Instances not found or Number of instances is ' \
                          'less than minimum. Only {0} instances can ' \
                          'be removed'.format(max_removing)
                    self.fail(
                        changed=False,
                        msg=msg
                    )
                else:
                    if action is None:
                        if len(as_instances) == 1:
                            if len(instances) == 1:
                                self.conn.auto_scaling.remove_instance(
                                    instance=instances[0],
                                    delete_instance=instance_delete
                                )
                                msg = 'Instance {0} was removed'.format(
                                    as_instances[0]
                                )
                                self.exit(
                                    changed=True,
                                    msg=msg
                                )
                            else:
                                msg = 'Instance {0} not found or ' \
                                      'Instance is not in INSERVICE ' \
                                      'state'.format(as_instances[0])
                                self.fail(
                                    changed=False,
                                    msg=msg
                                )
                        else:
                            self.exit(
                                changed=False,
                                msg='Instances not changed'
                            )
                    elif action == 'remove':
                        self._batch_instances_action(
                            instances=instances,
                            group=group,
                            timeout=timeout,
                            action=action,
                            instance_delete=instance_delete
                        )
                        self.exit(
                            changed=True,
                            msg='Action {0} was done'.format(action.upper())
                        )
                    else:
                        self.fail(
                            changed=False,
                            msg='Action is incompatible with this state'
                        )

        else:
            self.fail(
                changed=False,
                msg='AS instances are empty'
            )


def main():
    module = ASInstanceModule()
    module()


if __name__ == '__main__':
    main()
