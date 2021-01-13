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
module: cce_node_pool_info
short_description: Get CCE node pool info
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.5.0"
author: "Tino Schreiber (@tischrei)"
description:
  - Get CCE node pool info
options:
  cce_cluster:
    description:
      - CCE cluster name or id where the node pool is attached to
      - Mandatory
    type: str
    required: true
  name:
    description:
      - Name or ID of the CCE node pool to filter.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
cce_node_pools:
    description: Dictionary of CCE node pools
    returned: changed
    type: list
    sample: [
        {
            "api_version": "v3",
            "id": "8b98850a-4e72-11eb-8fea-0255ac101123",
            "kind": "NodePool",
            "metadata": null,
            "name": "test-nodepool-95461",
            "spec": {
                "autoscaling": {
                    "enable": false,
                    "max_node_count": 20,
                    "min_node_count": 1,
                    "priority": 50,
                    "scale_down_cooldown_time": 5
                },
                "initial_node_count": 0,
                "node_management": {
                    "ecs_group": "cce_nodes",
                },
                "node_pool_type": "vm",
                "node_template_spec": {
                    "availability_zone": "eu-de-02",
                    "billing_mode": 0,
                    "count": null,
                    "data_volumes": [
                        {
                            "extend_params": {
                                "use_type": "docker"
                            },
                            "metadata": {
                                "__system__cmkid": "1ed68cb7-b09b-423c-8d66-fdd",
                                "__system__encrypted": "1"
                            },
                            "size": 100,
                            "type": "SSD"
                        },
                        {
                            "extend_params": {
                                "use_type": "docker"
                            },
                            "metadata": null,
                            "size": 100,
                            "type": "SATA"
                        }
                    ],
                    "ecs_group": null,
                    "extend_params": {
                        "alpha.cce/NodeImageID": "123456",
                        "alpha.cce/postInstall": "bHMgLWwK",
                        "alpha.cce/preInstall": "bHMgLWw=",
                        "maxPods": 100
                    },
                    "flavor": "s2.large.2",
                    "floating_ip": {
                        "count": null,
                        "floating_ip_spec": {
                            "bandwidth": {}
                        },
                        "ids": null,
                    },
                    "k8s_tags": {
                        "cce.cloud.com/cce-nodepool": "my-tag",
                        "test-k8stag": "test"
                    },
                    "login": {
                        "id": null,
                        "location": null,
                        "name": null,
                        "ssh_key": "tischrei-pub"
                    },
                    "node_nic_spec": {
                        "primary_nic": {
                            "network_id": "25d24fc8-d019-4a34-9fff-0a09fde6"
                        }
                    },
                    "os": "EulerOS 2.5",
                    "root_volume": {
                        "size": 40,
                        "type": "SATA"
                    },
                    "tags": null,
                    "taints": [
                        {
                            "key": "test-taints",
                            "value": "test",
                            "effect": "NoSchedule"
                        }
                    ],
                    "userTags": [
                        {
                            "key": "test-resourcetag",
                            "value": "test"
                        }
                    ],
                }
            },
            "status": {
                "current_node": 0,
                "status": ""
            }
        }
    ]
'''

EXAMPLES = '''
# Query all CCE cluster node pools
- opentelekomcloud.cloud.cce_node_pool_info:
    cloud: "{{ test_cloud }}"
    cce_cluster: cce-cluster-name
  register: pool

# Query specific CCE node pool by name
- opentelekomcloud.cloud.cce_node_pool_info:
    cloud: "{{ test_cloud }}"
    cce_cluster: cce-cluster-name
    name: cce-node-pool-name
  register: pool
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CCENodePoolInfoModule(OTCModule):
    argument_spec = dict(
        cce_cluster=dict(required=True),
        name=dict(required=False),
    )

    otce_min__version = '0.13.0'

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
            pool = self.conn.cce.find_node_pool(
                cluster=cluster,
                pool=self.params['name'])
            if pool:
                pool = pool.to_dict()
                pool.pop('location')
                data.append(pool)
            else:
                self.exit(
                    changed=False,
                    cce_node_pools=[]
                )
        else:
            for raw in self.conn.cce.node_pools(cluster=cluster):
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit(
            changed=False,
            cce_node_pools=data
        )


def main():
    module = CCENodePoolInfoModule()
    module()


if __name__ == '__main__':
    main()
