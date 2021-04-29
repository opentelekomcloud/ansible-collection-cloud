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
module: loadbalancer
short_description: Add/Delete load balancer from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Artem Goncharov (@gtema)"
description:
  - Add or Remove Enhanced Load Balancer from the OTC load-balancer
    service(ELB).
options:
  name:
    description:
      - Name that has to be given to the load balancer
    required: true
    type: str
  state:
    description:
      - Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
  vip_subnet:
    description:
      - The name or id of the subnet for the virtual IP of the load balancer.
        One of I(vip_network), I(vip_subnet), or I(vip_port) must be specified
        for creation.
    type: str
  vip_address:
    description:
      - IP address of the load balancer virtual IP.
    type: str
  public_ip_address:
    description:
      - Public IP address associated with the VIP.
    type: str
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
    type: int
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
- opentelekomcloud.cloud.loadbalancer:
    state: present
    name: my_lb
    vip_subnet: my_subnet
    timeout: 150

# Create a load balancer together with its sub-resources in the 'all in one'
# way. A public IP address is also allocated to the load balancer VIP.
- opentelekomcloud.cloud.loadbalancer:
    name: ELB
    state: present
    vip_subnet: default_subnet
    auto_public_ip: yes
    wait: yes
    timeout: 600

# Delete a load balancer(and all its related resources)
- opentelekomcloud.cloud.loadbalancer:
    state: absent
    name: my_lb

# Delete a load balancer(and all its related resources) together with the
# public IP address(if any) attached to it.
- opentelekomcloud.cloud.loadbalancer:
    state: absent
    name: my_lb
    delete_public_ip: yes
'''

import time

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LoadBalancerModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        state=dict(default='present', choices=['absent', 'present']),
        vip_subnet=dict(required=False),
        vip_address=dict(required=False),
        public_ip_address=dict(required=False, default=None),
        auto_public_ip=dict(required=False, default=False, type='bool'),
        delete_public_ip=dict(required=False, default=False, type='bool'),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def _wait_for_lb(self, lb, status, failures, interval=5):
        """Wait for load balancer to be in a particular provisioning status."""
        timeout = self.params['timeout']

        total_sleep = 0
        if failures is None:
            failures = []

        while total_sleep < timeout:
            lb = self.conn.network.get_load_balancer(lb.id)

            if lb:
                if lb:
                    return None
            else:
                if status == "DELETED":
                    return None
                else:
                    self.fail_json(
                        msg="Load Balancer %s transitioned to DELETED" % lb.id
                    )

            time.sleep(interval)
            total_sleep += interval

        self.fail_json(
            msg="Timeout waiting for Load Balancer %s to transition to %s" %
                (lb.id, status)
        )

    def bind_floating_ip(self, lb, public_vip_address, allocate_fip):
        fip = None
        orig_public_ip = None
        new_public_ip = None
        changed = False
        if public_vip_address or allocate_fip:
            ips = self.conn.network.ips(
                port_id=lb.vip_port_id,
                fixed_ip_address=lb.vip_address
            )
            ips = list(ips)
            if ips:
                orig_public_ip = ips[0]
                new_public_ip = orig_public_ip.floating_ip_address

        if (
            public_vip_address
            and public_vip_address != orig_public_ip.floating_ip_address
        ):
            fip = self.conn.network.find_ip(public_vip_address)
            if not fip:
                self.fail_json(
                    msg='Public IP %s is unavailable' % public_vip_address
                )

            if orig_public_ip:
                # Release origin public ip first
                self.conn.network.update_ip(
                    orig_public_ip,
                    fixed_ip_address=None,
                    port_id=None
                )

            # Associate new public ip
            self.conn.network.update_ip(
                fip,
                fixed_ip_address=lb.vip_address,
                port_id=lb.vip_port_id
            )

            new_public_ip = public_vip_address
            changed = True
        elif allocate_fip and not orig_public_ip:
            fip = self.conn.network.find_available_ip()
            if not fip:

                pub_net = self.conn.get_network('admin_external_net')
                if not pub_net:
                    self.fail_json(
                        msg='Public network admin_external_net not found'
                    )
                fip = self.conn.network.create_ip(
                    floating_network_id=pub_net.id
                )

            self.conn.network.update_ip(
                fip,
                fixed_ip_address=lb.vip_address,
                port_id=lb.vip_port_id
            )

            new_public_ip = fip.floating_ip_address
            changed = True

        return (new_public_ip, changed)

    def run(self):
        vip_subnet = self.params['vip_subnet']
        public_vip_address = self.params['public_ip_address']
        allocate_fip = self.params['auto_public_ip']
        delete_fip = self.params['delete_public_ip']

        vip_subnet_id = None

        lb = None

        changed = False
        lb = self.conn.network.find_load_balancer(
            name_or_id=self.params['name'])

        if self.params['state'] == 'present':
            if not lb:
                if vip_subnet:
                    subnet = self.conn.get_subnet(vip_subnet)
                    if not subnet:
                        self.fail_json(
                            msg='subnet %s is not found' % vip_subnet
                        )
                    vip_subnet_id = subnet.id

                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                lb = self.conn.network.create_load_balancer(
                    name=self.params['name'],
                    vip_subnet_id=vip_subnet_id,
                    vip_address=self.params['vip_address'],
                )
                changed = True

            if not self.params['wait']:
                if self.ansible.check_mode:
                    self.exit_json(changed=False)
                self.exit_json(
                    changed=changed,
                    loadbalancer=lb.to_dict(),
                    id=lb.id
                )

            self._wait_for_lb(lb, "ACTIVE", ["ERROR"])

            # Associate public ip to the load balancer VIP. If
            # public_vip_address is provided, use that IP, otherwise, either
            # find an available public ip or create a new one.
            (floating_ip, ip_changed) = self.bind_floating_ip(
                lb, public_vip_address, allocate_fip)

            if floating_ip:
                # Include public_vip_address in the result.
                lb = self.conn.network.find_load_balancer(name_or_id=lb.id)
                lb_dict = lb.to_dict()
                lb_dict.update({"public_vip_address": floating_ip})
                changed = changed and ip_changed

                self.exit_json(
                    changed=changed,
                    loadbalancer=lb_dict,
                    id=lb.id
                )

            self.exit_json(
                changed=changed,
                loadbalancer=lb.to_dict(),
                id=lb.id
            )

        elif self.params['state'] == 'absent':
            changed = False
            public_vip_address = None

            if lb:
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                if delete_fip:
                    ips = self.conn.network.ips(
                        port_id=lb.vip_port_id,
                        fixed_ip_address=lb.vip_address
                    )
                    ips = list(ips)
                    if ips:
                        public_vip_address = ips[0]

                self.conn.network.delete(
                    '/lbaas/loadbalancers/{id}?cascade=true'.format(id=lb.id))
                changed = True

                if delete_fip and public_vip_address:
                    self.conn.network.delete_ip(public_vip_address)
                    changed = True

            self.exit_json(changed=changed)


def main():
    module = LoadBalancerModule()
    module()


if __name__ == '__main__':
    main()
