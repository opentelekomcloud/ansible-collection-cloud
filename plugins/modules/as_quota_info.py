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
module: as_quota_info
short_description: Get information about auto scaling quotas
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.1"
author: "Polina Gubina (@Polina-Gubina)"
description:
  - This module is used to query the total quotas and used quotas of AS \
    groups, AS configurations, bandwidth scaling policies, AS policies, and \
    instances for a specified tenant.
options:
  scaling_group:
    description: Name or id of an auto scaling group. If set, quota for this group will be outputed.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
as_quotas:
  description: The auto scaling quota object list.
  type: complex
  returned: On Success.
  contains:
    resources:
      description: Specifies resources.
      type: complex
      contains:
        type:
          description:
            - Specifies the quota type.
            - Can be 'scaling_Group', 'scaling_Config', 'scaling_Policy' \
            'sсaling_Instance', 'bandwidth_scaling_policy'.
          type: str
        used:
          description:
            - Specifies the used amount of the quota.
            - When type is set to scaling_Policy or scaling_Instance, \
            this parameter is reserved, and the system returns -1 as the \
            parameter value. You can query the used quota of AS policies \
            and AS instances in a specified AS group.
          type: int
        quota:
          description:
            - Specifies the total quota.
          type: int
        max:
          description:
            - Specifies the quota upper limit.
          type: int
'''

EXAMPLES = '''
# Get as quotas.
- opentelekomcloud.cloud.as_quota_info:
  register: as_quotas

# Get as quotas of a specified AS group.
- opentelekomcloud.cloud.as_quota_info:
    scaling_group: "test-group"
  register: as_quotas
'''


from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class ASQuotaInfoModule(OTCModule):
    argument_spec = dict(
        scaling_group=dict(required=False)
    )

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        data = []

        scaling_group_id = None
        if self.params['scaling_group']:
            try:
                scaling_group_id = self.conn.auto_scaling.find_group(self.params['scaling_group'],
                                                                     ignore_missing=False).id
            except self.sdk.exceptions.ResourceNotFound:
                self.fail_json(msg="Auto scaling group not found")

        for raw in self.conn.auto_scaling.quotas(group=scaling_group_id):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit_json(
            changed=False,
            as_quotas=data
        )


def main():
    module = ASQuotaInfoModule()
    module()


if __name__ == '__main__':
    main()
