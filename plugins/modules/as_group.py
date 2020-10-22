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
  max_instance_number:
    description:
      - Specifies the maximum number of instances. The default value is 0.
    type: int
  cool_down_time:
    description:
      - Specifies the cooldown period (in seconds). The value ranges from 0 to 86400 and is 300 by default.
      - After a scaling action is triggered, the system starts the cooldown period. During the cooldown period, scaling actions triggered by alarms will be denied. Scheduled, periodic, and manual scaling actions are not affected.
    type: int
  lb_listener:
    description:
      - Specifies ID or name of a classic load balancer listener. The system supports the binding of up to six load balancer listeners, the IDs of which are separated using a comma (,).
    type: str
  lbaas_listeners:
    description:
      - Specifies information about an enhanced load balancer.
    type: complex
    contains:
        pool_id:
            description: Specifies the backend ECS group ID.
            type: str
        protocol_port:
            description: Specifies the backend protocol ID, which is the port on which a backend ECS listens for traffic. The port ID ranges from 1 to 65535.
            type: int
        weight:
            description: Specifies the weight, which determines the portion of requests a backend ECS processes when being compared to other backend ECSs added to the same listener. The value of this parameter ranges from 0 to 100.
            type: int
  available_zones:
    description:
      - Specifies the AZ information. The ECS associated with a scaling action will be created in a specified AZ. If you do not specify an AZ, the system automatically specifies one.
    type: list
  networks:
    description:
      - Specifies network information. The system supports up to five subnets. The first subnet transferred serves as the primary NIC of the ECS by default.
      - Mandatory for creation of autoscaling group.
    type: complex
    contains:
        id:
            description: Specifies the network ID.
            type: str
  security_groups:
    description:
      - Specifies the security group. If the security group is specified both in the AS configuration and AS group, the security group specified in the AS configuration prevails. If the security group is not specified in either of them, the default security group is used.
    type: complex
    contains:
        id:
            description: Specifies the security group ID.
            type: str
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
  health_periodic_audit_time:
    description:
      -  Specifies the instance health check period.  The value can be 1, 5, 15, 60, or 180 in the unit of minutes. If this parameter is not specified, the default value is 5. If the value is set to 0, health check is performed every 10 seconds.
    type: int
  health_periodic_audit_grace_period:
    description:
      -  Specifies the grace period for instance health check. The unit is second and value range is 0-86400. The default value is 600. The health check grace period starts after an instance is added to an AS group and is enabled. The AS group will start checking the instance status only after the grace period ends.
      -  This parameter is valid only when the instance health check method of the AS group is ELB_AUDIT.
    type: int
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
  delete_volume:
    description:
      - Specifies whether to delete the data disks attached to the ECS when deleting the ECS.
    type: bool
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
        min_instance_number=dict(required=False, type='int'),
        max_instance_number=dict(required=False, type='int'),
        cool_down_time=dict(required=False, type='int'),
        lb_listener=dict(required=False),
        lbaas_listeners=dict(required=False, type='complex'),
        available_zones=dict(required=False, type='list', elements='str'),
        networks=dict(required=False, type='complex'),
        security_groups=dict(required=False, type='complex'),
        vpc=dict(required=False),
        health_periodic_audit_method=dict(required=False, choices=['elb_audit', 'nova_audit']),
        health_periodic_audit_time=dict(required=False, type='int'),
        health_periodic_audit_grace_period=dict(required=False, type='int'),
        instance_terminate_policy=dict(required=False, choices=['old_config_old_instance', 'old_config_new_instance', 'old_instance', 'new_instance']),
        notifications=dict(required=False, type='list', elements='str'),
        delete_publicip=dict(required=False, type='bool'),
        delete_volume=dict(required=False, type='bool'),
        enterprise_project_id=dict(required=False),
        multi_az_priority_policy=dict(required=False, choices=['equilibrium_distribute', 'pick_first'], type='str'),
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['scaling_group_name', 'networks', 'vpc_id']),
            ('scaling_group_name', None, [])
        ],
        supports_check_mode=True
    )

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

            if not as_group:

                attrs = {
                    'scaling_group_name': scaling_group_name
                }

                attrs['scaling_configuration_id'] = self.conn.auto_scaling.find_config(self.params['scaling_configuration'], ignore_missing=True)

                if not attrs['scaling_configuration_id']:
                    self.fail_json("Scaling configuration not found")

                if self.params['lb_listener']:
                    attrs['lb_listener_id'] = self.conn.network.find_listener(self.params['lb_listener'], ignore_missing=True)
                    if not attrs['lb_listener_id']:
                        self.fail_json("lb_listener no found")

                if self.params['vpc']:
                    attrs['vpc_id'] = self.conn.network.find_router(self.params['vpc'], ignore_missing=True)
                    if not attrs['vpc_id']:
                        self.fail_json("vpc no found")

                if desire_instance_number:
                    attrs['desire_instance_number'] = self.params['desire_instance_number']
                if min_instance_number:
                    attrs['min_instance_number'] = self.params['min_instance_number']
                if max_instance_number:
                    attrs['max_instance_number'] = self.params['max_instance_number']
                if cool_down_time:
                    attrs['cool_down_time'] = self.params['cool_down_time']
                if lbaas_listeners:
                    attrs['lbaas_listeners'] = self.params['lbaas_listeners']
                if available_zones:
                    attrs['available_zones'] = self.params['available_zones']
                if networks:
                    attrs['networks'] = self.params['networks']
                if security_groups:
                    attrs['security_groups'] = self.params['security_groups']
                if health_periodic_audit_method:
                    attrs['health_periodic_audit_method'] = self.params['health_periodic_audit_method']
                if health_periodic_audit_time:
                    attrs['health_periodic_audit_time'] = self.params['health_periodic_audit_time']
                if health_periodic_audit_grace_period:
                    attrs['health_periodic_audit_grace_period'] = self.params['health_periodic_audit_grace_period']
                if instance_terminate_policy:
                    attrs['instance_terminate_policy'] = self.params['instance_terminate_policy']
                if notifications:
                    attrs['notifications'] = self.params['notifications']
                if delete_publicip:
                    attrs['delete_publicip'] = self.params['delete_publicip']
                if delete_volume:
                    attrs['delete_volume'] = self.params['delete_volume']
                if enterprise_project_id:
                    attrs['enterprise_project_id'] = self.params['enterprise_project_id']
                if multi_az_priority_policy:
                    attrs['multi_az_priority_policy'] = self.params['multi_az_priority_policy']

                as_group = self.conn.auto_scaling.create_group(**attrs)
                changed = True

                self.exit_json(
                    changed=changed,
                    as_group=as_group
                )

            else:
                self.fail_json(
                    msg="VPC peering with this name already exists"
                )



def main():
    module = ASGroupModule()
    module()


if __name__ == '__main__':
    main()
