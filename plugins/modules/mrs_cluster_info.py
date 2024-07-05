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


DOCUMENTATION = """
module: mrs_cluster_info
short_description: Get info about MRS clusters.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.14.4"
author: "Attila Somogyi (@sattila1999)"
description:
  - Get MRS cluster info from the OTC.
options:
  name:
    description:
      - name or ID of the cluster to be queried.
    type: str
  limit:
    description:
      - Number of clusters to be queried.
    type: int
  tags:
    description:
      - Search for a cluster by its tags.
    type: list
    elements: str
  status:
    description:
      - Cluster status, where values can be the following.
      - starting
      - running
      - terminated
      - failed
      - abnormal
      - terminating
      - frozen
      - scaling-out
      - scaling-in
    type: str
requirements: ["openstacksdk", "otcextensions"]
"""

RETURN = """
cluster:
    description:
      - Info about specified MRS cluster.
    returned: On Success
    type: complex
    contains:
      az:
        description: Az name.
        type: str
        sample: "eu-de-01"
      az_id:
        description: Az ID.
        type: str
        sample: "eu-de-01"
      billing_type:
        description: Cluster billing mode.
        type: str
        sample: "Metered"
      bootstrap_scripts:
        description: Bootstrap action script information.
        type: complex
        contains:
          active_master:
            description: Whether the bootstrap action script runs only on active Master nodes.
            type: bool
            sample: false
          before_component_start:
            description:
              - Time when the bootstrap action script is executed.
              - Currently two options are available.
            type: bool
            sample: true
          fail_action:
            description:
              - continue
              - errorout
            type: str
            sample: "errorout"
          name:
            description: Name of a bootstrap action script. It must be unique in a cluster.
            type: str
            sample: "bootstrap-script-1"
          nodes:
            description: Type of a node where the bootstrap action script is executed.
            type: complex
            sample: ["Master"]
          start_time:
            description: Execution time of one boot operation script.
            type: str
            sample: "1711530046"
          state:
            description: Running state of one bootstrap action script.
            type: str
            sample: "SUCCESS"
          uri:
            description: Path of the shell script.
            type: str
            sample: "s3a://bootstrap/presto/presto-install.sh"
      charging_start_time:
        description: Start time of billing.
        type: str
        sample: "1711530046"
      cluster_id:
        description: Cluster id.
        type: str
        sample: "c4ab345f-78c2-47hk-9864-e2f74f402f49"
      cluster_type:
        description: Cluster type.
        type: str
        sample: "0"
      cluster_version:
        description: Cluster version.
        type: str
        sample: "MRS 3.2.0-LTS.2"
      component_list:
        description: Component list.
        type: complex
        contains:
          componentDesc:
            description: Component description.
            type: str
            sample: "A framework that allows for the distributed processing of large data sets across clusters."
          componentId:
            description: Component ID.
            type: str
            sample: "MRS 3.2.0-LTS.2_001"
          componentName:
            description: Component name.
            type: str
            sample: "Hadoop"
          componentVersion:
            description: Component version.
            type: str
            sample: "3.3.1"
      core_data_volume_count:
        description:
          - Number of data disks of the Core node.
          - Value ranges from 1 to 10.
        type: int
        sample: 1
      core_data_volume_size:
        description:
          - Data disk storage space of the Core node.
          - To increase data storage capacity, you can add disks at the same time when creating a cluster.
          - Value ranges from 100 GB to 32,000 GB.
        type: int
        sample: 600
      core_data_volume_type:
        description:
          - Data disk storage type of the Core node.
          - Currently, SATA, SAS and SSD are supported.
        type: str
        sample: "SATA"
      core_node_product_id:
        description: Product ID of a Core node.
        type: str
        sample: "98c1fgc0897249653b1ec456d06e1234"
      core_node_size:
        description: Instance specifications of a Core node.
        type: str
        sample: "c3.xlarge.2.linux.mrs"
      core_node_spec_id:
        description: Specification ID of a Core node.
        type: str
        sample: "c3.xlarge.2"
      core_num:
        description: Number of Core nodes deployed in a cluster.
        type: str
        sample: "3"
      created_at:
        description: Cluster creation time, which is a 10-bit timestamp.
        type: str
        sample: "1711529080"
      deployment_id:
        description: Cluster deployment ID.
        type: str
        sample: "b3ab337a-19z2-47cd-9864-e2f38f402f57"
      error_info:
        description: Error message.
        type: str
        sample: null
      external_alternate_ip:
        description: Backup external IP address.
        type: str
        sample: "100.74.244.67"
      external_ip:
        description: External IP address.
        type: str
        sample: "100.73.125.240"
      fee:
        description: Cluster creation fee, which is automatically calculated.
        type: str
        sample: "0.0"
      hadoop_version:
        description: Hadoop version.
        type: str
        sample: "3.3.1"
      instance_id:
        description: Instance ID.
        type: str
        sample: "b3ab442a-98c2-47ab-9887-e3c36f402f32"
      internal_ip:
        description: Internal IP address.
        type: str
        sample: "192.168.0.253"
      log_collection:
        description: Whether to collect logs when cluster installation fails.
        type: int
        sample: 0
      master_data_volume_count:
        description:
          - Number of data disks of the Master node.
          - The value can be set to 1 only.
        type: int
        sample: 1
      master_data_volume_size:
        description:
          - Data disk storage space of the Master node.
          - To increase data storage capacity, you can add disks at the same time when creating a cluster.
          - Value ranges from 100 GB to 32,000 GB.
        type: int
        sample: 600
      master_data_volume_type:
        description:
          - Data disk storage type of the Master node.
          - Currently, SATA, SAS and SSD are supported.
        type: str
        sample: "SATA"
      master_ip:
        description: IP address of a Master node.
        type: str
        sample: "192.168.0.245"
      master_node_product_id:
        description: Product ID of a Master node.
        type: str
        sample: "98c1fgc0897249653b1ec456d06e1234"
      master_node_size:
        description: Instance specifications of a Master node.
        type: str
        sample: "c4.4xlarge.4.linux.mrs"
      master_node_spec_id:
        description: Specification ID of a Master node.
        type: str
        sample: "c4.4xlarge.4"
      master_num:
        description: Number of Master nodes deployed in a cluster.
        type: str
        sample: "2"
      name:
        description: Cluster name.
        type: str
        sample: "mrs-1"
      node_groups:
        description: List of Master, Core and Task nodes.
        type: complex
        contains:
          DataVolumeCount:
            description: Number of data disks of a node.
            type: int
            sample: 1
          DataVolumeProductId:
            description: Data disk product ID of a node.
            type: str
            sample: "98c1fgc0897249653b1ec456d06e1234"
          DataVolumeResourceSpecCode:
            description: Data disk product specifications of a node.
            type: str
          DataVolumeResourceType:
            description: Data disk product type of a node.
            type: str
          DataVolumeSize:
            description: Data disk storage space of a node.
            type: int
            sample: 600
          DataVolumeType:
            description:
              - Data disk storage type of a node.
              - Currently, SATA, SAS and SSD are supported.
            type: str
            sample: "SATA"
          GroupName:
            description: Node group name.
            type: str
            sample: "core_node_analysis_group"
          NodeNum:
            description: Number of nodes. The value ranges from 0 to 500.
            type: int
            sample: 3
          NodeProductId:
            description: Instance product ID of a node.
            type: str
            sample: "98c1fgc0897249653b1ec456d06e1234"
          NodeSize:
            description: Instance specifications of a node.
            type: str
            sample: "c3.xlarge.2.linux.mrs"
          NodeSpecId:
            description: Instance specification ID of a node.
            type: str
            sample: "c3.xlarge.2"
          RootVolumeProductId:
            description: System disk product ID of a node.
            type: str
            sample: "98c1fgc0897249653b1ec456d06e1234"
          RootVolumeResourceSpecCode:
            description: System disk product specifications of a node.
            type: str
          RootVolumeResourceType:
            description: System disk product type of a node.
            type: str
          RootVolumeSize:
            description:
              - System disk size of a node.
              - This parameter is not configurable and its default value is 40 GB.
            type: int
            sample: 480
          RootVolumeType:
            description: System disk type of a node.
            type: str
            sample: "SATA"
          VmProductId:
            description: VM product ID of a node.
            type: str
            sample: "98c1fgc0897249653b1ec456d06e1234"
          VmSpecCode:
            description: VM specifications of a node.
            type: str
            sample: "c3.xlarge.2.linux"
      order_id:
        description: Cluster creation order ID.
        type: str
        sample: "MRS1733524072957vapz"
      project_id:
        description: Project ID.
        type: str
        sample: "cf183d0142e94747bf57acf742e7fa87"
      region:
        description: Cluster work region.
        type: str
        sample: "eu-de"
      remark:
        description: Cluster remarks.
        type: str
      safe_mode:
        description: Running mode of an MRS cluster.
        type: int
        sample: 1
      scale:
        description:
          - Node change status.
          - If this parameter is left blank, the cluster nodes are not changed.
          - scaling-out
          - scaling-in
          - scaling-error
          - scaling-up
          - scaling_up_first
          - scaled_up_first
          - scaled-up-success
        type: str
      security_group_id:
        description: Security group ID.
        type: str
        sample: "2d7178d5-0bee-43e8-c212-fbcfe4c1667f"
      stage_desc:
        description: Cluster operation progress description.
        type: str
        sample: "Installing MRS Manager"
      status:
        description:
          - Cluster status.
          - starting
          - running
          - terminated
          - failed
          - abnormal
          - terminating
          - frozen
          - scaling-out
          - scaling-in
        type: str
        sample: "running"
      subnet_id:
        description: Subnet ID.
        type: str
        sample: "9a31d412-f482-42cd-9gol-98h59f9a3a50"
      subnet_name:
        description: Subnet name.
        type: str
        sample: "subnet-1"
      tags:
        description: Tag information.
        type: list
        sample: ["key1=value1"]
      task_node_groups:
        description: List of Task nodes.
        type: list
        sample: [{
                    "AutoScalingPolicy": null,
                    "BillingType": 12,
                    "DataVolumeCount": 1,
                    "DataVolumeProductId": null,
                    "DataVolumeResourceSpecCode": null,
                    "DataVolumeResourceType": null,
                    "DataVolumeSize": 600,
                    "DataVolumeType": "SATA",
                    "GroupName": "master_node_default_group",
                    "NeedLvm": false,
                    "NodeNum": 2,
                    "NodeProductId": null,
                    "NodeSize": "c4.4xlarge.4.linux.mrs",
                    "NodeSpecId": "c4.4xlarge.4",
                    "RootVolumeProductId": null,
                    "RootVolumeResourceSpecCode": null,
                    "RootVolumeResourceType": null,
                    "RootVolumeSize": 480,
                    "RootVolumeType": "SATA",
                    "SeqId": 66778,
                    "VmProductId": null,
                    "VmSpecCode": "c4.4xlarge.4.linux",
                    "assignedRoles": [
                        "SlapdServer:1,2",
                        "KerberosServer:1,2",
                        "KerberosAdmin:1,2",
                        "quorumpeer:1,2",
                        "NameNode:1,2",
                        "Zkfc:1,2",
                        "JournalNode:1,2",
                        "ResourceManager:1,2",
                        "JobHistoryServer:2",
                        "DBServer:1,2",
                        "HttpFS:1,2",
                        "MetaStore:1,2",
                        "WebHCat:2",
                        "HiveServer:1,2",
                        "JDBCServer2x:1,2",
                        "JobHistory2x:1,2",
                        "SparkResource2x:1,2",
                        "TezUI:1,2",
                        "TimelineServer:2",
                        "RangerAdmin:1,2",
                        "UserSync:2",
                        "TagSync:2",
                        "KerberosClient",
                        "SlapdClient",
                        "meta",
                        "FlinkResource:1,2",
                        "FlinkServer:1,2"
                    ],
                    "az_placement_expression": null,
                    "clusterId": "b3ab337a-98c2-47ab-9864-e2f36f402f49",
                    "cpuType": "X86",
                    "currency": null,
                    "dccNodeProductId": null,
                    "dccNodeSize": null,
                    "disabled": false,
                    "hypervisorType": null,
                    "isSpotInstance": false,
                    "nodeType": null,
                    "serverGroupId": "25dcf361-c048-43fa-9267-3788779e7d9c",
                    "spotPrice": null,
                    "volumeDssClusterId": null,
                    "volumeDssClusterType": null
                }
            ]
      total_num:
        description: Total number of nodes deployed in a cluster.
        type: str
        sample: "5"
      updated_at:
        description: Cluster update time, which is a 10-bit timestamp.
        type: str
        sample: "1719561546"
      vnc:
        description: URI for remotely logging in to an ECS.
        type: str
        sample: "v2/gz183d0345e96897bf57acf742e7cz49/servers/44330fbb-498c-477f-8c5b-e11d62fdbecf/action"
      volume_size:
        description: Disk storage space.
        type: int
        sample: 0
      vpc:
        description: VPC name.
        type: str
        sample: "vpc-1"
"""

EXAMPLES = """
# Get info about clusters
- opentelekomcloud.cloud.mrs_cluster_info:
    name: "mrs-ea59"
  register: result

# Get info about clusters using query filters
- opentelekomcloud.cloud.mrs_cluster_info:
    status: "running"
    limit: 2
    tags:
      - key1=value1
      - key2=value2
  register: result
"""

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import (
    OTCModule,
)


def _normalize_tags(tags):
    result = ''
    for tag in tags:
        tag_parts = tag.split('=')
        if len(tag_parts) == 2 and tag_parts[1]:
            result += f'{tag_parts[0]}*{tag_parts[1]},'
        else:
            result += f'{tag_parts[0]},'
    return result[:-1]


class MRSClusterInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(),
        status=dict(type='str'),
        tags=dict(required=False, type='list', elements='str'),
        limit=dict(type='int')
    )
    module_kwargs = dict(supports_check_mode=True)

    otce_min_version = '0.24.1'

    def run(self):
        data = []
        if self.params['name']:
            raw = self.conn.mrs.find_cluster(
                name_or_id=self.params['name'], ignore_missing=True
            )
            if raw:
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)
        else:
            if self.params['tags']:
                self.params['tags'] = _normalize_tags(self.params['tags'])
            kwargs = {k: self.params[k]
                      for k in ['tags', 'status', 'limit']
                      if self.params[k] is not None}

            for raw in self.conn.mrs.clusters(**kwargs):
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit_json(changed=False, mrs_clusters=data)


def main():
    module = MRSClusterInfoModule()
    module()


if __name__ == '__main__':
    main()
