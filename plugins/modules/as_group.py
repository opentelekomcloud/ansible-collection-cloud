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
short_description: Create/Update/Remove AutoScaling group from the OTC
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.2.0"
author:
  - "Polina Gubina (@Polina-Gubina)"
  - "Irina Pereiaslavskaia (@irina-pereiaslavskaia)"
description:
  - Create/Update/Remove AutoScaling group from the OTC.
options:
  scaling_group:
    description:
      - Name or ID of the AS Group.
    required: true
    type: dict
    suboptions:
      id:
        description:
          - Specifies the AS Group ID.
          - Mandatory for updating and deleting AS Group.
        type: str
      name:
        description:
          - Specifies the AS Group name.
          - Mandatory for creating AS Group.
        type: str
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
      - After a scaling action is triggered, the system starts the cooldown \
      period. During the cooldown period, scaling actions triggered by alarms \
      will be denied. Scheduled, periodic, and manual scaling actions are not \
      affected.
    type: int
    default: 300
  lb_listener:
    description:
      - Specifies ID or name of a classic load balancer listener. The system \
      supports the binding of up to six load balancer listeners, the IDs of \
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
          - Specifies the backend protocol ID, which is the port on which a \
          backend ECS listens for traffic. The port ID ranges from 1 to 65535.
        type: int
        required: true
      weight:
        description:
          - Specifies the weight, which determines the portion of requests a \
          backend ECS processes when being compared to other backend ECSs \
          added to the same listener.
        type: int
        required: true
  availability_zones:
    description:
      - Specifies the AZ information. The ECS associated with a scaling \
      action will be created in a specified AZ.If you do not specify an AZ, \
      the system automatically specifies one.
    type: list
    elements: str
  networks:
    description:
      - Specifies network information. The system supports up to five subnets.\
       The first subnet transferred serves as the primary NIC of the ECS by \
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
      - A maximum of one security group can be selected.
      - Specifies the security group. If the security group is specified both \
      in the AS configuration and AS group, the security group specified in \
      the AS configuration prevails.
      - If the security group is not specified in either of them, the default \
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
      - Specifies the health check method for instances in the AS group.\
      When load balancing is configured for an AS group, the default value \
      is ELB_AUDIT. Otherwise, the default value is NOVA_AUDIT.
      - ELB_AUDIT indicates the ELB health check, which takes effect in an \
      AS group with a listener.
      - NOVA_AUDIT indicates the ECS health check, which is the health check \
      method delivered with AS.
    choices: [elb_audit, nova_audit]
    type: str
  health_periodic_audit_time:
    description:
      - Specifies the instance health check period.
      - The value can be 1, 5, 15, 60, or 180 in the unit of minutes.
      - If this parameter is not specified, the default value is 5.
      - If the value is set to 0, health check is performed every 10 seconds.
    type: int
    default: 5
  health_periodic_audit_grace_period:
    description:
      - Specifies the grace period for instance health check.
      - The unit is second and value range is 0-86400.
      - The default value is 600.
      - The health check grace period starts after an instance is added to an \
      AS group and is enabled.The AS group will start checking the instance \
      status only after the grace period ends.
      - This parameter is valid only when the instance health check method \
      of the AS group is ELB_AUDIT.
    type: int
    default: 600
  instance_terminate_policy:
    description:
      - Specifies the instance removal policy.
      - OLD_CONFIG_OLD_INSTANCE (default). The earlier-created instances \
      based on the earlier-created AS configurations are removed first.
      - OLD_CONFIG_NEW_INSTANCE. The later-created instances based on the \
      earlier-created AS configurations are removed first.
      - OLD_INSTANCE. The earlier-created instances are removed first.
      - NEW_INSTANCE. The later-created instances are removed first.
    choices: [old_config_old_instance, old_config_new_instance,
    old_instance, new_instance]
    type: str
    default: 'old_config_old_instance'
  notifications:
    description:
      - Specifies the notification mode.
    type: list
    elements: str
  delete_publicip:
    description:
      - Specifies whether to delete the EIP bound to the ECS when \
      deleting the ECS.
      - The default value is false.
    type: bool
    default: 'no'
  delete_volume:
    description:
      - Specifies whether to delete the data disks attached to the \
      ECS when deleting the ECS.
      - The default value is false.
    type: bool
    default: 'no'
  force_delete:
    description:
      - Specifies whether to forcibly delete an AS group, remove the ECS \
      instances and release them when the AS group is running instances or \
      performing scaling actions.
    type: bool
    default: 'no'
  multi_az_priority_policy:
    description:
      - Specifies the priority policy used to select target AZs when \
      adjusting the number of instances in an AS group.
      - EQUILIBRIUM_DISTRIBUTE (default). When adjusting the number of \
      instances, ensure that instances in each AZ in the available_zones list \
      is evenly distributed. If instances cannot be added in the target AZ, \
      select another AZ based on the PICK_FIRST policy.
      - PICK_FIRST. When adjusting the number of instances, target AZs are \
      determined in the order in the available_zones list.
    choices: [equilibrium_distribute, pick_first]
    type: str
    default: 'equilibrium_distribute'
  action:
    description:
      - Specifies a flag for enabling or disabling an AS group.
    type: str
    choices: [resume, pause]
  state:
    description:
      - Whether resource should be present or absent.
    choices: [present, absent]
    type: str
    default: 'present'
  wait:
    description:
      - If the module should wait for the AS Group to be created or deleted.
    type: bool
    default: 'yes'
  timeout:
    description:
      - The duration in seconds that module should wait.
    default: 200
    type: int
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
as_group:
  description: AS groups object.
  type: complex
  returned: On Success.
  contains:
    id:
      description: Specifies the AS group ID.
      type: str
      sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
'''

EXAMPLES = '''
#Create AS Group
 - opentelekomcloud.cloud.as_group:
     scaling_group:
       name: "as_group_test"
     networks:
       - id: "a64b4561-af18-4440-9976-b2398ed39ce5"
     router: "5d1ac1f4-bec6-4b8c-aae0-7c4345c68f5d"
     scaling_configuration: "as_config_test"
     desire_instance_number: 1
     max_instance_number: 1
     action: "resume"
     state: "present"
     wait: yes
     timeout: 360
   register: result

#Delete AS Group
 - opentelekomcloud.cloud.as_group:
     scaling_group:
       name: "as_group_test"
     state: "absent"
     force_delete: yes
     wait: yes
     timeout: 360
   register: result

'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


def is_value_changed(old: list, new: list):
    """Compare lists"""
    result = [x for x in old + new if x not in old or x not in new]
    return True if result else False


class ASGroupModule(OTCModule):
    argument_spec = dict(
        scaling_group=dict(required=True, type='dict',
                           options=dict(
                               id=dict(type='str'),
                               name=dict(type='str')
                           )),
        scaling_configuration=dict(required=False),
        desire_instance_number=dict(required=False, type='int'),
        min_instance_number=dict(required=False, type='int', default=0),
        max_instance_number=dict(required=False, type='int', default=0),
        cool_down_time=dict(required=False, type='int', default=300),
        lb_listener=dict(required=False, type='str'),
        lbaas_listeners=dict(required=False, type='list', elements='dict',
                             options=dict(
                                 pool_id=dict(required=True, type='str'),
                                 protocol_port=dict(required=True, type='int'),
                                 weight=dict(required=True, type='int')
                             )
                             ),
        availability_zones=dict(required=False, type='list', elements='str'),
        networks=dict(required=False, type='list', elements='dict',
                      options=dict(
                          id=dict(required=True, type='str')
                      )),
        security_groups=dict(required=False, type='list', elements='dict',
                             options=dict(
                                 id=dict(required=True, type='str')
                             )),
        router=dict(required=False, type='str'),
        health_periodic_audit_method=dict(required=False, type='str',
                                          choices=['elb_audit', 'nova_audit']),
        health_periodic_audit_time=dict(required=False, type='int', default=5),
        health_periodic_audit_grace_period=dict(
            required=False, type='int', default=600
        ),
        instance_terminate_policy=dict(
            required=False,
            choices=['old_config_old_instance', 'old_config_new_instance',
                     'old_instance', 'new_instance'],
            default='old_config_old_instance'),
        notifications=dict(required=False, type='list', elements='str'),
        delete_publicip=dict(required=False, type='bool', default=False),
        delete_volume=dict(required=False, type='bool', default=False),
        force_delete=dict(required=False, type='bool', default=False),
        multi_az_priority_policy=dict(
            required=False, choices=['equilibrium_distribute', 'pick_first'],
            default='equilibrium_distribute'
        ),
        action=dict(required=False, type='str', choices=['resume', 'pause']),
        state=dict(
            type='str', choices=['present', 'absent'], default='present'
        ),
        wait=dict(type='bool', default=True),
        timeout=dict(type='int', default=200)

    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def _is_as_config_find(self, as_config):
        return self.conn.auto_scaling.find_config(as_config)

    def _attrs_id_config(self, attrs, as_config):
        config = self._is_as_config_find(as_config)
        if config:
            attrs['scaling_configuration_id'] = config.id
            return attrs
        else:
            self.fail(
                changed=False,
                msg="Scaling configuration {0} not found".format(as_config)
            )

    def _attrs_lb_listeners(self, attrs, lb_listener):
        lb_listener_list = lb_listener.split(',')
        if 0 < len(lb_listener_list) <= 6:
            attrs['lb_listener_id'] = ','.join(lb_listener_list)
            return attrs
        else:
            self.fail(
                changed=False,
                msg="More then 6 classical load balancers are specified"
            )

    def _attrs_id_router(self, attrs, router):
        rtr = self.conn.network.find_router(router)
        if rtr:
            attrs['router_id'] = rtr.id
            return attrs
        else:
            self.fail(
                changed=False,
                msg="Router {0} not found".format(router)
            )

    def _attrs_lbaas_listeners(self, attrs, lbaas_listeners):
        if 0 < len(lbaas_listeners) <= 6:
            lb_listeners = []
            lstnr = {}
            for listener in lbaas_listeners:
                pool = self.conn.network.find_pool(listener['pool_id'])
                if pool:
                    lstnr['pool_id'] = pool.id
                else:
                    self.fail(
                        changed=False,
                        msg="Pool {0} not found".format(listener['pool_id'])
                    )
                lstnr['protocol_port'] = listener['protocol_port']
                lstnr['weight'] = listener['weight']
                lb_listeners.append(lstnr)
            attrs['lbaas_listeners'] = lb_listeners
            return attrs
        else:
            self.fail(
                changed=False,
                msg="More then 6 enhanced load balancers are specified"
            )

    def _attrs_networks(self, attrs, networks):
        if 0 < len(networks) <= 5:
            netwrks = []
            netwrk = {}
            for network in networks:
                net = self.conn.network.find_network(network['id'])
                if net:
                    netwrk['id'] = net.id
                    netwrks.append(netwrk)
                else:
                    self.fail(
                        changed=False,
                        msg="Network {0} not found".format(network['id'])
                    )
            attrs['networks'] = netwrks
            return attrs
        else:
            self.fail(
                changed=False,
                msg="More than 5 networks are specified"
            )

    def _attrs_security_groups(self, attrs, security_groups, as_config=None):
        if as_config:
            config = self._is_as_config_find(as_config)
            if config and config.security_groups:
                attrs['security_groups'] = config.security_groups
        else:
            if len(security_groups) == 1:
                sec_groups = []
                sec_group = {}
                group = self.conn.network.find_security_group(
                    name_or_id=security_groups.id
                )
                if group:
                    sec_group['id'] = group.id
                    sec_groups.append(sec_group)
                attrs['security_groups'] = sec_groups
                return attrs
            else:
                self.fail(
                    changed=False,
                    msg="The number of security groups in the AS group "
                        "exceeds the upper limit."
                )

    def _find_as_group(self, as_group):
        if as_group.get('id'):
            return self.conn.auto_scaling.find_group(
                name_or_id=as_group.get('id')
            )
        elif as_group.get('name'):
            return self.conn.auto_scaling.find_group(
                name_or_id=as_group.get('name')
            )

    def _attrs_for_as_group_create(self, attrs, as_group, as_configuration,
                                   desire_instance_number, min_instance_number,
                                   max_instance_number, cool_down_time,
                                   lb_listener, lbaas_listeners,
                                   availability_zones, networks,
                                   security_groups, router, hp_audit_method,
                                   hp_audit_time, hp_audit_grace_period,
                                   instance_terminate_policy, notifications,
                                   delete_publicip, delete_volume,
                                   multi_az_priority_policy):

        if as_group.get('name') and not as_group.get('id'):
            attrs['scaling_group_name'] = as_group.get('name')
        else:
            self.fail(
                changed=False,
                msg="Name is mandatory for creating AS Group."
            )

        if networks:
            attrs = self._attrs_networks(attrs, networks)
        else:
            self.fail(
                changed=False,
                msg="'networks' is mandatory for creating an AS Group."
            )

        if router:
            attrs = self._attrs_id_router(attrs, router)
        else:
            self.fail(
                changed=False,
                msg="'router' is mandatory for creating an AS group."
            )

        if as_configuration:
            attrs = self._attrs_id_config(attrs, as_configuration)

        if desire_instance_number:
            attrs['desire_instance_number'] = desire_instance_number

        if min_instance_number:
            attrs['min_instance_number'] = min_instance_number

        if max_instance_number:
            attrs['max_instance_number'] = max_instance_number

        if cool_down_time:
            attrs['cool_down_time'] = cool_down_time

        if lb_listener and lbaas_listeners:
            self.fail(
                changed=False,
                msg="Either 'lb_listener' or 'lbaas_listener' "
                    "can be specified"
            )

        if lb_listener:
            attrs = self._attrs_lb_listeners(attrs, lb_listener)

        if lbaas_listeners:
            attrs = self._attrs_lbaas_listeners(attrs, lbaas_listeners)

        if not hp_audit_method:
            # set default values  for 'health_periodic_audit_method'
            if lb_listener or lbaas_listeners:
                attrs['health_periodic_audit_method'] = "elb_audit".upper()
            else:
                attrs['health_periodic_audit_method'] = "nova_audit".upper()
        else:
            if not lb_listener and not lbaas_listeners:
                if hp_audit_method == 'elb_audit':
                    self.fail("Without LB only 'nova_audit' is available")
                else:
                    attrs['health_periodic_audit_method'] = \
                        hp_audit_method.upper()
            else:
                attrs['health_periodic_audit_method'] = \
                    hp_audit_method.upper()

        if availability_zones:
            attrs['availability_zones'] = availability_zones

        if security_groups:
            attrs = self._attrs_security_groups(attrs, security_groups)

        if hp_audit_time:
            attrs['health_periodic_audit_time'] = hp_audit_time

        if delete_publicip:
            attrs['delete_publicip'] = delete_publicip

        if delete_volume:
            attrs['delete_volume'] = delete_volume

        if hp_audit_grace_period:
            attrs['health_periodic_audit_grace_period'] = \
                hp_audit_grace_period

        if instance_terminate_policy:
            attrs['instance_terminate_policy'] = \
                instance_terminate_policy.upper()

        if notifications:
            attrs['notifications'] = notifications

        if multi_az_priority_policy:
            attrs['multi_az_priority_policy'] = \
                multi_az_priority_policy.upper()

        return attrs

    def _attrs_for_as_group_update(self, attrs, as_group, as_configuration,
                                   desire_instance_number, min_instance_number,
                                   max_instance_number, cool_down_time,
                                   lb_listener, lbaas_listeners,
                                   availability_zones, networks,
                                   security_groups, hp_audit_method,
                                   hp_audit_time, hp_audit_grace_period,
                                   instance_terminate_policy, notifications,
                                   delete_publicip, delete_volume,
                                   multi_az_priority_policy, group):

        if as_group and (group.name != as_group.get('name')):
            attrs['scaling_group_name'] = as_group

        if (as_configuration and
                as_configuration != group.scaling_configuration_id and
                as_configuration != group.scaling_configuration_name):
            attrs = self._attrs_id_config(attrs, as_configuration)

        if (desire_instance_number and
                (group.desire_instance_number != desire_instance_number)):
            attrs['desire_instance_number'] = desire_instance_number

        if (min_instance_number and
                (group.min_instance_number != min_instance_number)):
            attrs['min_instance_number'] = min_instance_number

        if (max_instance_number and
                (group.max_instance_number != max_instance_number)):
            attrs['max_instance_number'] = max_instance_number

        if cool_down_time and group.cool_down_time != cool_down_time:
            attrs['cool_down_time'] = cool_down_time

        if lb_listener and lbaas_listeners:
            self.fail(
                changed=False,
                msg="Either 'lb_listener' or 'lbaas_listener' "
                    "can be specified"
            )

        if lb_listener and group.lb_listner_id != lb_listener:
            attrs = self._attrs_lb_listeners(attrs, lb_listener)

        if (lbaas_listeners and
                is_value_changed(group.lbaas_listeners, lbaas_listeners)):
            attrs = self._attrs_lbaas_listeners(attrs, lbaas_listeners)

        if (availability_zones and
                is_value_changed(
                    group.availability_zones, availability_zones
                )):
            attrs['availability_zones'] = availability_zones

        if (networks and
                is_value_changed(group.networks, networks)):
            attrs = self._attrs_networks(attrs, networks)

        if (security_groups and
                is_value_changed(group.security_groups, security_groups)):
            attrs = self._attrs_security_groups(attrs, security_groups)

        if (hp_audit_method and
                (group.health_periodic_audit_method !=
                 hp_audit_method.upper())):

            if (not group.lb_listener_id and
                    not group.lbaas_listeners and
                    hp_audit_method == 'elb_audit'.upper()):
                self.fail_json(
                    msg="Without LB only 'nova_audit' is available"
                )

            attrs['health_periodic_audit_method'] = hp_audit_method.upper()

        if (hp_audit_time and
                group.health_periodic_audit_time != hp_audit_time):
            attrs['health_periodic_audit_time'] = hp_audit_time

        if (hp_audit_grace_period and
                group.health_periodic_audit_grace_period !=
                hp_audit_grace_period):
            attrs['health_periodic_audit_grace_period'] = hp_audit_grace_period

        if (instance_terminate_policy
                and group.instance_terminate_policy !=
                instance_terminate_policy.upper()):
            attrs['instance_terminate_policy'] = \
                instance_terminate_policy.upper()

        if notifications and group.notifications != notifications:
            attrs['notifications'] = notifications

        if delete_publicip and group.delete_publicip != delete_publicip:
            attrs['delete_publicip'] = delete_publicip

        if delete_volume and group.delete_volume != delete_volume:
            attrs['delete_volume'] = delete_volume

        if (multi_az_priority_policy and group.multi_az_priority_policy !=
                multi_az_priority_policy.upper()):
            attrs['multi_az_priority_policy'] = multi_az_priority_policy.upper()

        return attrs

    def _wait_for_instances(self, as_group, timeout, desire_instance_number=0):
        for count in self.sdk.utils.Iterate_timeout(
            timeout=timeout,
            message="Timeout waiting for AS Instances"
        ):
            instances = list(self.conn.auto_scaling.instances(
                group=as_group
            ))
            if (len(instances) == desire_instance_number
                    and [instance.id for instance in instances
                         if instance.id]):
                for instance in instances:
                    self.conn.auto_scaling.wait_for_instance(instance=instance)

    def _resume_group(self, group, wait, timeout, desire_instance_number=0):
        result_group = group
        self.conn.auto_scaling.resume_group(group=group)
        if wait:
            try:
                if desire_instance_number > 0:
                    self.conn.auto_scaling.wait_for_instances(
                        as_group=group,
                        timeout=timeout,
                        desire_instance_number=desire_instance_number
                    )
                result_group = self.conn.auto_scaling.wait_for_group(
                    group=group,
                    wait=timeout
                )
            except self.sdk.exceptions.ResourceTimeout:
                self.fail(
                    msg="Timeout failure waiting for AS Group"
                )
        return result_group

    def _pause_group(self, group, wait, timeout):
        result_group = group
        self.conn.auto_scaling.pause_group(group=group)
        if wait:
            try:
                result_group = self.conn.auto_scaling.wait_for_group(
                    group=group,
                    status='PAUSED',
                    wait=timeout
                )
            except self.sdk.exceptions.ResourceTimeout:
                self.fail(
                    msg="Timeout failure waiting for AS Group"
                )
        return result_group

    def _action_group(self, action, group, wait, timeout):
        if action == 'resume':
            return self._resume_group(group, wait, timeout)
        elif action == 'pause':
            return self._pause_group(group, wait, timeout)

    def _needs_update(self, as_group, as_configuration, desire_instance_number,
                      min_instance_number, max_instance_number, cool_down_time,
                      lb_listener, lbaas_listeners, availability_zones,
                      networks, security_groups, hp_audit_method,
                      hp_audit_time, hp_audit_grace_period,
                      instance_terminate_policy, notifications,
                      delete_publicip, delete_volume, multi_az_priority_policy,
                      group):
        if as_group and group.name != as_group.get('name'):
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

        if (lb_listener and
                group.lb_listner_id != lb_listener):
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

        if (hp_audit_method and
                group.health_periodic_audit_method != hp_audit_method.upper()):
            return True

        if (hp_audit_time and
                group.health_periodic_audit_time != hp_audit_time):
            return True

        if (hp_audit_grace_period and
                group.health_periodic_audit_grace_period !=
                hp_audit_grace_period):
            return True

        if (instance_terminate_policy and group.instance_terminate_policy !=
                instance_terminate_policy.upper()):
            return True

        if notifications and group.notifications != notifications:
            return True

        if delete_publicip and group.delete_publicip != delete_publicip:
            return True

        if delete_volume and group.delete_volume != delete_volume:
            return True

        if (multi_az_priority_policy and group.multi_az_priority_policy !=
                multi_az_priority_policy.upper()):
            return True

        return False

    def _is_group_can_be_deleted(self, as_group):
        as_instances = list(self.conn.auto_scaling.instances(as_group))
        return False if as_instances else True

    def _delete_as_group(self, as_group, force_delete, wait, timeout):
        self.conn.auto_scaling.delete_group(
            group=as_group,
            force_delete=force_delete
        )
        if wait:
            try:
                self.conn.auto_scaling.wait_for_delete_group(
                    group=as_group,
                    wait=timeout
                )
            except self.sdk.exceptions.ResourceTimeout:
                self.fail(
                    msg="Timeout failure waiting for delete AS Group"
                )

    def _system_state_change(self, as_group, as_configuration,
                             desire_instance_number, min_instance_number,
                             max_instance_number, cool_down_time, lb_listener,
                             lbaas_listeners, availability_zones, networks,
                             security_groups, hp_audit_method,
                             hp_audit_time, hp_audit_grace_period,
                             instance_terminate_policy, notifications,
                             delete_publicip, delete_volume,
                             multi_az_priority_policy, group):
        state = self.params['state']
        if state == 'present':
            if not group:
                return True
            return self._needs_update(
                as_group, as_configuration, desire_instance_number,
                min_instance_number, max_instance_number, cool_down_time,
                lb_listener, lbaas_listeners, availability_zones, networks,
                security_groups, hp_audit_method, hp_audit_time,
                hp_audit_grace_period, instance_terminate_policy,
                notifications, delete_publicip, delete_volume,
                multi_az_priority_policy, group
            )
        elif state == 'absent' and group:
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
        availability_zones = self.params['availability_zones']
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
        force_delete = self.params['force_delete']
        multi_az_priority_policy = self.params['multi_az_priority_policy']
        action = self.params['action']
        wait = self.params['wait']
        timeout = self.params['timeout']
        state = self.params['state']

        attrs = {}

        changed = False

        if as_group:
            group = self._find_as_group(as_group)

            if self.ansible.check_mode:
                self.exit(
                    changed=self._system_state_change(
                        as_group, as_configuration,
                        desire_instance_number, min_instance_number,
                        max_instance_number, cool_down_time,
                        lb_listener, lbaas_listeners,
                        availability_zones, networks, security_groups,
                        hp_audit_method, hp_audit_time,
                        hp_audit_gr_period, instance_terminate_policy,
                        notifications, delete_publicip, delete_volume,
                        multi_az_priority_policy, group)
                )

            if group:

                if state == 'present':

                    if self._needs_update(
                            as_group, as_configuration, desire_instance_number,
                            min_instance_number, max_instance_number,
                            cool_down_time, lb_listener, lbaas_listeners,
                            availability_zones, networks, security_groups,
                            hp_audit_method, hp_audit_time, hp_audit_gr_period,
                            instance_terminate_policy, notifications,
                            delete_publicip, delete_volume,
                            multi_az_priority_policy, group
                    ):
                        attrs = self._attrs_for_as_group_update(
                            as_group, as_configuration, desire_instance_number,
                            min_instance_number, max_instance_number,
                            cool_down_time, lb_listener, lbaas_listeners,
                            availability_zones, networks, security_groups,
                            hp_audit_method, hp_audit_time, hp_audit_gr_period,
                            instance_terminate_policy, notifications,
                            delete_publicip, delete_volume,
                            multi_az_priority_policy, group
                        )
                        group = self.conn.auto_scaling.update_group(**attrs)
                        changed = True
                        if action:
                            group = self._action_group(
                                action=action,
                                group=group,
                                wait=wait,
                                timeout=timeout
                            )
                        self.exit(
                            changed=changed,
                            as_group=group,
                            msg="AS Group {0} was updated".format(group.id)
                        )
                    elif action:
                        group = self._action_group(
                            action=action,
                            group=group,
                            wait=wait,
                            timeout=timeout
                        )
                        changed = True
                        self.exit(
                            changed=changed,
                            as_group=group,
                            msg="Action {0} for AS Group {1} was done".format(
                                action, group.id
                            )
                        )
                    else:
                        self.fail(
                            changed=changed,
                            msg="AS Group {0} exists".format(group.id)
                        )

                else:
                    if force_delete or self._is_group_can_be_deleted(group):
                        self._delete_as_group(group, force_delete, wait,
                                              timeout)
                        changed = True
                        self.exit(
                            changed=changed,
                            msg="AS Group {0} was deleted".format(group.id)
                        )
                    else:
                        changed = False
                        self.fail(
                            changed=changed,
                            msg="AS Group {0} can't be deleted due to "
                                "AS Instances presence".format(group.id)
                        )

            else:

                if state == 'present':
                    attrs = self._attrs_for_as_group_create(
                        attrs, as_group, as_configuration,
                        desire_instance_number, min_instance_number,
                        max_instance_number, cool_down_time, lb_listener,
                        lbaas_listeners, availability_zones, networks,
                        security_groups, router, hp_audit_method,
                        hp_audit_time, hp_audit_gr_period,
                        instance_terminate_policy, notifications,
                        delete_publicip, delete_volume,
                        multi_az_priority_policy
                    )
                    group = self.conn.auto_scaling.create_group(**attrs)
                    changed = True
                    if (as_configuration and
                            self.conn.auto_scaling.find_config(
                            name_or_id=as_configuration) and action):
                        group = self._action_group(
                            action=action,
                            group=group,
                            wait=wait,
                            timeout=timeout
                        )
                    self.exit(
                        changed=changed,
                        as_group=group,
                        msg="AS Group {0} was created".format(as_group.get(
                            "name"))
                    )
                else:
                    self.fail(
                        changed=changed,
                        msg="AS Group {0} not found".format(as_group.get(
                            "name"))
                    )

        else:
            self.fail(
                changed=changed,
                msg="Name or/and ID should be specified"
            )


def main():
    module = ASGroupModule()
    module()


if __name__ == '__main__':
    main()
