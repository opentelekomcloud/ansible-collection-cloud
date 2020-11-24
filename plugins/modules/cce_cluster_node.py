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
  annotations:
    description: Specifiy annotations for CCE node
    type: dict
  az:
    description: Availability zone
    type: str
  cluster:
    description:
      - CCE cluster name or id which hosts the cce cluster node
    type: str
  count:
    description:
      - Cluster node count which will be created.
      - If node count is greater than 1 the name of the node
      - gets a suffix.
    type: int
    default: 1
  data_volumes:
    description: List of data volumes attached to the cluster node.
    type: list
    elements: dict
    sample:
      - SATA: 100
        SAS: 120
  description:
    description:
      - Cluster node description
    type: str
  flavor:
    description:
      - Flavor of the cluster node
    type: str
  keypair:
    description:
      - Name of the public key to login
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
    default: SATA
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
    default: true
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
# Create CCE node
- cce_cluster_node:
    annotations:
        annotation1: 'myannotation'
    az: 'eu-de-02'
    cluster: '7ca53d10-2a70-11eb-9ade-0255ac101123'
    count: 1
    data_volumes:
        - SATA: 100
          SAS: 120
    description: 'my-node'
    flavor: 's2.large.2'
    keypair: 'my-pub-key'
    labels:
        mein: label
    name: "{{ cce_node_name }}"
    root_volume_size: 40
    root_volume_type:  SATA
    wait: false
  register: node

# Delete CCE node
- cce_cluster_node:
    cluster: '7ca53d10-2a70-11eb-9ade-0255ac101123'
    name: "{{ cce_node_name }}"
    state:absent
    wait: false
  register: node
 '''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CceClusterNodeModule(OTCModule):
    argument_spec = dict(
        annotations=dict(required=False, type='dict'),
        az=dict(required=False),
        cluster=dict(required=False),
        count=dict(required=False, type='int', default=1),
        data_volumes=dict(
            required=False,
            type='list',
            elements='dict'
        ),
        description=dict(required=False),
        flavor=dict(required=False),
        keypair=dict(required=False),
        labels=dict(required=False, type='dict'),
        name=dict(required=True),
        root_volume_size=dict(required=False, type='int', default=40),
        root_volume_type=dict(
            required=False,
            choices=['SATA', 'SAS', 'SSD'],
            default='SATA'),
        state=dict(default='present', choices=['absent', 'present']),
        timeout=dict(required=False, type='int', default=180),
        wait=dict(required=False, type='bool', default=True)
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present',
             ['az', 'cluster', 'flavor', 'keypair']),
            ('state', 'absent', ['cluster']),
        ]
    )

    def create_data_volumes(self, volume_list):
        volumes = []
        volume_types = ['SATA', 'SAS', 'SSD']

        if volume_list:
            for item in volume_list:
                for key in item:
                    if key not in volume_types:
                        self.fail_json(
                            msg='The specified data volume type %s does not '
                                'match the clouds specification: %s'
                                % (key, volume_types)
                        )
                    if not (100 <= item[key] <= 32768):
                        self.fail_json(
                            msg='The data volume size must be specified '
                                'between 100 and 32768 GB.'
                        )
                    volumes.append({
                        'volumetype': key,
                        'size': item[key]
                    })

        return volumes

    def run(self):
        annotations = self.params['annotations']
        az = self.params['az']
        cce_cluster = self.params['cluster']
        count = self.params['count']
        data_volumes = self.params['data_volumes']
        description = self.params['description']
        flavor = self.params['flavor']
        keypair = self.params['keypair']
        labels = self.params['labels']
        name = self.params['name']
        root_volume_size = self.params['root_volume_size']
        root_volume_type = self.params['root_volume_type']
        timeout = self.params['timeout']
        wait = self.params['wait']

        cluster = None
        data = None
        changed = False

        cluster = self.conn.cce.find_cluster(
            name_or_id=cce_cluster,
            ignore_missing=True)
        cluster_node = self.conn.cce.find_cluster_node(
            cluster=cluster,
            node=name)

        if not cluster:
            self.fail_json(
                msg='CCE cluster %s not found by name or id.'
                    % cce_cluster
            )

        # Create CCE node
        if self.params['state'] == 'present':
            if not cluster_node:
                if data_volumes:
                    data_volumes = self.create_data_volumes(data_volumes)
                if root_volume_size and (root_volume_size < 40):
                    self.fail_json(
                        msg='root_volume_size %s is smaller than 40 GB'
                            % root_volume_size)

                data = {
                    'kind': 'Node',
                    'apiVersion': 'v3',
                    'metadata': {
                        'name': name,
                        'labels': labels,
                        'annotations': annotations
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
                        'dataVolumes': data_volumes,
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
                    node_id=cluster_node.id
                )

            self.exit_json(
                changed=changed,
                cce_cluster_node=cluster_node.to_dict(),
                id=cluster_node.id
            )

        # CCE cluster node deletion
        elif self.params['state'] == 'absent':
            changed = False

            if cluster_node:
                info = self.conn.cce.delete_cluster_node(
                    cluster=cce_cluster,
                    node=cluster_node.id)
                if self.params['wait'] and info.job_id:
                    self.conn.cce.wait_for_job(info.job_id, wait=timeout)

                changed = True

            self.exit_json(changed=changed)


def main():
    module = CceClusterNodeModule()
    module()


if __name__ == '__main__':
    main()
