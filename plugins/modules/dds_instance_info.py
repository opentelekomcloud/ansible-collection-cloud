#!/usr/bin/python
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions,
# limitations under the License.

DOCUMENTATION = '''
module: dds_instance_info
short_description: Obtain information about a specified DB instance.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.9.0"
author: "Yustina Kvrivishvili (@YustinaKvr)"
description:
  - Get info about instances.
options:
  instance:
    description:
      - Specifies the DB instance ID or name.
    type: str
  mode:
    description:
      - Specifies the instance type.
    choices: [sharding, replicaset]
    type: str
  datastore_type:
    description:
      - Specifies the database type. The value is DDS-Community.
    type: str
    default: 'DDS-Community'
  vpc_id:
    description:
      - Specifies the VPC ID.
    type: str
  subnet_id:
    description:
      - Specifies the network ID of the subnet.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
instance:
    description:
        - Info about a specified DB instance.
        - If ID or name is not specified, info about all instances inside one project.
    returned: On Success
    type: complex
    contains:
        actions:
          description: Indicates the operation that is executed on the DB instance.
          type: list
          sample: "CREATE"
        availability_zone:
          description: Indicates the AZ.
          type: str
          sample: null
        backup_strategy:
          description: Indicates the backup policy.
          type: complex
          contains:
            keep_days:
              description: Indicates the number of days to retain the generated backup files.
              type: int
              sample: 7
            start_time:
              description:
                  - Indicates the backup time window.
                  - Automated backups will be triggered during the backup time window.
                  - The current time is the UTC time.
              type: str
              sample: "22:00-23:00"
        created:
          description: Indicates the DB instance creation time.
          type: str
          sample: "2021-08-12T13:58:08"
        datastore:
          description: Specifies the domain name associated with the server certificate.
          type: complex
          contains:
            storage_engine:
              description: Storage engine.
              type: str
              sample: null
            type:
              description: Indicates the DB engine.
              type: str
              sample: "DDS-Community"
            version:
              description: Indicates the database version.
              type: str
              sample: "3.4"
        datastore_type:
          description: Specifies the database type.
          type: str
          sample: null
        disk_encryption_id:
          description: Indicates the disk encryption key ID.
          type: str
          sample: null
        engine:
          description: Indicates the storage engine.
          type: str
          sample: "wiredTiger"
        flavor:
          description: Indicates the DB instance flavor.
          type: str
          sample: null
        groups:
          description: Indicates group information.
          type: complex
          contains:
            id:
              description:
                  - Indicates the group ID.
                  - This parameter is valid only when the node type is shard or config.
              type: str
              sample: null
            name:
              description: Indicates the group name.
              type: str
              sample: null
            nodes:
              description: Indicates the AZ.
              type: complex
              contains:
                availability_zone:
                  description: Indicates the AZ.
                  type: str
                  sample: null
                id:
                  description: Indicates the node ID.
                  type: str
                  sample: "254c36d7e72a40d0b1667983a8a2fc09no02"
                name:
                  description: Indicates the node name.
                  type: str
                  sample: "test_dds_replica_node_3"
                private_ip:
                  description:
                      - Indicates the private IP address of a node.
                      - Valid only for mongos and replica set instances.
                      - The value exists only after ECSs are created successfully.
                  type: str
                  sample: "192.168.115.80"
                public_ip:
                  description:
                      - Indicates the EIP that has been bound.
                      - Valid only for mongos nodes of cluster instances.
                  type: str
                  sample: ""
                role:
                  description: Indicates the node role.
                  type: str
                  sample: "Primary"
                spec_code:
                  description: Indicates the resource specifications code.
                  type: str
                  sample: "dds.mongodb.s2.medium.4.repset"
                status:
                  description: Indicates the node status.
                  type: str
                  sample: "normal"
            status:
              description:
                  - Indicates the group status.
                  - This parameter is valid only when the node type is shard or config.
              type: str
              sample: null
            type:
              description: Indicates the node type.
              type: str
              sample: null
            volume:
              description: Indicates the volume information.
              type: complex
              contains:
                size:
                  description: Indicates the disk size. Unit GB
                  type: str
                  sample: "10"
                used:
                  description: Indicates the disk usage. Unit GB
                  type: str
                  sample: "0.333129882812"
        id:
          description: Indicates the DB instance ID.
          type: str
          sample: "7ddf3c02aea54610bb6ba324e653484din02"
        maintenance_window:
          description: Indicates the maintenance time window.
          type: str
          sample: "02:00-06:00"
        mode:
          description: Indicates the instance type, which is the same as the request parameter.
          type: str
          sample: "CREATE"
        name:
          description: Indicates the operation that is executed on the DB instance.
          type: str
          sample: "ReplicaSet"
        pay_mode:
          description: Indicates the billing mode. 0 indicates the pay-per-use billing mode.
          type: str
          sample: "0"
        port:
          description: Indicates the database port number. The port range is 2100 to 9500.
          type: int
          sample: "8635"
        region:
          description: Indicates the region where the DB instance is deployed.
          type: str
          sample: "eu-de"
        security_group_id:
          description: Indicates the security group ID.
          type: str
          sample: "120888d9-65be-4899-b07d-aa151c2895d4"
        ssl:
          description: Indicates that SSL is enabled or not.
          type: bool
          sample: 0
        status:
          description: Indicates the DB instance status.
          type: str
          sample: "normal"
        subnet_id:
          description: Indicates the subnet ID.
          type: str
          sample: "c2fdde80-9a24-4a84-99fe-d07e942274b1"
        time_zone:
          description: Indicates the time zone.
          type: str
          sample: ""
        updated:
          description: Indicates the time when a DB instance is updated.
          type: str
          sample: "2021-08-12T13:58:03"
        vpc_id:
          description: Indicates the VPC ID.
          type: str
          sample: "199dcd34-9c6f-49d5-b12a-5fa96351acf1"
'''

EXAMPLES = '''
# Get info about instances
- opentelekomcloud.cloud.dds_instance_info:
  register: result
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DDSInstanceInfo(OTCModule):
    argument_spec = dict(
        instance=dict(),
        mode=dict(choices=['sharding', 'replicaset']),
        datastore_type=dict(default='DDS-Community'),
        vpc_id=dict(),
        subnet_id=dict()
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        data = []
        query = {}

        instance = self.params['instance']
        mode = self.params['mode']
        datastore_type = self.params['datastore_type']
        vpc_id = self.params['vpc_id']
        subnet_id = self.params['subnet_id']

        if instance:
            db_instance = self.conn.dds.find_instance(name_or_id=instance)
            if db_instance:
                query['id'] = db_instance.id
                query['name'] = db_instance.name
        if mode:
            query['mode'] = mode

        if datastore_type:
            query['datastore_type'] = datastore_type

        if vpc_id:
            vpc = self.conn.network.find_router(name_or_id=vpc_id)
            if vpc:
                query['vpc_id'] = vpc.id

        if subnet_id:
            subnet = self.conn.network.find_subnet(name_or_id=subnet_id)
            if subnet:
                query['subnet_id'] = subnet.id

        for raw in self.conn.dds.instances(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            instance=data
        )


def main():
    module = DDSInstanceInfo()
    module()


if __name__ == '__main__':
    main()
