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
module: cce_cluster_node_info
short_description: Get CCE node info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.4.0"
author: "Tino Schreiber (@tischrei)"
description:
  - Get CCE node info
options:
  cce_cluster:
    description:
      - CCE cluster name or id where the cluster nodes are located in
      - Mandatory
    type: str
    required: true
  name:
    description:
      - Name or ID of the CCE cluster node to filter.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
cce_cluster_nodes:
    description: Dictionary of CCE cluster nodes
    returned: changed
    type: list
    sample: [
        {
            "api_version": "v3",
            "id": "6f620aad-24ec-11eb-a970-0255ac101123",
            "kind": "Node",
            "metadata": {
                "annotations": {
                    "kubernetes.io/node-pool.id": "eu-de-01#s2.large.2#EulerOS 2.5"
                },
                "created_at": null,
                "id": "6f620aad-24ec-11eb-a970-0255ac101123",
                "labels": null,
                "location": null,
                "name": "cce-cluster-node-name",
                "updated_at": null
            },
            "name": "cce-cluster-node-name",
            "spec": {
                "availability_zone": "eu-de-01",
                "billing_mode": 0,
                "count": null,
                "data_volumes": [
                    {
                        "id": null,
                        "location": null,
                        "name": null,
                        "size": 100,
                        "type": "SATA"
                    }
                ],
                "flavor": "s2.large.2",
                "floating_ip": {
                    "count": null,
                    "floating_ip": {
                        "bandwidth": {}
                    },
                    "id": null,
                    "ids": null,
                    "location": null,
                    "name": null
                },
                "id": null,
                "location": null,
                "login": {
                    "sshKey": "ssh-key",
                    "userPassword": {}
                },
                "name": null,
                "os": "EulerOS 2.5",
                "root_volume": {
                    "id": null,
                    "location": null,
                    "name": null,
                    "size": 40,
                    "type": "SATA"
                }
            },
            "status": {
                "floating_ip": null,
                "id": null,
                "instance_id": "8371c8c7-a5cc-4b9b-aeb5-c11a9d05c123",
                "job_id": null,
                "location": null,
                "name": null,
                "private_ip": "192.168.0.123",
                "status": "Active"
            }
        }
    ]
'''

EXAMPLES = '''
# Query all CCE cluster nodes
- opentelekomcloud.cloud.cce_cluster_node_info:
    cloud: "{{ test_cloud }}"
    cce_cluster: cce-cluster-name
  register: node

# Query specific CCE cluster node by name
- opentelekomcloud.cloud.cce_cluster_node_info:
    cloud: "{{ test_cloud }}"
    cce_cluster: cce-cluster-name
    name: cce-node-name
  register: node
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CCEClusterNodeInfoModule(OTCModule):
    argument_spec = dict(
        cce_cluster=dict(required=True),
        name=dict(required=False),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    otce_min__version = '0.12.1'

    def run(self):

        data = []
        query = {}

        cluster = self.conn.cce.find_cluster(
            self.params['cce_cluster'],
            ignore_missing=True)
        if not cluster:
            self.fail_json(
                changed=False,
                message=('No cluster found with name or id: %s' %
                         self.params['cce_cluster'])
            )
        else:
            query['cluster'] = self.params['cce_cluster']
        if self.params['name']:
            node = self.conn.cce.find_cluster_node(
                cluster=cluster,
                node=self.params['name'])
            if node:
                node = node.to_dict()
                node.pop('location')
                data.append(node)
            else:
                self.exit(
                    changed=False,
                    cce_cluster_nodes=[]
                )
        else:
            for raw in self.conn.cce.cluster_nodes(cluster=cluster):
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit(
            changed=False,
            cce_cluster_nodes=data
        )


def main():
    module = CCEClusterNodeInfoModule()
    module()


if __name__ == '__main__':
    main()
