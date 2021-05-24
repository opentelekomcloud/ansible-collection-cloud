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
module: as_group
short_description: Create/Remove AutoScaling group from the OTC
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.2.0"
author: "Polina Gubina (@Polina-Gubina)"
description:
  - Create/Remove AutoScaling group from the OTC.
options:
  scaling_group:
    description:
      - Name or ID of the AS Group.
    type: str
    required: true
  scaling_configuration:
    description:
      - The AS configuration ID or name.
    type: str
  desire_instance_number:
    description:
      - Specifies the expected number of instances.
      - The default value is the minimum number of instances.
    type: int
  min_instance_number:
    description:
      - Specifies the minimum number of instances.
      - The default value is 0.
    type: int
  max_instance_number:
    description:
      - Specifies the maximum number of instances.
      - The default value is 0.
    type: int
  cool_down_time:
    description:
      - Specifies the cooldown period (in seconds). 
      - The value ranges from 0 to 86400 and is 300 by default.
      - After a scaling action is triggered, the system starts the cooldown
      period. During the cooldown period, scaling actions triggered by alarms
      will be denied. Scheduled, periodic, and manual scaling actions are not
      affected.
    type: int
  lb_listener:
    description:
      - Specifies ID or name of a classic load balancer listener. The system
      supports the binding of up to six load balancer listeners, the IDs of
      which are separated using a comma (,).
      - Mandatory when 'lbaas_listeners' is not specified.
    type: str
  lbaas_listeners:
    description:
      - Specifies information about an enhanced load balancer.
      - Mandatory when 'lb_listener' is not specified.
    type: list
    elements: dict
    suboptions:
      pool_id:
        description:
          - Specifies the backend ECS group ID.
        type: str
        required: true
      protocol_port:
        description:
          - Specifies the backend protocol ID, which is the port on which a
           backend ECS listens for traffic. The port ID ranges from 1 to 65535.
        type: int
        required: true
      weight:
        description:
          - Specifies the weight, which determines the portion
          of requests a backend ECS processes when being compared to other 
          backend ECSs added to the same listener.
        type: int
        required: true
  available_zones:
    description:
      - Specifies the AZ information. The ECS associated with a scaling
       action will be created in a specified AZ.If you do not specify an AZ,
       the system automatically specifies one.
    type: list
    elements: str
  networks:
    description:
      - Specifies network information. The system supports up to five subnets.
       The first subnet transferred serves as the primary NIC of the ECS by 
       default.
      - Mandatory for creation of AS group.
    type: list
    elements: dict
    suboptions:
      id:
        description:
          - Specifies the network ID.
        type: str
        required: true
  security_groups:
    description:
      - Specifies the security group. If the security group is specified both
      in the AS configuration and AS group, the security group specified in
      the AS configuration prevails.
      - If the security group is not specified in either of them, the default
      security group is used.
    type: list
    elements: dict
    suboptions:
      id:
        description:
          - Specifies the security group ID.
        type: str
        required: true
  router:
    description:
      - The router ID or name.
      - Mandatory for creating AS group.
    type: str
  health_periodic_audit_method:
    description:
      - Specifies the health check method for instances in the AS group.
      When load balancing is configured for an AS group, the default value
      is ELB_AUDIT. Otherwise, the default value is NOVA_AUDIT.
      - ELB_AUDIT indicates the ELB health check, which takes effect in an
      AS group with a listener.
      - NOVA_AUDIT indicates the ECS health check, which is the health check
      method delivered with AS.
    choices: ['elb_audit', 'nova_audit']
    type: str
  health_periodic_audit_time:
    description:
      - Specifies the instance health check period. 
      - The value can be 1, 5, 15, 60, or 180 in the unit of minutes.
      - If this parameter is not specified, the default value is 5.
      - If the value is set to 0, health check is performed every 10 seconds.
    type: int
  health_periodic_audit_grace_period:
    description:
      - Specifies the grace period for instance health check.
      - The unit is second and value range is 0-86400.
      - The default value is 600.
      - The health check grace period starts after
      an instance is added to an AS group and is enabled.The AS group will
      start checking the instance status only after the grace period ends.
      - This parameter is valid only when the instance health check method
      of the AS group is ELB_AUDIT.
    type: int
  instance_terminate_policy:
    description:
      - Specifies the instance removal policy.
      - OLD_CONFIG_OLD_INSTANCE (default). The earlier-created instances
      based on the earlier-created AS configurations are removed first.
      - OLD_CONFIG_NEW_INSTANCE. The later-created instances based on the
      earlier-created AS configurations are removed first.
      - OLD_INSTANCE. The earlier-created instances are removed first.
      - NEW_INSTANCE. The later-created instances are removed first.
    choices: ['old_config_old_instance', 'old_config_new_instance',
    'old_instance', 'new_instance']
    type: str
  notifications:
    description:
      - Specifies the notification mode.
    type: list
    elements: str
  delete_publicip:
    description:
      - Specifies whether to delete the EIP bound to the ECS when
      deleting the ECS.
      - The default value is false.
    type: bool
  delete_volume:
    description:
      - Specifies whether to delete the data disks attached to the
      ECS when deleting the ECS.
      - The default value is false.
    type: bool
  enterprise_project_id:
    description:
      - Specifies the enterprise project ID, which is used to specify
      the enterprise project to which the AS group belongs.
      - If the value is 0 or left blank, the AS group belongs to the default
      enterprise project.
      - If the value is a UUID, the AS group belongs to the enterprise project
      corresponding to the UUID.
    type: str
  multi_az_priority_policy:
    description:
      - Specifies the priority policy used to select target AZs when adjusting
      the number of instances in an AS group.
      - EQUILIBRIUM_DISTRIBUTE (default). When adjusting the number of
      instances, ensure that instances in each AZ in the available_zones list
      is evenly distributed. If instances cannot be added in the target AZ,
      select another AZ based on the PICK_FIRST policy.
      - PICK_FIRST. When adjusting the number of instances, target AZs are
      determined in the order in the available_zones list.
    choices: ['equilibrium_distribute', 'pick_first']
    type: str
  state:
    description:
      - Whether resource should be present or absent.
    choices: ['present', 'absent']
    type: str
    default: 'present'
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
as_group:
  description: AS groups object.
  type: complex
  returned: On Success.
  contains:
    scaling_group_id:
      description: Specifies the AS group ID.
      type: str
      sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
'''

EXAMPLES = '''
opentelekomcloud.cloud.as_group:
  scaling_group_name: "scaling-group-test"
  networks:
    - id: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
  router: "65707a7e-ee4f-4d13-8283-b4da2e037c69"
register: as_group
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


def is_value_changed(old: list, new: list):
    """Compare lists"""
    result = [x for x in old + new if x not in old or x not in new]
    if result:
        return True
    else:
        return False


class ASGroupModule(OTCModule):
    argument_spec = dict(
        scaling_group=dict(required=True, type='str'),
        scaling_configuration=dict(required=False),
        desire_instance_number=dict(required=False, type='int'),
        min_instance_number=dict(required=False, type='int'),
        max_instance_number=dict(required=False, type='int'),
        cool_down_time=dict(required=False, type='int'),
        lb_listener=dict(required=False),
        lbaas_listeners=dict(required=False, type='list', elements='dict'),
        available_zones=dict(required=False, type='list', elements='str'),
        networks=dict(required=False, type='list', elements='dict'),
        security_groups=dict(required=False, type='list', elements='dict'),
        router=dict(required=False, type='str'),
        health_periodic_audit_method=dict(required=False, type='str', choices=['elb_audit', 'nova_audit']),
        health_periodic_audit_time=dict(required=False, type='int'),
        health_periodic_audit_grace_period=dict(required=False, type='int'),
        instance_terminate_policy=dict(required=False,
                                       choices=['old_config_old_instance', 'old_config_new_instance',
                                                'old_instance', 'new_instance']),
        notifications=dict(required=False, type='list', elements='str'),
        delete_publicip=dict(required=False, type='bool'),
        delete_volume=dict(required=False, type='bool'),
        enterprise_project_id=dict(required=False),
        multi_az_priority_policy=dict(required=False, choices=['equilibrium_distribute', 'pick_first']),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def _find_id_config(self):
        config = self.conn.auto_scaling.find_config(self.params['scaling_configuration'], ignore_missing=True)
        config_id = None
        if config:
            config_id = config.id
        else:
            self.fail_json(msg="Scaling configuration not found")
        return config_id

    def _find_id_listener(self):
        listener = self.conn.network.find_listener(self.params['scaling_configuration'], ignore_missing=True)
        listener_id = None
        if listener:
            listener_id = listener.id
        else:
            self.fail_json(msg="Listener not found")
        return listener_id

    def _find_id_router(self):
        router = self.conn.network.find_router(self.params['router'], ignore_missing=True)
        router_id = None
        if router:
            router_id = router.id
        else:
            self.fail_json(msg="Router not found")
        return router_id

    def _get_attrs_for_as_group_create(self):
        pass

    def _get_attrs_for_as_group_update(self):
        pass

    def _needs_update(self, as_group, as_configuration, desire_instance_number,
                      min_instance_number, max_instance_number, cool_down_time,
                      lb_listner, lbaas_listeners, availability_zones,
                      networks, security_groups, router, hp_audit_method,
                      hp_audit_time, hp_audit_grace_period,
                      instance_terminate_policy, notifications,
                      delete_publicip, delete_volume, enterprise_project_id,
                      multi_az_priority_policy, group):
        if as_group and group.name != as_group and group.id != as_group:
            return True
        if (as_configuration and
                group.scaling_configuration_id != as_configuration and
                group.scaling_configuration_name != as_configuration):
            return True
        if (desire_instance_number and
                group.desire_instance_number != desire_instance_number):
            return True
        if (min_instance_number and
                group.min_instance_number != min_instance_number):
            return True
        if (max_instance_number and
                group.max_instance_number != max_instance_number):
            return True
        if (cool_down_time and
                group.cool_down_time != cool_down_time):
            return True
        if (lb_listner and
                group.lb_listner_id != lb_listner):
            return True
        if (lbaas_listeners and
                is_value_changed(group.lbaas_listeners, lbaas_listeners)):
            return True
        if (availability_zones and
                is_value_changed(group.availability_zones,
                                 availability_zones)):
            return True
        if (networks and
                is_value_changed(group.networks, networks)):
            return True
        if (security_groups and is_value_changed(group.security_groups,
                                                 security_groups)):
            return True
        if router and group.router_id != router.id:
            return True
        if (hp_audit_method and
                group.health_periodic_audit_method != hp_audit_method):
            return True
        if (hp_audit_time and
                group.health_periodic_audit_time != hp_audit_time):
            return True
        if (hp_audit_grace_period and
                group.health_periodic_audit_grace_period !=
                hp_audit_grace_period):
            return True
        if (instance_terminate_policy and group.instance_terminate_policy !=
                instance_terminate_policy):
            return True
        if notifications and group.notifications != notifications:
            return True
        if delete_publicip and group.delete_publicip != delete_publicip:
            return True
        if delete_volume and group.delete_volume != delete_volume:
            return True
        if (enterprise_project_id and group.enterprise_project_id !=
                enterprise_project_id):
            return True
        if (multi_az_priority_policy and group.multi_az_priority_policy !=
                multi_az_priority_policy):
            return True
        return False

    def run(self):

        as_group = self.params['scaling_group']
        as_configuration = self.params['scaling_configuration']
        desire_instance_number = self.params['desire_instance_number']
        min_instance_number = self.params['min_instance_number']
        max_instance_number = self.params['max_instance_number']
        cool_down_time = self.params['cool_down_time']
        lb_listener = self.params['lb_listener']
        lbaas_listeners = self.params['lbaas_listeners']
        available_zones = self.params['available_zones']
        networks = self.params['networks']
        security_groups = self.params['security_groups']
        router = self.params['router']
        hp_audit_method = self.params['health_periodic_audit_method']
        hp_audit_time = self.params['health_periodic_audit_time']
        hp_audit_gr_period = self.params['health_periodic_audit_grace_period']
        instance_terminate_policy = self.params['instance_terminate_policy']
        notifications = self.params['notifications']
        delete_publicip = self.params['delete_publicip']
        delete_volume = self.params['delete_volume']
        enterprise_project_id = self.params['enterprise_project_id']
        multi_az_priority_policy = self.params['multi_az_priority_policy']

        attrs = {}

        changed = False

        try:
            group = self.conn.auto_scaling.find_group(
                name_or_id=as_group,
                ignore_missing=False
            )
        except self.sdk.exceptions.ResourceNotFound:
            self.fail(
                changed=changed,
                msg='Scaling group {0} not found'.format(as_group)
            )

        if self.params['state'] == 'present':

            if group:

                if as_group and (group.name != as_group):
                    attrs['scaling_group_name'] = group.name

                if as_configuration:
                    id_config = self._find_id_config()
                    if as_group.scaling_configuration_id != id_config:
                        attrs['scaling_configuration_id'] = id_config

                if (desire_instance_number and
                        (group.desire_instance_number != desire_instance_number)):
                    attrs['desire_instance_number'] = desire_instance_number

                if (min_instance_number and
                        (group.min_instance_number != min_instance_number)):
                    attrs['min_instance_number'] = min_instance_number

                if (max_instance_number and
                        (group.max_instance_number != max_instance_number)):
                    attrs['max_instance_number'] = max_instance_number

                if cool_down_time and (group.cool_down_time != cool_down_time):
                    attrs['cool_down_time'] = cool_down_time

                if lb_listener:
                    lb_listener_id = self._find_listener_id()
                    if group.lb_listener_id != lb_listener_id:
                        attrs['lb_listener_id'] = lb_listener_id

                if available_zones and (group.available_zones != available_zones):
                    attrs['available_zones'] = available_zones

                if networks:
                    list_ids = []
                    list_new_ids = []
                    for n in as_group.networks:
                        list_ids.append(n['id'])
                    for m in self.params['networks']:
                        list_new_ids.append(m['id'])
                    dif = set(list_ids) ^ set(list_new_ids)
                    if dif:
                        attrs['networks'] = networks

                if security_groups and (group.security_groups != security_groups):
                    attrs['available_zones'] = available_zones

                if hp_audit_method and (group.health_periodic_audit_method != hp_audit_method):

                    if not group.lb_listener_id and hp_audit_method == 'elb_audit':
                        self.fail_json(msg="Without LB only 'nova_audit' is available")

                    attrs['health_periodic_audit_method'] = hp_audit_method

                if (instance_terminate_policy
                        and group.instance_terminate_policy != instance_terminate_policy):
                    attrs['instance_terminate_policy'] = instance_terminate_policy

                if notifications and group.notifications != notifications:
                    attrs['notifications'] = notifications

                if delete_publicip and group.delete_publicip != delete_publicip:
                    attrs['delete_publicip'] = delete_publicip

                if delete_volume and group.delete_volume != delete_volume:
                    attrs['delete_volume'] = delete_volume

                if (enterprise_project_id
                        and group.enterprise_project_id != enterprise_project_id):
                    attrs['enterprise_project_id'] = enterprise_project_id

                changed = False

                if attrs:
                    changed = True

                if self.ansible.check_mode:
                    self.exit(changed=changed, as_group=as_group)
                as_group = self.conn.auto_scaling.update_group(as_group, **attrs)

                self.exit_json(
                    changed=changed,
                    as_group=as_group
                )

            else:

                if as_group:
                    attrs['scaling_group_name'] = as_group
                else:
                    self.json(msg="Name is mandatory for creating.")

                if networks:
                    attrs['networks'] = networks
                else:
                    self.fail_json(msg="'networks' is mandatory for creating an AS group.")

                if router:
                    attrs['vpc_id'] = self._find_id_router()
                else:
                    self.fail_json(msg="'router' is mandatory for creating an AS group.")

                if as_configuration:
                    attrs['scaling_configuration_id'] = self._find_id_config()

                if lb_listener and lbaas_listeners:
                    self.fail_json(msg="Either 'lb_listener' or"
                                       " 'lbaas_listener' can be specified")

                if not hp_audit_method:
                    # set default values  for 'health_periodic_audit_method'
                    if lb_listener or lbaas_listeners:
                        attrs['health_periodic_audit_method'] = "ELB_AUDIT"
                    else:
                        attrs['health_periodic_audit_method'] = "NOVA_AUDIT"
                else:
                    if not lb_listener and not lbaas_listeners:
                        if hp_audit_method == 'elb_audit':
                            self.fail_json("Without LB only 'nova_audit' is available")
                        else:
                            attrs['health_periodic_audit_method'] = hp_audit_method.upper()
                    else:
                        attrs['health_periodic_audit_method'] = hp_audit_method.upper()

                if lb_listener:
                    attrs['lb_listener_id'] = self._find_id_listener()

                if lbaas_listeners:
                    attrs['lbaas_listeners'] = lbaas_listeners

                if min_instance_number:
                    attrs['min_instance_number'] = min_instance_number
                else:
                    attrs['min_instance_number'] = 0

                if max_instance_number:
                    attrs['max_instance_number'] = max_instance_number
                else:
                    attrs['max_instance_number'] = 0

                if hp_audit_time:
                    attrs['health_periodic_audit_time'] = hp_audit_time
                else:
                    attrs['health_periodic_audit_time'] = 5

                if delete_publicip:
                    attrs['delete_publicip'] = delete_publicip
                else:
                    attrs['delete_publicip'] = False

                if delete_volume:
                    attrs['delete_volume'] = delete_volume
                else:
                    attrs['delete_volume'] = False

                if cool_down_time:
                    attrs['cool_down_time'] = cool_down_time
                else:
                    attrs['cool_down_time'] = 300

                if hp_audit_gr_period:
                    attrs['health_periodic_audit_grace_period'] = hp_audit_gr_period
                else:
                    attrs['health_periodic_audit_grace_period'] = 600

                if desire_instance_number:
                    attrs['desire_instance_number'] = desire_instance_number
                if available_zones:
                    attrs['available_zones'] = available_zones
                if security_groups:
                    attrs['security_groups'] = security_groups

                if instance_terminate_policy:
                    attrs['instance_terminate_policy'] = instance_terminate_policy.upper()
                else:
                    attrs['instance_terminate_policy'] = 'OLD_CONFIG_OLD_INSTANCE'

                if notifications:
                    attrs['notifications'] = notifications
                if enterprise_project_id:
                    attrs['enterprise_project_id'] = enterprise_project_id
                if multi_az_priority_policy:
                    attrs['multi_az_priority_policy'] = multi_az_priority_policy.upper()
                else:
                    attrs['multi_az_priority_policy'] = 'EQUILIBRIUM_DISTRIBUTE'

                if self.ansible.check_mode:
                    self.exit(changed=True)

                as_group = self.conn.auto_scaling.create_group(**attrs)
                changed = True

                self.exit_json(
                    changed=changed,
                    as_group=as_group
                )

        elif self.params['state'] == 'absent':
            if as_group:
                if self.ansible.check_mode:
                    self.exit(changed=True)
                self.conn.auto_scaling.delete_group(as_group)
                self.exit(changed=True, msg="Resource was deleted")
            else:
                if self.ansible.check_mode:
                    self.exit(changed=False)
                self.fail_json("The group doesn't exist")


def main():
    module = ASGroupModule()
    module()


if __name__ == '__main__':
    main()
