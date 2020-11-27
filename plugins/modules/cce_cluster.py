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
module: cce_cluster
short_description: Add/Delete CCE Cluster
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Artem Goncharov (@gtema)"
description:
  - Add or Remove CCE Cluster in OTC.
options:
  name:
    description: Name that has to be given to the cluster.
    required: true
    type: str
  state:
    description: Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
  flavor:
    description: Cluster flavor name.
    type: str
  type:
    description: Cluster type
    choices: [virtualmachine]
    default: virtualmachine
    type: str
  description:
    description: Cluster description.
    type: str
  router:
    description: Name or ID of the Neutron router.
    type: str
  network:
    description: Name or ID of the Neutron network.
    type: str
  container_network_mode:
    description: Network type.
    type: str
    choices: [overlay_l2, underlay_ipvlan, vpc-router]
  container_network_cidr:
    description: CIDR for the internal network.
    type: str
  external_ip:
    description: External IP to be assigned to the cluster.
    type: str
  version:
    description: Version of the Kubernetes.
    type: str
  authentication_mode:
    description: Cluster authentication mode.
    type: str
    choices: [rbac, x509, authenticating_proxy]
  authentication_proxy_ca:
    description: CA root certificate provided in the authenticating_proxy mode.
    type: str
  service_ip_range:
    description: |
      Service CIDR block or the IP address range which the
      kubernetes clusterIp must fall within.
    type: str
  kube_proxy_mode:
    description: Service forwarding mode.
    type: str
    choices: [iptables, ipvs]
  availability_zone:
    description: Cluster AZ. Use 'multi_az' for spreading muster nodes across
                 AZ.
    type: str
  wait:
    description:
      - If the module should wait for the cluster to be created or deleted.
    type: bool
    default: 'yes'
  timeout:
    description:
      - The amount of time the module should wait.
    default: 1800
    type: int
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
id:
    description: The CCE Cluster UUID.
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
'''

EXAMPLES = '''
- name: Create cluster
  opentelekomcloud.cloud.cce:
    name: "{{ cce_cluster_name }}"
    flavor: "{{ cce_flavor }}"
    description: "Ansible collection test"
    router: "{{ router_name }}"
    network: "{{ network_name }}"
    container_network_mode: "{{ container_network_mode }}"
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CceClusterModule(OTCModule):
    argument_spec = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['absent', 'present']),
        type=dict(type='str', default='virtualmachine',
                  choices=['virtualmachine']),
        flavor=dict(type='str'),
        description=dict(type='str'),
        router=dict(type='str'),
        network=dict(type='str'),
        container_network_mode=dict(
            type='str',
            choices=['overlay_l2', 'underlay_ipvlan', 'vpc-router']),
        container_network_cidr=dict(type='str'),
        external_ip=dict(type='str'),
        version=dict(type='str'),
        authentication_mode=dict(type='str', choices=['rbac', 'x509',
                                                      'authenticating_proxy']),
        authentication_proxy_ca=dict(type='str'),
        service_ip_range=dict(type='str'),
        kube_proxy_mode=dict(type='str', choices=['iptables', 'ipvs']),
        availability_zone=dict(type='str'),

        wait=dict(required=False, type='bool', default=True),
        timeout=dict(required=False, type='int', default=1800)
    )
    module_kwargs = dict(
        supports_check_mode=True,
        required_if=[
            ('state', 'present',
             ['flavor', 'router', 'network',
              'container_network_mode']),
            ('authentication_mode', 'authenticating_proxy',
             ['authentication_proxy_ca'])
        ]
    )

    otce_min_version = '0.11.0'

    def _system_state_change(self, cluster):
        state = self.params['state']
        if state == 'present':
            if not cluster:
                return True
            # TODO: check other parameters, whether update is required
        elif state == 'absent' and cluster:
            return True
        return False

    def run(self):
        self.params['wait_timeout'] = self.params['timeout']
        if self.params['type'].lower() == 'virtualmachine':
            self.params['type'] = 'VirtualMachine'

        cluster = None
        changed = False

        cluster = self.conn.cce.find_cluster(
            name_or_id=self.params['name'])

        if self.ansible.check_mode:
            self.exit_json(changed=self._system_state_change(cluster))

        if self.params['state'] == 'present':
            if not cluster:
                changed = True
                cluster = self.conn.create_cce_cluster(**self.params)
            else:
                # Decide whether update is required
                pass

            self.exit_json(
                changed=changed,
                cce_cluster=cluster.to_dict(),
                id=cluster.id
            )

        elif self.params['state'] == 'absent':
            changed = False

            if cluster:
                # TODO(gtema) perhaps delete all nodes here first
                attrs = {
                    'cluster': cluster.id
                }
                if self.params['wait']:
                    attrs['wait'] = True
                    if self.params['timeout']:
                        attrs['wait_timeout'] = self.params['timeout']

                changed = True
                self.conn.delete_cce_cluster(**attrs)

            self.exit_json(changed=changed)


def main():
    module = CceClusterModule()
    module()


if __name__ == '__main__':
    main()
