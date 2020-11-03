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
module: deh_server_info
short_description: Get info about ECSs on a Dedicated host
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Tino Schreiber (@tischrei)"
description:
  - Get info about ECSs on a Dedicated host
options:
  dedicated_host:
    description:
      - ID of a Dedicated Host
    type: str
    required: true
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
deh_servers:
    description: Dictionary of ECSs on a Dedicated host
    returned: changed
    type: list
    sample: [
      {
          "addresses": {
              "26ca2783-dc40-4e3a-95b1-5a0756441123": [
                  {
                      "OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:3d:b0:d3",
                      "OS-EXT-IPS:type": "fixed",
                      "addr": "192.168.0.16",
                      "version": 4
                  },
                  {
                      "OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:3d:b0:d3",
                      "OS-EXT-IPS:type": "floating",
                      "addr": "100.74.198.155",
                      "version": 4
                  }
              ]
          },
          "created_at": "2020-09-30T09:59:01Z",
          "flavor": {
              "disk": 0,
              "ephemeral": 0,
              "extra_specs": {
                  "cond:compute": "autorecovery",
                  "cond:operation:az": "az01(normal),az02(normal),az03(normal)",
                  "cond:operation:status": "abandon",
                  "ecs:generation": "s3",
                  "ecs:performancetype": "normal",
                  "ecs:virtualization_env_types": "CloudCompute",
                  "hw:cpu_cores": "1",
                  "hw:cpu_sockets": "1",
                  "hw:cpu_threads": "1",
                  "hw:numa_nodes": "1",
                  "quota:conn_limit_total": "1000000",
                  "quota:disk_max_num": "60",
                  "quota:max_pps": "50000",
                  "quota:max_rate": "500",
                  "quota:min_rate": "100",
                  "quota:physics_max_rate": "13500",
                  "quota:scsi_disk_max_num": "60",
                  "quota:vbd_disk_max_num": "24",
                  "quota:vif_max_num": "12",
                  "quota:vif_multiqueue_num": "1",
                  "resource_type": "IOoptimizedS2",
                  "sched:policy": "flat_balance"
              },
              "id": "s2.medium.1",
              "original_name": "s2.medium.1",
              "ram": 1024,
              "swap": 0,
              "vcpus": 1
          },
          "id": "a0c4d7d6-a2ae-4519-92d9-f0780e6f1123",
          "metadata": {
              "cascaded.instance_extrainfo": "pcibridge:1",
              "charging_mode": "0",
              "image_name": "Standard_Ubuntu_20.04_latest",
              "metering.cloudServiceType": "sys.service.type.ec2",
              "metering.image_id": "c8983e9e-1dda-479a-9a95-b41fe325a123",
              "metering.imagetype": "gold",
              "metering.resourcespeccode": "deh.linux",
              "metering.resourcetype": "1",
              "os_bit": "64",
              "os_type": "Linux",
              "vpc_id": "26ca2783-dc40-4e3a-95b1-5a0756441123"
          },
          "name": "my-ecs-on-deh",
          "status": "ACTIVE",
          "tenant_id": "16d53a84a13b49529d2e2c3646691123",
          "updated_at": "2020-09-30T09:59:15Z",
          "user_id": "18569c6d589c4be3a300b6401c74d123"
      }
    ]
'''

EXAMPLES = '''
# Query all ECSs on DeH host
- opentelekomcloud.cloud.deh_server_info:
    dedicated_host: 123456-host-id
  register: server
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DehServerInfoModule(OTCModule):
    argument_spec = dict(
        dedicated_host=dict(required=True)
    )

    def run(self):

        data = []
        query = {}

        if self.params['dedicated_host']:
            deh = self.conn.deh.find_host(
                name_or_id=self.params['dedicated_host'],
                ignore_missing=True)
            if deh:
                query['host'] = deh.id
            else:
                self.exit(
                    changed=False,
                    deh_hosts=[],
                    message=('No DEH host found with ID: %s' %
                             self.params['dedicated_host'])
                )

        for raw in self.conn.deh.servers(**query):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            deh_servers=data
        )


def main():
    module = DehServerInfoModule()
    module()


if __name__ == '__main__':
    main()
