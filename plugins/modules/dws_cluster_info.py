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
module: dws_cluster_info
short_description: Get info about DWS clusters.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.14.4"
author: "Attila Somogyi (@sattila1999)"
description:
  - Get DWS cluster info from the OTC.
options:
  name:
    description:
      - name or ID of the cluster to be queried.
    type: str
  limit:
    description:
      - Number of clusters to be queried.
      - The default value is 10, indicating that 10 clusters are queried at a time.
    type: int
requirements: ["openstacksdk", "otcextensions"]
"""

RETURN = """
cluster:
    description:
      - Info about specified DWS cluster.
    returned: On Success
    type: complex
    contains:
      availability_zone:
        description: AZ name.
        type: str
        sample: "eu-de-01"
      created_at:
        description: Cluster creation time. Format YYYY-MM-DDThh:mm:ssZ.
        type: str
        sample: "2018-02-10T14:28:14Z"
      endpoints:
        description: Private network connection information about the cluster.
        type: complex
        contains:
          connect_info:
            description: Private network connection information.
            type: str
            sample: "192.168.0.10:8000"
      enterprise_project_id:
        description: Enterprise project ID. The value 0 indicates the ID of the default enterprise project.
        type: str
        sample: "aca4e50a-266f-4786-827c-f8d6cc3fbada"
      flavor:
        description: The flavor of the cluster.
        type: str
        sample: "dws.m3.xlarge"
      id:
        description: Cluster ID.
        type: str
        sample: "7d85f602-a948-4a30-afd4-e84f47471c15"
      maintain_window:
        description: Cluster maintenance window.
        type: complex
        contains:
          day:
            description:
              - Maintenance time in each week in the unit of day.
              - Mon
              - Tue
              - Wed
              - Thu
              - Fri
              - Sat
              - Sun
            type: str
            sample: "Wed"
          start_time:
            description: Maintenance start time in HH:mm format. The time zone is GMT+0.
            type: str
            sample: "22:00"
          end_time:
            description: Maintenance end time in HH:mm format. The time zone is GMT+0.
            type: str
            sample: "02:00"
      name:
        description: Cluster name.
        type: str
        sample: "dws-1"
      network_id:
        description: Subnet ID.
        type: str
        sample: "374eca02-cfc4-4de7-8ab5-dbebf7d9a720"
      nodes:
        description: Cluster Instance.
        type: complex
        contains:
          id:
            description: Cluster instance ID.
            type: str
            sample: "acaf62a4-41b3-4106-bf6b-2f669d88291e"
          name:
            description: Cluster instance name.
            type: str
            sample: "dwh-1-dws-cn-cn-1-1"
          status:
            description: Cluster instance status.
            type: str
            sample: "200"
      num_nodes:
        description: Number of cluster instances.
        type: int
        sample: 3
      num_recent_events:
        description: Number of events.
        type: int
        sample: 6
      parameter_group:
        description: Parameter group details.
        type: complex
        contains:
          id:
            description: Parameter group ID.
            type: str
            sample: "157e9cc4-64a8-11e8-adc0-fa7ae01bbebc"
          name:
            description: Parameter group name.
            type: str
            sample: "Default-Parameter-Group-dws"
          status:
            description:
              - Cluster parameter status.
              - In-Sync
              - Applying
              - Pending-Reboot
              - Sync-Failure
            type: str
            sample: "In-Sync"
      port:
        description: Service port of a cluster. The value ranges from 8000 to 30000. The default value is 8000.
        type: int
        sample: 8000
      private_ip:
        description: List of private network IP addresses.
        type: list
        sample: ["192.168.0.12","192.168.0.66"]
      public_endpoints:
        description: Public network connection information about the cluster. Not used by default.
        type: complex
        contains:
          public_connect_info:
            description: Public network connection information.
            type: str
            sample: "10.0.0.8:8000"
      public_ip:
        description: Public IP address. If the parameter is not specified, public connection is not used by default.
        type: complex
        contains:
          public_bind_type:
            description:
              - Binding type of an EIP.
              - auto_assign
              - not_use
              - bind_existing
            type: str
            sample: "auto_assign"
          eip_id:
            description: EIP ID
            type: str
            sample: "85b20d7e-9etypeb2a-98f3-3c8843ea3574"
      resize_info:
        description: Cluster scale-out details.
        type: complex
        contains:
          target_node_num:
            description: Number of nodes after the scale-out.
            type: int
            sample: 6
          origin_node_num:
            description: Number of nodes before the scale-out.
            type: int
            sample: 3
          resize_status:
            description:
              - Scale-out status.
              - GROWING
              - RESIZE_FAILURE
            type: str
            sample: "GROWING"
          start_time:
            description: Scale-out start time. Format YYYY-MM-DDThh:mm:ss.
            type: str
            sample: "2018-02-14T14:28:14Z"
      router_id:
        description: VPC ID.
        type: str
        sample: "85b20d7e-9eb7-4b2a-98f3-3c8843ea3574"
      security_group_id:
        description: Security group ID.
        type: str
        sample: "dc3ec145-9029-4b39-b5a3-ace5a01f772b"
      status:
        description:
          - Cluster status.
          - CREATING
          - AVAILABLE
          - UNAVAILABLE
          - CREATION FAILED
        type: str
        sample: "AVAILABLE"
      sub_status:
        description:
          - Sub-status of clusters in the AVAILABLE state.
          - NORMAL
          - READONLY
          - REDISTRIBUTING
          - REDISTRIBUTION-FAILURE
          - UNBALANCED
          - UNBALANCED | READONLY
          - DEGRADED
          - DEGRADED | READONLY
          - DEGRADED | UNBALANCED
          - UNBALANCED | REDISTRIBUTING
          - UNBALANCED | REDISTRIBUTION-FAILURE
          - READONLY | REDISTRIBUTION-FAILURE
          - UNBALANCED | READONLY | REDISTRIBUTION-FAILURE
          - DEGRADED | REDISTRIBUTION-FAILURE
          - DEGRADED | UNBALANCED | REDISTRIBUTION-FAILURE
          - DEGRADED | UNBALANCED | READONLY | REDISTRIBUTION-FAILURE
          - DEGRADED | UNBALANCED | READONLY
        type: str
        sample: "READONLY"
      tags:
        description: Labels in a cluster.
        type: complex
        contains:
          key:
            description:
              - Key.
              - Can contain a maximum of 36 Unicode characters, which cannot be null.
              - The first and last characters cannot be spaces.
              - Only letters, digits, hyphens (-), and underscores (_) are allowed.
            type: str
            sample: "key1"
          value:
            description:
              - Value.
              - Can contain a maximum of 43 Unicode characters, which can be null.
              - The first and last characters cannot be spaces.
              - Only letters, digits, hyphens (-), and underscores (_) are allowed.
            type: str
            sample: "value1"
      task_status:
        description:
          - Cluster management task.
          - RESTORING
          - SNAPSHOTTING
          - GROWING
          - REBOOTING
          - SETTING_CONFIGURATION
          - CONFIGURING_EXT_DATASOURCE
          - DELETING_EXT_DATASOURCE
          - REBOOT_FAILURE
          - RESIZE_FAILURE
        type: str
        sample: "SNAPSHOTTING"
      updated_at:
        description: Last modification time of a cluster. Format YYYY-MM-DDThh:mm:ssZ.
        type: str
        sample: "2018-02-10T14:28:14Z"
      user_name:
        description: Username of the administrator.
        type: str
        sample: "dbadmin"
      version:
        description: Data warehouse version.
        type: str
        sample: "1.2.0"
"""

EXAMPLES = """
# Get info about clusters
- opentelekomcloud.cloud.dws_cluster_info:
    name: "dws-ea59"
    limit: 5
  register: result
"""

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import (
    OTCModule,
)


class DWSClusterInfoModule(OTCModule):
    argument_spec = dict(name=dict(), limit=dict(type="int"))
    module_kwargs = dict(supports_check_mode=True)

    otce_min_version = "0.24.1"

    def run(self):
        name = self.params["name"]
        if name:
            dws_clusters = self.conn.dws.find_cluster(name)
        else:
            kwargs = {
                k: self.params[k] for k in ["limit"] if self.params[k] is not None
            }

            raw = self.conn.dws.clusters(**kwargs)
            dws_clusters = [c.to_dict(computed=False) for c in raw]

        self.exit_json(changed=False, dws_clusters=dws_clusters)


def main():
    module = DWSClusterInfoModule()
    module()


if __name__ == "__main__":
    main()
