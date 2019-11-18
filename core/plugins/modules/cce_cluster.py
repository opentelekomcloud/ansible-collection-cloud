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
module: cce_cluster
short_description: Add/Delete CCE Cluster
extends_documentation_fragment: openstack
version_added: "2.9"
author: "Artem Goncharov (@gtema)"
description:
  - Add or Remove CCE Cluster in OTC
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
  flavor:
    description:
      - Cluster flavor name
    required: true
    choices: [cce.s1.small, cce.s1.medium, ...]
  cluster_type:
    description: Cluster type
    required: true
    choices: [baremetal, virtualmachine]
  description:
    description:
      - Cluster description
  router:
    description:
      - Name or ID of the Neutron router
    required: true
  network:
    description:
      - Name or ID of the Neutron network
    required: true
  network_mode:
    description: Network type
    required: true
    choices: [overlay_l2, underlay_ipvlan, vpc-router]
  wait:
    description:
      - If the module should wait for the cluster to be created or deleted.
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
cce_cluster:
    description: Dictionary describing the Cluster.
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


def _wait_for_cluster(module, cloud, lb, status, failures, interval=5):
    """Wait for cluster to be in a particular provisioning status."""
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


def _system_state_change(module, cloud, cluster):
    state = module.params['state']
    if state == 'present':
        if not cluster:
            return True
        # TODO: check other parameters, whether update is required
    elif state == 'absent' and cluster:
        return True
    return False


def main():
    argument_spec = openstack_full_argument_spec(
        name=dict(required=True),
        state=dict(default='present', choices=['absent', 'present']),
        cluster_type=dict(default=None,
                          choices=['virtualmachine', 'baremetal']),
        flavor=dict(default=None, choices=[
            'cce.s1.small',
            'cce.s1.medium'
        ]),
        description=dict(required=False),
        router=dict(default=None),
        network=dict(default=None),
        network_mode=dict(default=None, choices=['overlay_l2',
                                                  'underlay_ipvlan',
                                                  'vpc-router']),
        wait=dict(required=False, type=bool, default=True),
        timeout=dict(required=False, type=int, default=None)
    )
    module_kwargs = openstack_module_kwargs(
        required_if=[
            'state', 'present',
            ['flavor', 'cluster_type', 'router', 'network', 'network_mode']
        ]
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        **module_kwargs)
    sdk, cloud = openstack_cloud_from_module(module)

    name = module.params['name']
    cluster_type = module.params['cluster_type']
    flavor = module.params['flavor']
    description = module.params['description']
    router = module.params['router']
    network = module.params['network']
    network_mode = module.params['network_mode']
    timeout = module.params['timeout']

    cluster = None
    data = None

    try:
        changed = False
        cluster = cloud.cce.find_cluster(
            name_or_id=name)

        if module.check_mode:
            module.exit_json(changed=_system_state_change(module, cloud,
                                                          cluster))

        if module.params['state'] == 'present':
            if not cluster:
                cloud_network = cloud.network.find_network(network)
                cloud_router = cloud.network.find_router(router)
                if not cloud_network:
                    module.fail_json(
                        msg='Network %s is not found' % network
                    )
                if not cloud_router:
                    module.fail_json(
                        msg='Router %s is not found' % router
                    )

                cluster_type = 'BareMetal' \
                    if cluster_type.lower() == 'baremetal' \
                    else 'VirtualMachine'

                data = {
                    'metadata': {'name': name},
                    'spec': {
                        'type': cluster_type,
                        'version': 'v1.9.10-r2',
                        'hostNetwork': {
                            'vpc': cloud_router.id,
                            'subnet': cloud_network.id
                        },
                        'flavor': flavor,
                        'containerNetwork': {
                            'mode': network_mode,
                            'cidr': '172.16.0.0/16'
                        }
                    }
                }
                if description:
                    data['spec']['description'] = description

                cluster = cloud.cce.create_cluster(
                    **data
                )
                changed = True

                if not module.params['wait']:
                    module.exit_json(
                        changed=changed,
                        cce_cluster=cluster.to_dict(),
                        id=cluster.id
                    )

                if cluster.job_id:
                    cloud.cce.wait_for_job(cluster.job_id,
                                           wait=timeout)

                # Refetch the cluster
                cluster = cloud.cce.get_cluster(cluster)

            module.exit_json(
                changed=changed,
                cce_cluster=cluster.to_dict(),
                id=cluster.id
            )

        elif module.params['state'] == 'absent':
            changed = False

            if cluster:
                # TODO perhaps delete all nodes here first
                cloud.cce.delete_cluster(cluster)
                changed = True

            module.exit_json(changed=changed)
    except sdk.exceptions.OpenStackCloudException as e:
        params = {
            'msg': str(e),
            'extra_data': {
                'request_data': data,
                'data': e.extra_data,
                'details': e.details,
                'response': e.response.text
            }
        }
        module.fail_json(**params)


if __name__ == "__main__":
    main()
