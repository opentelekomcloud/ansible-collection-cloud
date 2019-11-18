#!/usr/bin/env python
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

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: loadbalancer
short_description: Add/Delete load balancer from OpenTelekomCloud
extends_documentation_fragment: openstack
version_added: "2.9"
author: "Artem Goncharov (@gtema)"
description:
  - Add or Remove Enhanced Load Balancer from the OTC load-balancer
    service(ELB).
options:
  name:
    description:
      - Name that has to be given to the load balancer
    required: true
  state:
    description:
      - Should the resource be present or absent.
    choices: [present, absent]
    default: present
  vip_subnet:
    description:
      - The name or id of the subnet for the virtual IP of the load balancer.
        One of I(vip_network), I(vip_subnet), or I(vip_port) must be specified
        for creation.
  vip_address:
    description:
      - IP address of the load balancer virtual IP.
  public_ip_address:
    description:
      - Public IP address associated with the VIP.
  auto_public_ip:
    description:
      - Allocate a public IP address and associate with the VIP automatically.
    type: bool
    default: 'no'
  delete_public_ip:
    description:
      - When C(state=absent) and this option is true, any public IP address
        associated with the VIP will be deleted along with the load balancer.
    type: bool
    default: 'no'
  wait:
    description:
      - If the module should wait for the load balancer to be created or
        deleted.
    type: bool
    default: 'yes'
  timeout:
    description:
      - The amount of time the module should wait.
    default: 180
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
id:
    description: The load balancer UUID.
    returned: On success when C(state=present)
    type: str
    sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
loadbalancer:
    description: Dictionary describing the load balancer.
    returned: On success when C(state=present)
    type: complex
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
        name:
            description: Name given to the load balancer.
            type: str
            sample: "elb_test"
        vip_network_id:
            description: Network ID the load balancer virutal IP port belongs in.
            type: str
            sample: "f171db43-56fd-41cf-82d7-4e91d741762e"
        vip_subnet_id:
            description: Subnet ID the load balancer virutal IP port belongs in.
            type: str
            sample: "c53e3c70-9d62-409a-9f71-db148e7aa853"
        vip_port_id:
            description: The load balancer virutal IP port ID.
            type: str
            sample: "2061395c-1c01-47ab-b925-c91b93df9c1d"
        vip_address:
            description: The load balancer virutal IP address.
            type: str
            sample: "192.168.2.88"
        public_vip_address:
            description: The load balancer public VIP address.
            type: str
            sample: "10.17.8.254"
        provisioning_status:
            description: The provisioning status of the load balancer.
            type: str
            sample: "ACTIVE"
        operating_status:
            description: The operating status of the load balancer.
            type: str
            sample: "ONLINE"
        is_admin_state_up:
            description: The administrative state of the load balancer.
            type: bool
            sample: true
        listeners:
            description: The associated listener IDs, if any.
            type: list
            sample: [{"id": "7aa1b380-beec-459c-a8a7-3a4fb6d30645"}, {"id": "692d06b8-c4f8-4bdb-b2a3-5a263cc23ba6"}]
        pools:
            description: The associated pool IDs, if any.
            type: list
            sample: [{"id": "27b78d92-cee1-4646-b831-e3b90a7fa714"}, {"id": "befc1fb5-1992-4697-bdb9-eee330989344"}]
'''

EXAMPLES = '''
# Create a load balancer by specifying the VIP subnet.
- loadbalancer:
    auth:
      auth_url: https://identity.example.com
      username: admin
      password: passme
      project_name: admin
    state: present
    name: my_lb
    vip_subnet: my_subnet
    timeout: 150

# Create a load balancer together with its sub-resources in the 'all in one'
# way. A public IP address is also allocated to the load balancer VIP.
- loadbalancer:
    name: ELB
    state: present
    vip_subnet: default_subnet
    auto_public_ip: yes
    wait: yes
    timeout: 600

# Delete a load balancer(and all its related resources)
- loadbalancer:
    auth:
      auth_url: https://identity.example.com
      username: admin
      password: passme
      project_name: admin
    state: absent
    name: my_lb

# Delete a load balancer(and all its related resources) together with the
# public IP address(if any) attached to it.
- loadbalancer:
    auth:
      auth_url: https://identity.example.com
      username: admin
      password: passme
      project_name: admin
    state: absent
    name: my_lb
    delete_public_ip: yes
'''

import time

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.opentelekomcloud.core.plugins.module_utils.otc \
    import openstack_full_argument_spec, \
    openstack_module_kwargs, openstack_cloud_from_module


def _wait_for_lb(module, cloud, lb, status, failures, interval=5):
    """Wait for load balancer to be in a particular provisioning status."""
    timeout = module.params['timeout']

    total_sleep = 0
    if failures is None:
        failures = []

    while total_sleep < timeout:
        lb = cloud.network.get_load_balancer(lb.id)

        if lb:
            if lb:
                return None
        else:
            if status == "DELETED":
                return None
            else:
                module.fail_json(
                    msg="Load Balancer %s transitioned to DELETED" % lb.id
                )

        time.sleep(interval)
        total_sleep += interval

    module.fail_json(
        msg="Timeout waiting for Load Balancer %s to transition to %s" %
            (lb.id, status)
    )


def bind_floating_ip(cloud, module, lb, public_vip_address, allocate_fip):
    fip = None
    orig_public_ip = None
    new_public_ip = None
    if public_vip_address or allocate_fip:
        ips = cloud.network.ips(
            port_id=lb.vip_port_id,
            fixed_ip_address=lb.vip_address
        )
        ips = list(ips)
        if ips:
            orig_public_ip = ips[0]
            new_public_ip = orig_public_ip.floating_ip_address

    if public_vip_address and public_vip_address != orig_public_ip:
        fip = cloud.network.find_ip(public_vip_address)
        if not fip:
            module.fail_json(
                msg='Public IP %s is unavailable' % public_vip_address
            )

        # Release origin public ip first
        cloud.network.update_ip(
            orig_public_ip,
            fixed_ip_address=None,
            port_id=None
        )

        # Associate new public ip
        cloud.network.update_ip(
            fip,
            fixed_ip_address=lb.vip_address,
            port_id=lb.vip_port_id
        )

        new_public_ip = public_vip_address
    elif allocate_fip and not orig_public_ip:
        fip = cloud.network.find_available_ip()
        if not fip:

            pub_net = cloud.get_network('admin_external_net')
            if not pub_net:
                module.fail_json(
                    msg='Public network admin_external_net not found'
                )
            fip = cloud.network.create_ip(
                floating_network_id=pub_net.id
            )

        cloud.network.update_ip(
            fip,
            fixed_ip_address=lb.vip_address,
            port_id=lb.vip_port_id
        )

        new_public_ip = fip.floating_ip_address

    return new_public_ip


def _system_state_change(module, cloud, lb):
    state = module.params['state']
    if state == 'present':
        if not lb:
            return True
    elif state == 'absent' and lb:
        return True
    return False


def main():
    argument_spec = openstack_full_argument_spec(
        name=dict(required=True),
        state=dict(default='present', choices=['absent', 'present']),
        vip_subnet=dict(required=False),
        vip_address=dict(required=False),
        public_ip_address=dict(required=False, default=None),
        auto_public_ip=dict(required=False, default=False, type='bool'),
        delete_public_ip=dict(required=False, default=False, type='bool'),
    )
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        **module_kwargs)
    sdk, cloud = openstack_cloud_from_module(module)

    vip_subnet = module.params['vip_subnet']
    public_vip_address = module.params['public_ip_address']
    allocate_fip = module.params['auto_public_ip']
    delete_fip = module.params['delete_public_ip']

    vip_subnet_id = None

    lb = None

    try:
        changed = False
        lb = cloud.network.find_load_balancer(
            name_or_id=module.params['name'])

        if module.check_mode:
            module.exit_json(changed=_system_state_change(module, cloud, lb))

        if module.params['state'] == 'present':
            if not lb:
                if vip_subnet:
                    subnet = cloud.get_subnet(vip_subnet)
                    if not subnet:
                        module.fail_json(
                            msg='subnet %s is not found' % vip_subnet
                        )
                    vip_subnet_id = subnet.id

                lb = cloud.network.create_load_balancer(
                    name=module.params['name'],
                    vip_subnet_id=vip_subnet_id,
                    vip_address=module.params['vip_address'],
                )
                changed = True

            if not module.params['wait']:
                module.exit_json(
                    changed=changed,
                    loadbalancer=lb.to_dict(),
                    id=lb.id
                )

            _wait_for_lb(module, cloud, lb, "ACTIVE", ["ERROR"])

            # Associate public ip to the load balancer VIP. If
            # public_vip_address is provided, use that IP, otherwise, either
            # find an available public ip or create a new one.
            floating_ip = bind_floating_ip(
                cloud, module, lb,
                public_vip_address, allocate_fip)

            if floating_ip:
                # Include public_vip_address in the result.
                lb = cloud.network.find_load_balancer(name_or_id=lb.id)
                lb_dict = lb.to_dict()
                lb_dict.update({"public_vip_address": floating_ip})
                changed = True

            module.exit_json(
                changed=changed,
                loadbalancer=lb.to_dict(),
                id=lb.id
            )

        elif module.params['state'] == 'absent':
            changed = False
            public_vip_address = None

            if lb:
                cloud.network.delete(
                    '/lbaas/loadbalancers/{id}?cascade=true'.format(id=lb.id))
                changed = True

                if delete_fip and lb.vip_address:
                    cloud.network.delete_ip(lb.vip_address)
                    changed = True

            module.exit_json(changed=changed)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)


if __name__ == "__main__":
    main()
