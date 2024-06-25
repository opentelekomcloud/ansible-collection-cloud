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
---
module: dws_cluster
short_description: Manage dws clusters
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: 0.14.4
author: Vineet Pruthi (@vineet-pruthi)
description:
  - Manage dws cluster.
options:
  availability_zone:
    description: Availability Zone of a cluster.
    type: str
  num_cn:
    description:
    - Number of deployed CNs. The value ranges from 2 to the number of
      cluster nodes. The maximum value is 20 and the default value is 3.
    type: int
  flavor:
    description: Cluster flavor (node type).
    type: str
  name:
    description:
      - Cluster name.
      - It contains 4 to 32 characters. Only letters, digits, hyphens (-), and
        underscores (_) are allowed.
      - The value must start with a letter.
    required: true
    type: str
  network:
    description: Name or ID of the neutron network
    type: str
  num_nodes:
    description:
      - Number of cluster nodes.
      - For a cluster, the value ranges from 3 to 256.
        For a hybrid data warehouse (standalone), the value is 1.
    type: int
  password:
    description:
      - Administrator password for logging in to a GaussDB(DWS) cluster.
      - Contains 12 to 32 characters.
      - Contains at least three types of the following characters
        uppercase letters, lowercase letters, digits, and special characters.
      - Cannot be the same as the username or the username written in reverse order.
    type: str
  port:
    description:
      - Service port of a cluster. The value ranges from 8000 to 30000.
        The default value is 8000.
    type: int
  public_ip:
    description:
      - Public IP address. If the parameter is not specified,
        public connection is not used by default.
    type: dict
    suboptions:
      public_bind_type:
        description:
          - Binding type of an EIP.
        choices:
          - auto_assign
          - not_use
          - bind_existing
        type: str
      eip:
        description:
          - Elastic IP address or ID.
        type: str
  router:
    description: Name or ID of the Neutron router (VPC)
    type: str
  security_group:
    description: Name or ID of the security group
    type: str
  state:
    description: Instance state
    type: str
    choices:
      - present
      - absent
    default: present
  tags:
    description:
      - Tags in a cluster.
    type: list
    elements: dict
    suboptions:
      key:
        description:
          - Tag key. The value can contain 1 to 36 characters.
            Only digits, letters, hyphens (-) and underscores (_) are allowed.
      value:
        description:
          - Tag value. The value can contain 0 to 43 characters.
            Only digits, letters, hyphens (-) and underscores (_) are allowed.
  username:
    description:
      - Administrator username for logging in to a GaussDB(DWS) cluster.
        The administrator username must-
      - Consist of lowercase letters, digits, or underscores.
      - Start with a lowercase letter or an underscore.
      - Contain 1 to 63 characters.
      - Cannot be a keyword of the GaussDB(DWS) database.
    default: dbadmin
    type: str
  wait:
     description:
        - If the module should wait for the cluster to be created.
     type: bool
     default: 'yes'
  timeout:
    description:
      - The amount of time the module should wait for the cluster to get
        into active state.
    default: 1200
    type: int
'''

RETURN = '''
cluster:
    description: Dictionary of dws cluster
    returned: changed
    type: list
    sample: [
        {
            "cluster": {
                "id": "ef683016-871e-48bc-bf93-74a29d60d214",
                "name": "ES-Test"
            }
        }
    ]
'''

EXAMPLES = """
#Create dws Cluster
---
- hosts: localhost
  tasks:
    - name: Create dws cluster
      opentelekomcloud.cloud.dws_cluster:
        name: DWS-Test
        state: present
        num_cn: 2
        num_nodes: 3
        router: '{{ router_id }}'
        network: '{{ network_id }}'
        security_group: '{{ security_group_id }}'
        flavor: 'dws.xlarge.2'
        username: dbadmin
        password: 'SecretPassword'
        port: 8000
        timeout: 1200
        tags:
        - key: "key0"
          value: "value0"
        - key: "key1"
          value: "value1"

#Delete dws Cluster
- hosts: localhost
  tasks:
    - name: Delete dws cluster
      opentelekomcloud.cloud.dws_cluster:
        name: dws-test
        state: absent
"""

from ansible_collections.openstack.cloud.plugins.module_utils.resource import (
    StateMachine,
)
from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import (
    OTCModule,
)


class dwsClusterModule(OTCModule):
    argument_spec = dict(
        name=dict(type="str", required=True),
        availability_zone=dict(type="str"),
        num_nodes=dict(type="int"),
        num_cn=dict(type="int"),
        port=dict(type="int"),
        flavor=dict(type="str"),
        public_ip=dict(
            type="dict",
            options=dict(
                public_bind_type=dict(
                    type="str",
                    choices=["auto_assign", "not_use", "bind_existing"],
                ),
                eip=dict(type="str"),
            ),
        ),
        router=dict(type="str"),
        network=dict(type="str"),
        security_group=dict(type="str"),
        tags=dict(required=False, type="list", elements="dict"),
        username=dict(type="str", default="dbadmin"),
        password=dict(type="str", no_log=True),
        state=dict(
            type="str", choices=["present", "absent"], default="present"
        ),
        wait=dict(type="bool", default=True),
        timeout=dict(type="int", default=1200),
    )
    module_kwargs = dict(
        required_if=[
            (
                "state",
                "present",
                [
                    "flavor",
                    "router",
                    "network",
                    "security_group",
                    "name",
                    "num_nodes",
                    "password",
                ],
            ),
        ],
        supports_check_mode=True,
    )

    class _StateMachine(StateMachine):

        def _create(self, attributes, timeout, wait, **kwargs):
            resource = self.create_function(**attributes)
            wait_function = getattr(self.session, "wait_for_cluster")
            wait_function(resource, wait=timeout)
            return self.get_function(resource.id)

    def run(self):
        service_name = "dws"
        type_name = "cluster"
        session = getattr(self.conn, "dws")
        create_function = getattr(session, "create_{0}".format(type_name))
        delete_function = getattr(session, "delete_{0}".format(type_name))
        get_function = getattr(session, "get_{0}".format(type_name))
        find_function = getattr(session, "find_{0}".format(type_name))
        list_function = getattr(session, "{0}s".format(type_name))

        crud = dict(
            create=create_function,
            delete=delete_function,
            find=find_function,
            get=get_function,
            list=list_function,
            update=None,
        )

        sm = self._StateMachine(
            connection=self.conn,
            service_name=service_name,
            type_name=type_name,
            sdk=self.sdk,
            crud_functions=crud,
        )

        kwargs = dict(
            (k, self.params[k])
            for k in ["state", "timeout", "wait"]
            if self.params[k] is not None
        )
        kwargs["attributes"] = {"name": self.params["name"]}

        if self.params["state"] == "present":
            vpc_id = self.conn.vpc.find_vpc(
                self.params["router"], ignore_missing=False
            ).id
            net_id = None
            network = self.conn.vpc.find_subnet(
                self.params["network"], ignore_missing=True
            )
            if network:
                net_id = network.id
            else:
                net_id = self.conn.network.find_network(
                    self.params["network"], ignore_missing=False
                ).id

            security_group_id = self.conn.network.find_security_group(
                self.params["security_group"], ignore_missing=False
            ).id
            attrs = {
                "flavor": self.params["flavor"],
                "num_nodes": self.params["num_nodes"],
                "router_id": vpc_id,
                "network_id": net_id,
                "security_group_id": security_group_id,
                "user_name": self.params["username"],
                "user_pwd": self.params["password"],
            }
            if self.params["availability_zone"]:
                attrs['availability_zone'] = self.params["availability_zone"]
            if self.params["num_cn"]:
                attrs["num_cn"] = self.params["num_cn"]
            if self.params["availability_zone"]:
                attrs["availability_zone"] = self.params["availability_zone"]
            if self.params["port"]:
                attrs["port"] = self.params["port"]
            if self.params["public_ip"]:
                attrs["public_ip"] = self.params["public_ip"]
            if self.params['tags']:
                attrs['tags'] = self.params['tags']

            kwargs['attributes'].update(**attrs)

        cluster, is_changed = sm(
            check_mode=self.ansible.check_mode,
            updateable_attributes=[],
            non_updateable_attributes=[
                "flavor",
                "router",
                "network",
                "security_group",
                "availability_zone",
                "name",
                "num_nodes",
                "username",
                "password",
                "port",
                "public_ip",
                "num_cn",
            ],
            **kwargs
        )

        self.exit_json(changed=is_changed)


def main():
    module = dwsClusterModule()
    module()


if __name__ == "__main__":
    main()
