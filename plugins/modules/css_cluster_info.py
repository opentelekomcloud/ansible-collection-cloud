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
module: cs_cluster_info
short_description: Get info about CSS clusters.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.1"
author: "Yustina Kvrivishvili (@YustinaKvr)"
description:
  - Get CSS cluster info from the OTC.
options:
  id:
    description:
      - ID of the cluster to be queried.
    type: str
  start:
    description:
      - Start value of the query. The default value is 1, indicating that the query starts from the\
        first cluster.
    type: int
  limit:
    description:
      - Number of clusters to be queried. The default value is 10, indicating that 10 clusters are\
        queried at a time.
    type: int
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
cluster:
    description:
        - Info about specified CSS cluster.
    returned: On Success
    type: complex
    contains:
        actions:
          description: Indicates the operation that is executed on the cluster.
          type: list
          sample: "REBOOTING"
        cmk_id:
          desciption: Key ID used for disk encryption.
          type: str
          sample: "null"
        created_at:
          desription: Time when a cluster is created. The format is ISO8601: CCYY-MM-DDThh:mm:ss.
          type: str
          sample: "2021-10-05T15:55:06"
        datastore:
          description: Type of the data search engine.
          type: complex
          contains:
            type:
              description: Supported type: elasticsearch
              type: str
              sample: "elasticsearch"
            version: Engine version number. The current engine version is 6.2.3, 7.1.1, or 7.6.2.
              description:
              type: str
              sample: "7.6.2"
        disk_encryption:
          description: Whether disks are encrypted.
          type: str
          sample: "null"
        endpoint:
          description: Indicates the IP address and port number of the user used to access the VPC.
          type: str
          sample: "10.0.0.169:9200,10.0.0.191:9200,10.0.0.112:9200"
        error:
          description:
              - Error codes:
              - CSS.6000: indicates that a cluster fails to be created.
              - CSS.6001: indicates that capacity expansion of a cluster fails.
              - CSS.6002: indicates that a cluster fails to be restarted.
              - CSS.6004: indicates that a node fails to be created in a cluster.
              - CSS.6005: indicates that the service fails to be initialized.
          type: str
          sample: "null"
        id:
          description: Cluster ID.
          type: str
          sample: "a4edb35e-bded-4a44-ba9c-6b5d1f585f3d"
        instance:
          description:
          type: list
          sample:
        instance_count:
          description:
          type: list
          sample:
        is_disk_encrypted:
          description: Whether disks are encrypted.
          type: bool
          sample: false
        is_https_enabled:
          description: Communication encryption status.
          type: bool
          sample: false
        name:
          description: Cluster name.
          type: str
          sample: "css-test"
        nodes:
          description:
          type: complex
          contains:
            azCode:
              description: AZ to which a node belongs.
              type: str
              sample: "eu-de-01"
            id:
              description: Node ID.
              type: str
              sample: "7575d430-c918-4a80-9dba-8baa9ab49862"
            name:
              description: Node name.
              type: str
              sample: "css-test-iustina-ess-esn-3-1"
            specCode:
              description: Node specifications.
              type: str
              sample: "css.medium.8"
            status:
              description:
                  - Node status.
                  - 100: The operation, such as node creation, is in progress.
                  - 200: The instance is available.
                  - 303: The instance is unavailable.
              type: str
              sample: "200"
            type:
              description:
              type: list
              sample: "ess"
        progress:
          description:
          type: str
          sample: "[
            "CREATING": "2%"
            ]"
        router_id:
          description: Indicates the VPC ID.
          type: str
          sample: "7ea09482-793a-4aed-b4ce-447113d10d69"
        security_group_id:
          description: Security group ID.
          type: str
          sample: "120888d9-65be-4899-b07d-aa151c2895d4"
        status:
#What exact value?
          description:
              - Return value.
          type: str
          sample: "200"
        subnet_id:
          description: Subnet ID.
          type: str
          sample: "8d9bd4e8-3c88-4991-8df3-d5e3cfd9a835"
        updated_at:
          description:
              - Last modification time of a cluster.
              - The format is ISO8601: CCYY-MM-DDThh:mm:ss.
          type: str
          sample: "2021-10-13T10:35:56"
'''

EXAMPLES = '''
# Get info about clusters
- opentelekomcloud.cloud.css_cluster_info:
  register: result
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CSSClusterInfoModule(OTCModule):

    argument_spec = dict(
        id=dict(required=False),
        start=dict(type=int, required=False),
        limit=dict(type=int, required=False)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        data = []
        query = {}
        clusters = None

        if self.params['id']:
            query['id'] = self.params['id']
        if self.params['start']:
            query['start'] = self.params['id']
        if self.params['limit']:
            query['limit'] = self.params['limit']

        for raw in self.conn.css.clusters(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            clusters=data
        )


def main():
    module = CSSClusterInfoModule()
    module()


if __name__ == '__main__':
    main()
