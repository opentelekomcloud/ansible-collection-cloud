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
  - Add or Remove CCE Cluster in OTC
options:
  name:
    description:
      - Name that has to be given to the CCE cluster
    required: true
    type: str
  state:
    description:
      - Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
  flavor:
    description:
      - Cluster flavor name
    required: true
    choices: [cce.s1.small, cce.s1.medium]
    type: str
  cluster_type:
    description: Cluster type
    choices: [baremetal, virtualmachine]
    required: true
    type: str
  cluster_version:
    description:
      - Version of the CCE cluster.
      - If not provided, the newest version will be used
    required: false
    type: str
  description:
    description:
      - Cluster description
    type: str
  router:
    description:
      - Name or ID of the Neutron router
    required: true
    type: str
  network:
    description:
      - Name or ID of the Neutron network
    required: true
    type: str
  network_mode:
    description: Network type
    required: true
    type: str
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
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CceClusterModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        state=dict(default='present', choices=['absent', 'present']),
        cluster_type=dict(required=True, choices=['virtualmachine', 'baremetal']),
        cluster_version=dict(required=False),
        flavor=dict(required=True, choices=[
            'cce.s1.small',
            'cce.s1.medium'
        ]),
        description=dict(required=False),
        router=dict(required=True),
        network=dict(required=True),
        network_mode=dict(required=True, choices=['overlay_l2',
                                                  'underlay_ipvlan',
                                                  'vpc-router']),
        wait=dict(required=False, type='bool', default=True),
        timeout=dict(required=False, type='int', default=180)
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present',
             ['flavor', 'cluster_type', 'router', 'network', 'network_mode'])
        ]
    )

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
        name = self.params['name']
        cluster_type = self.params['cluster_type']
        cluster_version = self.params['cluster_version']
        flavor = self.params['flavor']
        description = self.params['description']
        router = self.params['router']
        network = self.params['network']
        network_mode = self.params['network_mode']
        timeout = self.params['timeout']

        cluster = None
        data = None
        changed = False

        cluster = self.conn.cce.find_cluster(
            name_or_id=name)

        if self.check_mode:
            self.exit_json(changed=self._system_state_change(cluster))

        if self.params['state'] == 'present':
            if not cluster:
                cloud_network = self.conn.network.find_network(network)
                cloud_router = self.conn.network.find_router(router)
                if not cloud_network:
                    self.fail_json(
                        msg='Network %s is not found' % network
                    )
                if not cloud_router:
                    self.fail_json(
                        msg='Router %s is not found' % router
                    )

                cluster_type = 'BareMetal' \
                    if cluster_type.lower() == 'baremetal' \
                    else 'VirtualMachine'

                data = {
                    'metadata': {'name': name},
                    'spec': {
                        'type': cluster_type,
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
                if cluster_version:
                    data['spec']['version'] = cluster_version

                cluster = self.conn.cce.create_cluster(
                    **data
                )
                changed = True

                if not self.params['wait']:
                    self.exit_json(
                        changed=changed,
                        cce_cluster=cluster.to_dict(),
                        id=cluster.id
                    )

                if cluster.job_id:
                    self.conn.cce.wait_for_job(cluster.job_id,
                                               wait=timeout)

                # Refetch the cluster
                cluster = self.conn.cce.get_cluster(cluster)
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
                # TODO perhaps delete all nodes here first
                self.conn.cce.delete_cluster(cluster)
                changed = True

            self.exit_json(changed=changed)


def main():
    module = CceClusterModule()
    module()


if __name__ == '__main__':
    main()
