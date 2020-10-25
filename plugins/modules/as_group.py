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
short_description: Create/Remove AutoScaling groups from the OTC
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Polina Gubina (@Polina-Gubina)"
description:
  - Create/Remove AutoScaling groups from the OTC.
options:
  scaling_group_name:
    description:
      - Name of the AS group.
      - Mandatory for creating autoscaling group.
    type: str
    required: yes
  scaling_group_id:
    description:
      - ID the AS group.
    type: str
  scaling_configuration:
    description:
      - The AS configuration ID or name.
    type: str
  desire_instance_number:
    description:
      - Specifies the expected number of instances. The default value is the minimum number of instances.
    type: int
  min_instance_number:
    description:
      - Specifies the minimum number of instances. The default value is 0.
    type: int
    default: 0
  max_instance_number:
    description:
      - Specifies the maximum number of instances. The default value is 0.
    type: int
    default: 0
  cool_down_time:
    description:
      - Specifies the cooldown period (in seconds). The value ranges from 0 to 86400 and is 300 by default.
      - After a scaling action is triggered, the system starts the cooldown period. During the cooldown period, scaling actions triggered by alarms will be denied. Scheduled, periodic, and manual scaling actions are not affected.
    type: int
    default: 300
  lb_listener:
    description:
      - Specifies ID or name of a classic load balancer listener. The system supports the binding of up to six load balancer listeners, the IDs of which are separated using a comma (,).
      - Mandatory when 'lbaas_listeners' is not specified.
    type: str
  lbaas_listeners:
    description:
      - Specifies information about an enhanced load balancer.
      - Mandatory when 'lb_listener' is not specified.
    type: list
    elements: dict
  available_zones:
    description:
      - Specifies the AZ information. The ECS associated with a scaling action will be created in a specified AZ. If you do not specify an AZ, the system automatically specifies one.
    type: list
  networks:
    description:
      - Specifies network information. The system supports up to five subnets. The first subnet transferred serves as the primary NIC of the ECS by default.
      - Mandatory for creation of autoscaling group.
    type: list
    elements: str
  security_groups:
    description:
      - Specifies the security group. If the security group is specified both in the AS configuration and AS group, the security group specified in the AS configuration prevails. If the security group is not specified in either of them, the default security group is used.
    type: list
    elements: dict
  vpc:
    description:
      - The VPC ID or name. 
      - Mandatory for creating resource.
    type: str
  health_periodic_audit_method:
    description:
      - Specifies the health check method for instances in the AS group. The default value is ELB_AUDIT.
      - ELB_AUDIT: indicates the ELB health check, which takes effect in an AS group with a listener.
      - NOVA_AUDIT: indicates the ECS health check, which is the health check method delivered with AS.
    choices: ['elb_audit', 'nova_audit']
    type: str
    default: 'nova_audit'
  health_periodic_audit_time:
    description:
      -  Specifies the instance health check period.  The value can be 1, 5, 15, 60, or 180 in the unit of minutes. If this parameter is not specified, the default value is 5. If the value is set to 0, health check is performed every 10 seconds.
    type: int
    default: 5
  health_periodic_audit_grace_period:
    description:
      -  Specifies the grace period for instance health check. The unit is second and value range is 0-86400. The default value is 600. The health check grace period starts after an instance is added to an AS group and is enabled. The AS group will start checking the instance status only after the grace period ends.
      -  This parameter is valid only when the instance health check method of the AS group is ELB_AUDIT.
    type: int
    default: 600
  instance_terminate_policy:
    description:
      -  Specifies the instance removal policy.
    choices: ['old_config_old_instance', 'old_config_new_instance', 'old_instance', 'new_instance']
    type: str
  notifications:
    description:
      -  Specifies the notification mode.
    type: list
    elements: str
  delete_publicip:
    description:
      -  Specifies whether to delete the EIP bound to the ECS when deleting the ECS.
    type: bool
    default: False
  delete_volume:
    description:
      - Specifies whether to delete the data disks attached to the ECS when deleting the ECS.
    type: bool
    default: False
  enterprise_project_id:
    description:
      - Specifies the enterprise project ID, which is used to specify the enterprise project to which the AS group belongs.
    type: str
  multi_az_priority_policy:
    description:
      - Specifies the priority policy used to select target AZs when adjusting the number of instances in an AS group.
      - EQUILIBRIUM_DISTRIBUTE (default): When adjusting the number of instances, ensure that instances in each AZ in the available_zones list is evenly distributed. If instances cannot be added in the target AZ, select another AZ based on the PICK_FIRST policy.
      - PICK_FIRST: When adjusting the number of instances, target AZs are determined in the order in the available_zones list.
    choices: ['equilibrium_distribute', 'pick_first']
    type: str
    default: "equilibrium_distribute"
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
# Create as group.
- as_group:
    name: my_prod_as_group
  register: data
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class ASGroupModule(OTCModule):
    argument_spec = dict(
        scaling_group_name=dict(required=True),
        scaling_group_id=dict(required=False),
        scaling_configuration=dict(required=False),
        desire_instance_number=dict(required=False, type='int'),
        min_instance_number=dict(required=False, type='int', default=0),
        max_instance_number=dict(required=False, type='int', default=0),
        cool_down_time=dict(required=False, type='int', default=300),
        lb_listener=dict(required=False),
        lbaas_listeners=dict(required=False, type='list', elements='str'),
        available_zones=dict(required=False, type='list', elements='str'),
        networks=dict(required=False, type='list', elements='dict'),
        security_groups=dict(required=False, type='list', elements='dict'),
        vpc=dict(required=False),
        health_periodic_audit_method=dict(required=False, choices=['elb_audit', 'nova_audit'], default='nova_audit'),
        health_periodic_audit_time=dict(required=False, type='int', default=5),
        health_periodic_audit_grace_period=dict(required=False, type='int', default=600),
        instance_terminate_policy=dict(required=False, choices=['old_config_old_instance', 'old_config_new_instance', 'old_instance', 'new_instance']),
        notifications=dict(required=False, type='list', elements='str'),
        delete_publicip=dict(required=False, type='bool', default=False),
        delete_volume=dict(required=False, type='bool', default=False),
        enterprise_project_id=dict(required=False),
        multi_az_priority_policy=dict(required=False, choices=['equilibrium_distribute', 'pick_first'], type='str', default='equilibrium_distribute'),
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['scaling_group_name', 'networks', 'vpc']),
            ('scaling_group_name', None, ['scaling_group_id']),
            ('lb_listener', None, ['lbaas_listeners']),
            ('lbaas_listeners', None, ['lb_listener']),
        ],
        supports_check_mode=True
    )

    def changed_when_update(self, as_group, **attrs):
        changed = False
        if (((as_group.scaling_group_name != attrs['scaling_group_name'])
                and ('scaling_group_name' in attrs))
            or ((as_group.scaling_configuration != attrs['scaling_configuration'])
                and ('scaling_configuration' in attrs))
            or ((as_group.desire_instance_number != attrs['desire_instance_number'])
                and ('desire_instance_number' in attrs))
            or ((as_group.min_instance_number != attrs['min_instance_number'])
                and ('min_instance_number' in attrs))
            or ((as_group.max_instance_number != attrs['max_instance_number'])
                and ('max_instance_number' in attrs))
            or ((as_group.cool_down_time != attrs['cool_down_time'])
                and ('cool_down_time' in attrs))
            or ((as_group.lb_listener != attrs['lb_listener'])
                and ('lb_listener' in attrs))
            or ((as_group.lbaas_listeners != attrs['lbaas_listeners'])
                and ('lbaas_listeners' in attrs))
            or ((as_group.available_zones != attrs['available_zones'])
                and ('available_zones' in attrs))
            or ((as_group.networks != attrs['networks'])
                and ('networks' in attrs))
            or ((as_group.security_groups != attrs['security_groups'])
                and ('security_groups' in attrs))
            or ((as_group.vpc != attrs['vpc'])
                and ('vpc' in attrs))
            or ((as_group.health_periodic_audit_method != attrs['health_periodic_audit_method'])
                and ('health_periodic_audit_method' in attrs))
            or ((as_group.health_periodic_audit_time != attrs['health_periodic_audit_time'])
                and ('health_periodic_audit_time' in attrs))
            or ((as_group.health_periodic_audit_grace_period != attrs['health_periodic_audit_grace_period'])
                and ('health_periodic_audit_grace_period' in attrs))
            or ((as_group.instance_terminate_policy != attrs['instance_terminate_policy'])
                and ('instance_terminate_policy' in attrs))
            or ((as_group.notifications != attrs['notifications'])
                and ('notifications' in attrs))
            or ((as_group.delete_publicip != attrs['delete_publicip'])
                and ('delete_publicip' in attrs))
            or ((as_group.delete_volume != attrs['delete_volume'])
                and ('delete_volume' in attrs))
            or ((as_group.enterprise_project_id != attrs['enterprise_project_id'])
                and ('enterprise_project_id' in attrs))
            or ((as_group.multi_az_priority_policy != attrs['multi_az_priority_policy'])
                and ('multi_az_priority_policy' in attrs))):
            changed = True
        return changed


    def run(self):
        scaling_group_name = self.params['scaling_group_name']
        scaling_group_id = self.params['scaling_group_id']
        scaling_configuration = self.params['scaling_configuration']
        desire_instance_number = self.params['desire_instance_number']
        min_instance_number = self.params['min_instance_number']
        max_instance_number = self.params['max_instance_number']
        cool_down_time = self.params['cool_down_time']
        lb_listener = self.params['lb_listener']
        lbaas_listeners = self.params['lbaas_listeners']
        available_zones = self.params['available_zones']
        networks = self.params['networks']
        security_groups = self.params['security_groups']
        vpc = self.params['vpc']
        health_periodic_audit_method = self.params['health_periodic_audit_method']
        health_periodic_audit_time = self.params['health_periodic_audit_time']
        health_periodic_audit_grace_period = self.params['health_periodic_audit_grace_period']
        instance_terminate_policy = self.params['instance_terminate_policy']
        notifications = self.params['notifications']
        delete_publicip = self.params['delete_publicip']
        delete_volume = self.params['delete_volume']
        enterprise_project_id = self.params['enterprise_project_id']
        multi_az_priority_policy = self.params['multi_az_priority_policy']

        as_group = None

        if scaling_group_name:
            as_group = self.conn.auto_scaling.find_group(scaling_group_name, ignore_missing=True)
        else:
            as_group = self.conn.auto_scaling.find_group(scaling_group_id, ignore_missing=True)

        if self.params['state'] == 'present':

            attrs = {
                'scaling_group_name': scaling_group_name
            }

            attrs['scaling_configuration_id'] = self.conn.auto_scaling.find_config(self.params['scaling_configuration'],
                                                                                   ignore_missing=True)
            if not attrs['scaling_configuration_id']:
                self.fail_json("Scaling configuration not found")

            if self.params['lb_listener']:
                attrs['lb_listener_id'] = self.conn.network.find_listener(self.params['lb_listener'],
                                                                          ignore_missing=True)
                if not attrs['lb_listener_id']:
                    self.fail_json("lb_listener no found")
            else:
                attrs['lbaas_listeners'] = self.params['lbaas_listeners']

            attrs['vpc_id'] = self.conn.network.find_router(self.params['vpc'], ignore_missing=True)
            if not attrs['vpc_id']:
                self.fail_json("vpc no found")

            attrs['health_periodic_audit_method'] = self.params['health_periodic_audit_method'].upper()
            attrs['min_instance_number'] = self.params['min_instance_number']
            attrs['max_instance_number'] = self.params['max_instance_number']
            attrs['health_periodic_audit_time'] = self.params['health_periodic_audit_time']
            attrs['delete_publicip'] = self.params['delete_publicip']
            attrs['delete_volume'] = self.params['delete_volume']
            attrs['cool_down_time'] = self.params['cool_down_time']
            attrs['health_periodic_audit_grace_period'] = self.params['health_periodic_audit_grace_period']

            if desire_instance_number:
                attrs['desire_instance_number'] = self.params['desire_instance_number']
            if available_zones:
                attrs['available_zones'] = self.params['available_zones']
            if networks:
                attrs['networks'] = self.params['networks']
            if security_groups:
                attrs['security_groups'] = self.params['security_groups']
            if instance_terminate_policy:
                attrs['instance_terminate_policy'] = self.params['instance_terminate_policy']
            if notifications:
                attrs['notifications'] = self.params['notifications']
            if enterprise_project_id:
                attrs['enterprise_project_id'] = self.params['enterprise_project_id']
            if multi_az_priority_policy:
                attrs['multi_az_priority_policy'] = self.params['multi_az_priority_policy']

            if not as_group:

                as_group = self.conn.auto_scaling.create_group(**attrs)
                changed = True

                self.exit_json(
                    changed=changed,
                    as_group=as_group
                )

            else:
                as_group = self.conn.auto_scaling.update_group(**attrs)
                changed = self.changed_when_update(as_group, **attrs)

                self.exit_json(
                    changed=changed,
                    as_group=as_group
                )

        elif self.params['state'] == 'absent':
            if as_group:
                self.conn.auto_scaling.delete_group()
            else:
                self.fail_json("The group doesn't exist")




def main():
    module = ASGroupModule()
    module()


if __name__ == '__main__':
    main()