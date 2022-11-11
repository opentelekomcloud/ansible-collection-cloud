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
version_added: '0.4.0'
author: 'Tino Schreiber (@tischrei)'
description:
  - Add or Remove CCE Cluster node in OTC
options:
  annotations:
    description: Specifiy annotations for CCE node
    type: dict
  availability_zone:
    description: Availability zone
    type: str
  cluster:
    description:
      - CCE cluster name or id which hosts the cce cluster node
    type: str
    required: true
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
  dedicated_host:
    description:
      - ID of a Dedicated Host where the cluster node will be located to.
    type: str
  ecs_group:
    description: ID of the ECS group where the CCE node can belong to.
    type: str
  fault_domain:
    description: The node is created in the specified fault domain.
    type: str
  flavor:
    description: Flavor ID of the cluster node
    type: str
  floating_ip:
    description: Floating IP used to connect to public networks.
    type: str
  k8s_tags:
    description: Dictionary of Kubernetes tags.
    type: dict
  ssh_key:
    description: Name of the public key to login
    type: str
  labels:
    description: Labels for the CCE cluster node
    type: dict
  lvm_config:
    description: ConfigMap of the Docker data disk.
    type: str
  max_pods:
    description: Maximum number of pods on the node.
    type: int
  name:
    description:
      - Name of the CCE cluster node.
    required: true
    type: str
  network:
    description:
      - Network ID of the CCE cluster node.
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
      - Type of the root volume.
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
  tags:
    description: CCE cluster node tags
    type: list
    elements: dict
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
  sample: '39007a7e-ee4f-4d13-8283-b4da2e037123'
cce_cluster_node:
  description: Dictionary describing the Cluster Node.
  returned: On success when C(state=present)
  type: dict
  sample: {
      cce_cluster_node: {
          'api_version': 'v3',
          'id': 'a815a926-30cd-11eb-b02d-0255ac101123',
          'kind': 'Node',
          'location': {
              'cloud': 'otc',
              'project': {
                  'domain_id': null,
                  'domain_name': null,
                  'id': '16d53a84a13b49529d2e2c3646691123',
                  'name': 'eu-de'
              },
              'region_name': 'eu-de',
              'zone': null
          },
          'metadata': {
              'annotations': {
                  'annotation1': 'abc'
              },
              'created_at': null,
              'id': 'a815a926-30cd-11eb-b02d-0255ac101123',
              'labels': {
                  'mein': 'label'
              },
              'location': null,
              'name': 'testccenode',
              'updated_at': null
          },
          'name': 'testccenode',
          'spec': {
              'availability_zone': 'eu-de-02',
              'billing_mode': 0,
              'count': 1,
              'data_volumes': [
                  {
                      'id': null,
                      'location': null,
                      'name': null,
                      'size': 150,
                      'type': 'SATA'
                  },
                  {
                      'id': null,
                      'location': null,
                      'name': null,
                      'size': 100,
                      'type': 'SAS'
                  }
              ],
              'dedicated_host': null,
              'ecs_group': null,
              'extend_params': {
                  'id': null,
                  'location': null,
                  'lvm_config': null,
                  'max_pods': 16,
                  'name': null,
                  'node_image_id': null,
                  'postinstall_script': null,
                  'preinstall_script': null
              },
              'fault_domain': null,
              'flavor': 's2.large.2',
              'floating_ip': {
                  'count': null,
                  'floating_ip': {
                      'bandwidth': {}
                  },
                  'id': null,
                  'ids': null,
                  'location': null,
                  'name': null
              },
              'id': null,
              'k8s_tags': {
                  'kubernetes.io/eniquota': '12',
                  'kubernetes.io/subeniquota': '0',
                  'testtag': 'value'
              },
              'location': null,
              'login': {
                  'sshKey': 'sshkey-pub',
                  'userPassword': {}
              },
              'name': null,
              'offload_node': null,
              'os': 'CentOS 7.7',
              'root_volume': {
                  'id': null,
                  'location': null,
                  'name': null,
                  'size': 40,
                  'type': 'SATA'
              },
              'tags': [
                  {
                      'id': null,
                      'key': 'hellokey1',
                      'location': null,
                      'name': null,
                      'value': 'hellovalue1'
                  },
                  {
                      'id': null,
                      'key': 'hellokey2',
                      'location': null,
                      'name': null,
                      'value': 'hellovalue2'
                  }
              ],
              'taints': null
          },
          'status': {
              'floating_ip': null,
              'id': null,
              'instance_id': null,
              'job_id': 'a8168c15-30cd-11eb-b02d-0255ac101123',
              'location': null,
              'name': null,
              'private_ip': null,
              'status': null
          }
      }
  }
'''

EXAMPLES = '''
# Create CCE cluster node
- opentelekomcloud.cloud.cce_cluster_node:
    annotations:
      annotation1: 'abc'
    availability_zone: 'eu-de-02'
    cluster: "{{ cluster_name_or_id }}"
    count: 1
    data_volumes:
      - volumetype: 'SATA'
        size: 100
        encrypted: False
        cmk_id: ''
      - volumetype: 'SAS'
        size: 120
    flavor: 's2.large.2'
    k8s_tags:
      testtag: 'value'
    keypair: 'sshkey-pub'
    labels:
      mein: 'label'
    max_pods: 16
    name: "{{ cce_node_name }}"
    network: '25d24fc8-d019-4a34-9fff-0a09fde6a123'
    os: 'CentOS 7.7'
    root_volume_size: 40
    root_volume_type: SATA
    tags:
      - key: 'key1'
        value: 'value1'
      - key: 'key2'
        value: 'value2'
    wait: true
    state: present

# Delete CCE cluster node
- opentelekomcloud.cloud.cce_cluster_node:
    cluster: "{{ cluster_name_or_id }}"
    name: "{{ cce_node_name }}"
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CceClusterNodeModule(OTCModule):
    argument_spec = dict(
        annotations=dict(required=False, type='dict'),
        availability_zone=dict(required=False),
        cluster=dict(required=True),
        count=dict(required=False, type='int', default=1),
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
        k8s_tags=dict(required=False, type='dict'),
        ssh_key=dict(required=False, no_log=False),
        labels=dict(required=False, type='dict'),
        lvm_config=dict(required=False),
        max_pods=dict(required=False, type='int'),
        name=dict(required=True),
        network=dict(required=False),
        node_image_id=dict(required=False),
        offload_node=dict(required=False, type='bool'),
        os=dict(required=False),
        postinstall_script=dict(required=False),
        preinstall_script=dict(required=False),
        root_volume_size=dict(required=False, type='int', default=40),
        root_volume_type=dict(
            required=False,
            choices=['SATA', 'SAS', 'SSD'],
            default='SATA'),
        state=dict(default='present', choices=['absent', 'present']),
        tags=dict(required=False, type='list', elements='dict'),
        timeout=dict(required=False, type='int', default=180),
        wait=dict(required=False, type='bool', default=True)
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present',
             ['availability_zone', 'cluster', 'flavor', 'ssh_key',
              'data_volumes', 'network']),
            ('state', 'absent', ['cluster', 'name']),
        ],
        supports_check_mode=True
    )

    otce_min__version = '0.12.1'

    def run(self):
        self.params['wait_timeout'] = self.params['timeout']
        cce_cluster = self.params['cluster']

        cluster = None
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
            if self.ansible.check_mode:
                self.exit(changed=True)
            if not cluster_node:
                self.params.pop('cluster')
                cluster_node = self.conn.create_cce_cluster_node(
                    cluster=cluster.id,
                    **self.params
                )
                changed = True
            else:
                # Modify CCE Cluster Node not available right now
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
                attrs = {}
                if self.ansible.check_mode:
                    self.exit(changed=True)
                if self.params['wait']:
                    attrs['wait'] = True
                if self.params['timeout']:
                    attrs['wait_timeout'] = self.params['timeout']
                changed = True
                self.conn.delete_cce_cluster_node(
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
