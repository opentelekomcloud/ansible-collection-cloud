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
module: cbr_restore_point
short_description: Manage CBR Restore Point
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.12.4"
author: "Gubina Polina (@Polina-Gubina)"
description:
    - Manage cbr restore point from the OTC.
options:
  vault:
    description:
      - Vault name or id.
    type: str
    required: true
  auto_trigger:
    description:
        - Whether automatic triggering is enabled
    type: bool
    default: False
  description:
    description:
        - Backup description.
    type: str
  incremental:
    description:
      - Whether the backup is an incremental backup.
    type: bool
  name:
    description:
      - Backup name.
    type: str
  resources:
    description:
      - UUID list of resources to be backed up.
    type: list
    elements: str
  resource_details:
    description:
      - Resource details.
    type: list
    elements: dict
    suboptions:
      id:
        description: Cloud type, which is public.
        type: str
        required: true
      name:
        description:
          - Name of the resource to be backed up.\
          The value consists of 0 to 255 characters..
        type: str
      type:
        description: Cloud type, which is public.
        type: str
        required: true
        choices: ['OS::Nova::Server', 'OS::Cinder::Volume']
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
checkpoint:
    description: Restore point object.
    type: complex
    returned: On Success.
    contains:
      created_at:
        description: Creation time.
        type: str
      id:
        description: Restore point ID.
        type: str
      project_id:
        description: Project id.
        type: str
      status:
        description: Status.
        type: str
      vault:
        description: Project ID.
        type: complex
        contains:
          id:
            description: Vault ID.
            type: str
          name:
            description: Vault name.
            type: str
          resources:
            description: Backup name.
            type: dict
            contains:
              extra_info:
                description: Extra information of the resource.
                type: str
              id:
                description: ID of the resource to be backed up.
                type: str
              name:
                description: Name of the resource to be backed up.
                type: str
              protect_status:
                description: Protected status.
                type: str
              resource_size:
                description: Allocated capacity for the associated resource,\
                 in GB.
                type: str
              type:
                description: Type of the resource to be backed up.
                type: str
              backup_size:
                description: Backup size.
                type: str
              backup_count:
                description: Number of backups.
                type: str
          skipped_resources:
            description: Backup name.
            type: str
            contains:
              id:
                description: Resource ID.
                type: str
              type:
                description: Resource type.
                type: str
              name:
                description: Resource name.
                type: str
              code:
                description: Error code.
                type: str
              reason:
                description: Reason for the skipping. For example,\
                 the resource is being backed up.
                type: str
      extra_info:
        description: Vault name.
        type: dict
        contains:
          name:
            description: Backup name.
            type: str
          description:
            description: Backup description.
            type: str
          retention_duration:
            description: Number of days that backups can be retained.
            type: int
'''

EXAMPLES = '''
# Create a restore point
opentelekomcloud.cloud.cbr_restore_point:
  vault: "vault-name-or-id"
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CBRRestorePointModule(OTCModule):
    argument_spec = dict(
        vault=dict(required=True, type='str'),
        auto_trigger=dict(required=False, type='bool', default=False),
        description=dict(required=False, type='str'),
        incremental=dict(required=False, type='bool'),
        name=dict(type='str', required=False),
        resources=dict(type='list', elements='str', required=False),
        resource_details=dict(type='list', elements='dict', required=False,
                              options=dict(
                                  id=dict(required=True, type='str'),
                                  name=dict(required=False, type='str'),
                                  type=dict(required=True, type='str',
                                            choices=['OS::Nova::Server',
                                                     'OS::Cinder::Volume'])
                              )
                              )
    )

    def _parse_resource_details(self):
        resource_details = self.params['resource_details']
        parsed_resource_details = []
        for rd in resource_details:
            parsed_rd = {}
            parsed_rd['id'] = rd.get('id')\
                if rd.get('id') else self.fail_json(msg="'id' is required for 'resource_details'")
            parsed_rd['type'] = rd.get('type')\
                if rd.get('type') else self.fail_json(msg="'type' is required for 'resource_details'")
            if rd.get('name'):
                parsed_rd['name'] = rd.get('name')
            parsed_resource_details.append(parsed_rd)
        return parsed_resource_details

    def run(self):
        attrs = {}
        vault_id = self.conn.cbr.find_vault(name_or_id=self.params['vault']).id
        attrs['vault_id'] = vault_id
        if self.params['auto_trigger']:
            attrs['auto_trigger'] = self.params['auto_trigger']
        if self.params['description']:
            attrs['description'] = self.params['description']
        if self.params['incremental']:
            attrs['incremental'] = self.params['incremental']
        if self.params['name']:
            attrs['name'] = self.params['name']
        if self.params['resources']:
            attrs['resources'] = self.params['resources']
        if self.params['resource_details']:
            attrs['resource_details'] = self._parse_resource_details()

        checkpoint = self.conn.cbr.create_checkpoint(**attrs)
        self.exit(changed=True, checkpoint=checkpoint)


def main():
    module = CBRRestorePointModule()
    module()


if __name__ == '__main__':
    main()
