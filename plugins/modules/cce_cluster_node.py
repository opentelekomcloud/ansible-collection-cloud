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
    sample: {
        'annotation': 'abc123'
    }
  availability_zone:
    description: Availability zone
    type: str
    sample: eu-de-01
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
    sample: [
        {
            'SATA': 100
        },
        {
            'SAS': 200
        }
    ]
  dedicated_host:
    description:
      - ID of a Dedicated Host where the cluster node will be located to.
    type: str
    sample: 12223421354drfsadf123
  ecs_group:
    description: ID of the ECS group where the CCE node can belong to.
    type: str
  fault_domain:
    description: The node is created in the specified fault domain.
    type: str
  flavor:
    description:
      - Flavor ID of the cluster node
    type: str
    sample s2.large.2
  floating_ip:
    description: Floating IP used to connect to public networks.
    type: str
  k8s_tags:
    description: Dictionary of Kubernetes tags.
    type: dict
    sample: {
        "myk8s": "tag"
    }
  keypair:
    description:
      - Name of the public key to login
    type: str
  labels:
    description: Labels for the CCE cluster node
    type: dict
    sample: {
      'label1': 'mylabel'
    }
  lvm_config:
    description: ConfigMap of the Docker data disk.
    type: str
    sample: 'dockerThinpool=vgpaas/90%VG;kubernetesLV=vgpaas/10%VG;diskType=evs;lvType=linear'
  max_pods:
    description: Maximum number of pods on the node.
    type: int
    sample: 100
  name:
    description:
      - Name of the CCE cluster node.
    required: true
    type: str
  node_image_id:
    description: ID of a custom image used in a baremetall scenario.
    type: str
  offload_node:
    description: If node is offloading its components.
    type: bool
  os:
    description: Operating System of the cluster node.
    type: str
    sample 'CentOS 7.7'
  postinstall_script:
    description: Base64 encoded post installation script.
    type: str
  preinstall_script:
    description: Base64 encoded pre installation script.
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
    description: The CCE Cluster Node UUID.
    returned: On success when C(state=present)
    type: str
    sample: '39007a7e-ee4f-4d13-8283-b4da2e037c69'
cce_cluster_ node:
    description: Dictionary describing the Cluster Node.
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
        annotations=dict(required=False, type=dict),
        availability_zone=dict(required=False),
        cluster=dict(required=False),
        count=dict(required=False, type=int, default=1),
        data_volumes=dict(
            required=False,
            type='list',
            elements='dict'
        ),
        dedicated_host=dict(required=False),
        ecs_group=dict(required=False),
        fault_domain=dict(required=False),
        flavor=dict(required=False),
        floating_ip=dict(required=False),
        k8s_tags=dict(required=False, type=dict),
        keypair=dict(required=False),
        labels=dict(required=False, type=dict),
        lvm_config=dict(required=False),
        max_pods=dict(required=False, type=int),
        name=dict(required=True),
        node_image_id=dict(required=False),
        offload_node=dict(required=False, type=bool),
        os=dict(required=False),
        postinstall_script=dict(required=False),
        preinstall_script=dict(required=False),
        root_volume_size=dict(required=False, type=int, default=40),
        root_volume_type=dict(
            required=False,
            choices=['SATA', 'SAS', 'SSD'],
            default='SATA'),
        state=dict(default='present', choices=['absent', 'present']),
        tags=dict(required=False, type=list, elements=dict),
        timeout=dict(required=False, type='int', default=180),
        wait=dict(required=False, type='bool', default=True)
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present',
             ['az', 'cluster', 'flavor', 'keypair']),
            ('state', 'absent', ['cluster', 'name']),
        ]
    )

    otce_min__version = '0.13.0'

    def run(self):
        self.params['wait_timeout'] = self.params['timeout']
        cce_cluster = self.params['cluster']

        cluster = None
        data = None
        changed = False

        cluster = self.conn.cce.find_cluster(
            name_or_id=cce_cluster,
            ignore_missing=True)
        cluster_node = self.conn.cce.find_cluster_node(
            cluster=cluster,
            node=self.params['name'])

        if not cluster:
            self.fail_json(
                msg='CCE cluster %s not found by name or id.'
                    % cce_cluster
            )

        # Create CCE node
        if self.params['state'] == 'present':
            if not cluster_node:
                self.params.pop('cluster')
                cluster_node = self.conn.create_cce_cluster_node(
                    cluster=cluster.id,
                    **self.params
                )
                changed = True
            else:
                # Modify CCE Cluster Node
                # not available right now
                pass

            self.exit_json(
                changed=changed,
                cce_cluster_node=cluster_node.to_dict(),
                id=cluster_node.id
            )

        # CCE cluster node deletion
        elif self.params['state'] == 'absent':
            changed = False

            if cluster_node:
                attrs = {
                    'cluster': cluster.id
                    'node': cluster_node.id
                }
                if self.params['wait']:
                    attrs['wait'] = True
                if self.params['timeout']:
                    attrs['wait_timeout'] = self.params.['timeout']
                changed = True
                self.conn.cce.delete_cce_cluster_node(
                    cluster=cluster.id,
                    node=cluster_node.id,
                    **attrs
                )

            self.exit_json(changed=changed)


def main():
    module = CceClusterNodeModule()
    module()


if __name__ == '__main__':
    main()
