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
module: cce_node_pool
short_description: Add/Delete CCE Node Pool
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: '0.5.0'
author: 'Tino Schreiber (@tischrei)'
description:
  - Add or Remove CCE Node Pool in OTC
options:
  availability_zone:
    description: Availability zone or 'random' for all zones
    type: str
    default: random
  autoscaling_enabled:
    description: Enable or disable Autoscaling
    type: bool
    default: False
  cluster:
    description:
      - CCE cluster name or id which hosts the CCE Node Pool
    type: str
  data_volumes:
    description: List of data volumes attached to the cluster node.
    type: list
    elements: dict
    default: [{'volumetype': 'SATA', 'size': 100, 'encrypted': False, 'cmk_id': ''}]
  ecs_group:
    description: ID of the ECS group where the CCE node can belong to.
    type: str
  flavor:
    description: Flavor ID of the cluster node
    type: str
  initial_node_count:
    description: Expected number of nodes in this node pool.
    type: int
  k8s_tags:
    description: Dictionary of Kubernetes tags.
    type: dict
  lvm_config:
    description: ConfigMap of the Docker data disk.
    type: str
  max_node_count:
    description: Maximum number of nodes after scale-up.
    type: int
  min_node_count:
    description: Minimum number of nodes after a scale-down.
    type: int
  max_pods:
    description: Maximum number of pods on the node.
    type: int
  name:
    description:
      - Name of the CCE Node Pool
    required: true
    type: str
  network:
    description:
      - ID of the network to which the CCE node pool belongs to.
    type: str
  node_image_id:
    description:
      - Mandatory if custom image is used on a
      - bare metall node.
    type: str
  os:
    description: Operating System of the cluster node.
    type: str
  postinstall_script:
    description: Base64 encoded post installation script.
    type: str
  preinstall_script:
    description: Base64 encoded pre installation script.
    type: str
  priority:
    description: Node pool weight for scale-up operations.
    type: int
  public_key:
    description: Additional public key to be added for login.
    type: str
  root_volume_size:
    description:
      - Size of the root volume
    type: int
    default: 40
  root_volume_type:
    description:
      - Type of the root volume.
    type: str
    choices: [SATA, SAS, SSD]
    default: SATA
  scale_down_cooldown_time:
    description:
      - Interval in minutes during which nodes added after a scale-up will
      - not be deleted.
    type: int
  ssh_key:
    description: Name of the public key to login into the nodes
    type: str
  state:
    description:
      - Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
  tags:
    description: List of tags used to build UI labels.
    type: list
    elements: dict
  taints:
    description: List of taints.
    type: list
    elements: dict
requirements: ['openstacksdk', 'otcextensions']
'''

RETURN = '''
id:
  description: The CCE Node Pool UUID.
  returned: On success when C(state=present)
  type: str
  sample: '39007a7e-ee4f-4d13-8283-b4da2e037123'
cce_node_pool:
  description: Dictionary describing the CCE Node Pool.
  returned: On success when C(state=present)
  type: dict
  sample: {
    'api_version': 'v3',
    'id': 'e2d0d5f3-572e-11eb-8fea-0255ac101123',
    'kind': 'NodePool',
    'metadata': null,
    'name': 'test-ansible2',
    'spec': {
      'autoscaling': {
        'enable': true,
        'max_node_count': 3,
        'min_node_count': 1,
        'priority': 2,
        'scale_down_cooldown_time': 5
      },
      'initial_node_count': 0,
      'node_management': {
        'ecs_group': null,
      },
      'node_pool_type': 'vm',
      'node_template_spec': {
        'availability_zone': 'random',
        'billing_mode': 0,
        'count': null,
        'data_volumes': [
          {
            'extend_params': null,
            'metadata': null,
            'size': 120,
            'type': 'SSD'
          },
          {
            'extend_params': null,
            'metadata': null,
            'size': 100,
            'type': 'SATA'
          }
        ],
        'ecs_group': null,
        'extend_params': {
          'lvm_config': null,
          'max_pods': 110,
          'node_image_id': null,
          'postinstall_script': null,
          'preinstall_script': null,
          'public_key': 'ssh_pubkey_value'
        },
        'flavor': 's2.large.2',
        'floating_ip': {
          'count': null,
          'floating_ip_spec': {
            'bandwidth': {}
          },
          'ids': null,
        },
        'k8s_tags': {
          'cce.cloud.com/cce-nodepool': 'nodepool-name',
          'mysecondtag': 'mysecondvalue',
          'mytag': 'myvalue'
        },
        'login': {
          'ssh_key': 'tischrei-pub'
        },
        'node_nic_spec': {
          'primary_nic': {
            'network_id': '25d24fc8-d019-4a34-9fff-0a09fde6a123'
          }
        },
        'os': 'CentOS 7.7',
        'root_volume': {
          'size': 40,
          'type': 'SATA'
        },
        'tags': [
          {
            'key': 'my_first_key',
            'value': 'my_first_value'
          },
          {
            'key': 'my_second_key',
            'value': 'my_secound_value'
          }
        ],
        'taints': [
          {
            'effect': 'NoSchedule',
            'key': 'first_taint_key',
            'value': 'first_taint_value'
          },
          {
            'effect': 'NoExecute',
            'key': 'second_taint_key',
            'value': 'secound_taint_value'
          }
        ]
      }
    },
    'status': {
      'current_node': 0,
      'status': ''
    }
  }
'''

EXAMPLES = '''
# Create CCE Node Pool with minimal configuration
- cce_node_pool:
    cloud: "{{ test_cloud }}"
    cluster: clustername
    flavor: s2.large.2
    os: 'CentOS 7.7'
    name: my-nodepool
    network: '25d24fc8-d019-4a34-9fff-0a09fde6a123'
    ssh_key: 'ssh-pub'
    state: present
  register: pool

# Create CCE Node Pool with fine-grained configuration
- cce_node_pool:
    cloud: "{{ test_cloud }}"
    availability_zone: "random"
    autoscaling_enabled: True
    cluster: tino-test
    data_volumes:
      - volumetype: SSD
        size: 120
      - volumetype: SATA
        size: 100
        encrypted: False
        cmk_id: ''
    flavor: s2.large.2
    initial_node_count: 0
    k8s_tags:
      mytag: myvalue
      mysecondtag: mysecondvalue
    min_node_count: 1
    max_node_count: 3
    name: test-ansible2
    network: '25d24fc8-d019-4a34-9fff-0a09fde6a123'
    priority: 2
    os: 'CentOS 7.7'
    scale_down_cooldown_time: 5
    ssh_key: 'sshkey-pub'
    tags:
      - key: 'my_first_key'
        value: 'my_first_value'
      - key: 'my_second_key'
        value: 'my_secound_value'
    taints:
      - key: 'first_taint_key'
        value: 'first_taint_value'
        effect: 'NoSchedule'
      - key: 'second_taint_key'
        value: 'secound_taint_value'
        effect: 'NoExecute'
    state: present
  register: pool

# Delete CCE Node Pool
- opentelekomcloud.cloud.cce_node_pool:
    cluster: "{{ cluster_name_or_id }}"
    name: "{{ cce_node_pool_name_or_id }}"
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CceNodePoolModule(OTCModule):
    argument_spec = dict(
        availability_zone=dict(required=False, default="random"),
        autoscaling_enabled=dict(required=False, type='bool', default=False),
        cluster=dict(required=False),
        data_volumes=dict(
            required=False,
            type='list',
            elements='dict',
            default=[{
                'volumetype': 'SATA',
                'size': 100,
                'encrypted': False,
                'cmk_id': ''
            }]
        ),
        ecs_group=dict(required=False),
        flavor=dict(required=False),
        initial_node_count=dict(required=False, type='int', default=0),
        k8s_tags=dict(required=False, type='dict'),
        lvm_config=dict(required=False),
        min_node_count=dict(required=False, type='int'),
        max_node_count=dict(required=False, type='int'),
        max_pods=dict(required=False, type='int'),
        name=dict(required=True),
        network=dict(required=False),
        node_image_id=dict(required=False),
        os=dict(required=False),
        postinstall_script=dict(required=False),
        preinstall_script=dict(required=False),
        priority=dict(required=False, type='int'),
        public_key=dict(required=False),
        root_volume_size=dict(required=False, type='int', default=40),
        root_volume_type=dict(
            required=False,
            choices=['SATA', 'SAS', 'SSD'],
            default='SATA'),
        scale_down_cooldown_time=dict(required=False, type='int'),
        ssh_key=dict(required=False, no_log=False),
        state=dict(default='present', choices=['absent', 'present']),
        tags=dict(required=False, type='list', elements='dict'),
        taints=dict(required=False, type='list', elements='dict'),
    )
    module_kwargs = dict(
        supports_check_mode=True,
        required_if=[
            ('state', 'present',
                [
                    'cluster',
                    'flavor',
                    'os',
                    'name',
                    'network',
                    'ssh_key'
                ]),
            ('state', 'absent', ['cluster', 'name']),
        ]
    )

    otce_min_version = '0.13.0'

    def run(self):
        cce_cluster = self.params['cluster']

        cluster = None
        changed = False

        cluster = self.conn.cce.find_cluster(
            name_or_id=cce_cluster,
            ignore_missing=True)
        node_pool = self.conn.cce.find_node_pool(
            cluster=cluster,
            node_pool=self.params['name'])

        if not cluster:
            self.fail_json(
                msg='CCE cluster %s not found by name or id.'
                    % cce_cluster
            )

        # Create CCE node pool
        if self.params['state'] == 'present':
            if not node_pool:
                if self.ansible.check_mode:
                    self.exit(changed=True)
                self.params.pop('cluster')
                node_pool = self.conn.create_cce_node_pool(
                    cluster=cluster.id,
                    **self.params
                )
                changed = True
            else:
                # Modify CCE node pool not available right now
                if self.ansible.check_mode:
                    self.exit(changed=False)
                pass

            self.exit_json(
                changed=changed,
                cce_node_pool=node_pool.to_dict(),
                id=node_pool.id
            )

        # CCE node pool deletion
        elif self.params['state'] == 'absent':
            changed = False

            if node_pool:
                changed = True
                if self.ansible.check_mode:
                    self.exit(changed=True)
                self.conn.cce.delete_node_pool(
                    cluster=cluster.id,
                    node_pool=node_pool.id,
                )
            self.exit_json(changed=changed)


def main():
    module = CceNodePoolModule()
    module()


if __name__ == '__main__':
    main()
