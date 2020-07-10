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
---
module: cce_cluster_cert_info
short_description: Get Certificates of a CCE cluster
extends_documentation_fragment: openstack
version_added: "2.9"
author: "Artem Goncharov (@gtema)"
description:
  - Get CCE cluster certificates info from the OTC.
options:
  cluster:
    description: Name of the cluster.
    required: true
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
cce_cluster_certs:
    description: Dictionary containing cluster certificates.
    type: complex
    returned: On Success.
    contains:
        ca:
            description: Authority Certificate content.
            type: str
        client_certificate:
            description: Client Certificate content.
            type: str
        client_key:
            description: Private key for Client Certificate.
            type: str
        context:
            description: Dictionary with the certificate context information.
            type: dict
'''

EXAMPLES = '''
# Get configs versions.
- cce_cluster_info:
  register: data
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CceClusterCertInfoModule(OTCModule):
    argument_spec = dict(
        cluster=dict(required=True),
    )

    def run(self):
        cluster = self.params['cluster']

        cluster = self.conn.cce.find_cluster(cluster, ignore_missing=False)

        certs = self.conn.cce.get_cluster_certificates(cluster).to_dict()
        certs.pop('location')
        certs.pop('id')
        certs.pop('name')

        self.exit_json(
            changed=False,
            cce_cluster_certs=certs
        )


def main():
    module = CceClusterCertInfoModule()
    module()


if __name__ == '__main__':
    main()
