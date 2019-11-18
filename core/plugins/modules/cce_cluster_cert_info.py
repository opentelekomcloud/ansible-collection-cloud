#!/usr/bin/env python
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

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

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
  name:
    description: Name of the cluster.
    required: true
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
'''

EXAMPLES = '''
# Get configs versions.
- cce_cluster_info:
  register: data
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.opentelekomcloud.core.plugins.module_utils.otc \
    import openstack_full_argument_spec, \
    openstack_module_kwargs, openstack_cloud_from_module


def main():
    argument_spec = openstack_full_argument_spec(
        cluster=dict(required=True),
    )
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(
        argument_spec=argument_spec,
        **module_kwargs)
    sdk, cloud = openstack_cloud_from_module(module)

    cluster = module.params['cluster']

    try:
        cluster = cloud.cce.find_cluster(cluster, ignore_missing=False)

        certs = cloud.cce.get_cluster_certificates(cluster).to_dict()
        certs.pop('location')
        certs.pop('id')
        certs.pop('name')

        module.exit_json(
            changed=False,
            cce_cluster_certs=certs
        )

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)


if __name__ == "__main__":
    main()
