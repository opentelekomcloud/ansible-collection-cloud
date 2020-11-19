#!/usr/bin/python
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = '''
---
module: cce_cluster_node
short_description: Add/Delete CCE Cluster node
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: '0.3.0'
author: 'Tino Schreiber (@tischrei)'
description:
  - Add or Remove CCE Cluster node in OTC
options:
  az:
    description:
      - Availability zone
      - Mandatory for creation
    type: str
  cluster:
    description:
      - CCE cluster name or id which hosts the cce cluster node
    type: str
  count:
    description:
      - Cluster node count which will be created.
    type: int
  description:
    description:
      - Cluster description
    type: str
  flavor:
    description:
      - Flavor of the cluster node
    type: str
  keypair:
    description:
      - Name of the public key to login
      - Mandatory for cluster node creation
    type: str
  name:
    description:
      - Name of the CCE cluster node.
    required: true
    type: str
  root_volume_size:
    description:
      - Size of the root volume
    type: int
    default: 40
  root_volume_type:
    description:
      - Type of the cluster node
    type: str
    choices: [SATA, SAS, SSD]
  state:
    description:
      - Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
  wait:
    description:
      - If the module should wait for the cluster node to be
      - created or deleted.
    type: bool
    default: 'yes'
  timeout:
    description:
      - The amount of time the module should wait.
    default: 180
    type: int
requirements: ['openstacksdk', 'otcextensions']
'''

RETURN = '''
id:
    description: The CCE Cluster UUID.
    returned: On success when C(state=present)
    type: str
    sample: '39007a7e-ee4f-4d13-8283-b4da2e037c69'
cce_cluster:
    description: Dictionary describing the Cluster.
    returned: On success when C(state=present)
    type: complex
    contains:
        id:
            description: Unique UUID.
            type: str
            sample: '39007a7e-ee4f-4d13-8283-b4da2e037c69'
        name:
            description: Name given to the load balancer.
            type: str
            sample: 'elb_test'
'''

EXAMPLES = '''
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CceClusterNodeModule(OTCModule):
    argument_spec = dict(
        az=dict(required=False),
        cluster=dict(required=False),
        count=dict(required=False, type='int', default=1),
        description=dict(required=False),
        flavor=dict(required=False),
        keypair=dict(required=False),
        name=dict(required=True),
        root_volume_size=dict(required=False, type='int', default=40),
        root_volume_type=dict(
            required=False,
            choices=['SATA', 'SAS', 'SSD'],
            default='SATA'
        ),
        wait=dict(required=False, type='bool', default=True),
        timeout=dict(required=False, type='int', default=180)
    )
    module_kwargs = dict(
        required_if=[
            ('state',
             'present',
             ['az', 'cluster', 'flavor']),
        ]
    )

    def run(self):
        az = self.params['az']
        cce_cluster = self.params['cluster']
        count = self.params['count']
        description = self.params['description']
        flavor = self.params['flavor']
        keypair = self.params['keypair']
        name = self.params['name']
        root_volume_size = self.params['root_volume_size']
        root_volume_type = self.params['root_volume_type']
        wait = self.params['wait']
        timeout = self.params['timeout']

        cluster = None
        data = None
        changed = False

        cluster = self.conn.cce.find_cluster(
            name_or_id=name,
            ignore_missing=True)
        if not cluster:
            self.fail_json(
                msg='CCE cluster %s not found by name or id.'
                    % cce_cluster
            )

        if self.params['state'] == 'present':
            '''
            cluster_node = self.conn.cce.find_cluster_node(
                cluster=cluster,
                node=name
            )
            '''
            data = {
                'kind': 'Node',
                'apiVersion': 'v3',
                'metadata': {
                    'name': name,
                    'labels': {
                        'foo': 'bar'
                    },
                    'annotations': {
                        'annotation1': 'abc'
                    }
                },
                'spec': {
                    'flavor': flavor,
                    'az': az,
                    'login': {
                        'sshKey': keypair
                    },
                    'rootVolume': {
                        'size': root_volume_size,
                        'volumetype': root_volume_type
                    },
                    'dataVolumes': [
                        {
                            'size': 100,
                            'volumetype': 'SAS'
                        }
                    ],
                    'count': count,
                }
            }

            if description:
                data['spec']['description'] = description

            cluster_node = self.conn.cce.create_cluster_node(
                cluster=cluster,
                **data
            )
            changed = True

            if not self.params['wait']:
                self.exit_json(
                    changed=changed,
                    cce_cluster_node=cluster_node.to_dict(),
                    id=cluster_node.id
                )

            if cluster_node.job_id:
                self.conn.cce.wait_for_job(
                    cluster_node.job_id,
                    wait=timeout
                )

            # Refetch the cluster node
            cluster_node = self.conn.cce.get_cluster_node(
                cluster=cluster,
                cluster_node.id
            )

        self.exit_json(
            changed=changed,
            cce_cluster_node=cluster_node.to_dict(),
            id=cluster_node.id
        )
        '''
        elif self.params['state'] == 'absent':
            changed = False

            if cluster:
                # TODO perhaps delete all nodes here first
                self.conn.cce.delete_cluster(cluster)
                changed = True

            self.exit_json(changed=changed)
        '''


def main():
    module = CceClusterNodeModule()
    module()


if __name__ == '__main__':
    main()
