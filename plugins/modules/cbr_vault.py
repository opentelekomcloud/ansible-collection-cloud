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
module: cbr_vault
short_description: Manage CBR Vault
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Gubina Polina (@Polina-Gubina)"
description:
    - Manage cbr vault from the OTC.
options:
  name_or_id:
    description:
      - Vault name or id.
    type: str
    required: true
  policy:
    description:
      - Backup policy name or id. If the value of this parameter is null,\
       automatic backup is not performed. Can be set during creation and for\
       binding/unbinding policy to the vault.
    type: str
  billing:
    description:
        - Parameter information for creation. Mandatory for creation.
    type: dict
    suboptions:
      cloud_type:
        description:
          - Cloud type, which is public.
        type: str
      consistent_level:
        description:
          - Specification, which is crash_consistent\
           by default (crash consistent backup).
        type: str
        default: "crash_consistent"
        required: true
      object_type:
        description:
          - Object type, which can be server or disk.
        type: str
        required: true
        choices: ['server', 'disk']
      protect_type:
        description:
          - Protection type, which is backup.
        type: str
        required: true
      size:
        description:
          - Capacity, in GB. Minimum 1, maximum 10485760.
        type: int
        required: true
      charging_mode:
        description:
          - Billing mode, which is post_paid.
        default: "post_paid"
        type: str
      is_auto_renew:
        description:
          - Whether to automatically renew the subscription after expiration.\
           By default, it is not renewed.
        default: False
        type: bool
      is_auto_pay:
        description:
          - Whether the fee is automatically deducted from the\
           customer's account balance after an order is submitted.\
           The non-automatic payment mode is used by default.
        type: bool
        default: False
      console_url:
        description:
          - Redirection URL. Minimum 1, maximum 255.
        type: str
  description:
    description:
      - User-defined vault description. Minimum 0, maximum 64.
    type: str
  resources:
    description:
      - Associated resources. Set this parameter to [] if no\
       resources are associated when creating a vault. Mandatory for creation\
       and associating resources.
    type: list
    elements: dict
    suboptions:
      id:
        description:
          - ID of the resource to be backed up.
        type: str
        required: true
      type:
        description:
          - Type of the resource to be backed up.
        type: str
        required: true
        choices: ['OS::Nova::Server', 'OS::Cinder::Volume']
      name:
        description:
          - Resource name. Minimum 0, maximum 255.
        type: str
        required: false
  tags:
    description:
      - Tag list. This list cannot be an empty list. The list can contain\
      up to 10 keys. Keys in this list must be unique.
    type: list
    elements: dict
    suboptions:
      key:
        description:
          - Key. It can contain a maximum of 36 characters.
        type: str
        required: true
      value:
        description:
          - Value. It is mandatory when a tag is added and optional when\
           a tag is deleted.
        type: str
  auto_bind:
    description:
      - Whether automatic association is supported.
    type: bool
  bind_rules:
    description:
      - Rules for automatic association. Filters automatically associated\
       resources by tag.
    type: list
    elements: dict
    suboptions:
      key:
        description:
          - Key. It can contain a maximum of 36 characters.
        type: str
        required: true
      value:
        description:
          - Value. It is mandatory when a tag is added and optional when\
           a tag is deleted.
        type: str
  resource_ids:
    description:
      - List of resource IDs to be removed. Used for dissociating resources.
    type: list
    elements: str
  auto_expand:
    description:
      - Whether to enable auto capacity expansion for the vault.\
      Can be set in update.
    type: bool
  smn_notify:
    description:
      - Exception notification function.
    type: bool
    default: true
  threshold:
    description:
      - Vault capacity threshold. If the vault capacity usage exceeds this\ 
      threshold and smn_notify is true, an exception notification is sent.\
      Can be set only in update.
    type: int
    default: 80
  state:
    description:
      - Whether resource should be present or absent.
    choices: ['present', 'absent']
    type: str
    default: 'present'
  action:
    description:
      - What needs to be done.
    choices: ['associate_resources', 'dissociate_resources', 'bind_policy',/
                                                            'unbind_policy']
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
'''

EXAMPLES = '''
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class CBRVaultModule(OTCModule):
    argument_spec = dict(
        name_or_id=dict(required=True, type='str'),
        policy=dict(required=False),
        billing=dict(required=False, type=dict, options=dict(
            cloud_type=dict(required=False, type='str'),
            consistent_level=dict(required=True, type='str'),
            object_type=dict(required=True, type='str',
                             choices=['server','disk']),
            protect_type=dict(required=True, type='str'),
            size=dict(required=True, type='str'),
            charging_mode=dict(required=True, type='str', default='post_paid'),
            is_auto_renew=dict(required=False, type='bool', default=False),
            is_auto_pay=dict(required=False, type='bool', default=False),
            console_url=dict(required=False, type='str'),)),
        description=dict(required=False, type='str'),
        resources=dict(type='list', elements='dict', options=dict(
            id=dict(required=False, type='str'),
            type=dict(required=True, type='str',
                      choices=['OS::Nova::Server', 'OS::Cinder::Volume']),
            name=dict(required=False, type='str')
            )),
        resource_ids=dict(required=False, type='list', elements='str'),
        tags=dict(required=False, type='list', elements='dict',
                  options=dict(key=dict(required=True, type='str'),
                               value=dict(required=True, type='str'))),
        auto_bind=dict(type='bool', required=False),
        bind_rules=dict(type='list', required=False, elements=dict,
                        options=dict(key=dict(required=True, type='str'),
                                     value=dict(required=True, type='str'))),
        auto_expand=dict(type='bool', required=False),
        smn_notify=dict(type='bool', default=True, required=False),
        threshold=dict(type='int', default=80, required=False),
        state=dict(type='str', required=False, choices=['present', 'absent'],
                   default='present'),
        action=dict(type='str', required=False, choices=['associate_resources',
                    'dissociate_resources', 'bind_policy', 'unbind_policy'])
    )
    module_kwargs = dict(
        required_if=[
            ('action', 'associate_resources', ['name_or_id', 'resources']),
            ('action', 'dissociate_resources', ['name_or_id', 'resource_ids']),
            ('action', 'bind_policy', ['name_or_id', 'policy']),
            ('action', 'unbind_policy', ['name_or_id', 'policy'])
        ],
        supports_check_mode=True
    )

    def _parse_resources(self):
        resources = self.params['resources']
        parsed_resources = []
        for resource in resources:
            parsed_resource = {}
            parsed_resource['id'] = resource.get('id')\
                if resource.get('id') else self.fail_json(msg="'id' is required for 'resource'")
            parsed_resource['type'] = resource.get('type')\
                if resource.get('type') else self.fail_json(msg="'type' is required for 'resource'")
            if resource.get('name'):
                parsed_resource['name'] = resource.get('name')
            parsed_resources.append(parsed_resource)
        return parsed_resources

    def _parse_tags(self):
        tags = self.params['tags']
        parsed_tags = []
        for tag in tags:
            parsed_tag = {}
            parsed_tag['key'] = tag.get('key')\
                if tag.get('key') else self.fail_json(msg="'key' is required for 'tag'")
            parsed_tag['value'] = tag.get('value')\
                if tag.get('value') else self.fail_json(msg="'value' is required for 'tag'")
            parsed_tags.append(parsed_tag)
        return parsed_tags

    def _parse_billing(self):
        billing = self.params['billing']
        parsed_billing = {}
        if billing.get('cloud_type'):
            parsed_billing['cloud_type'] = billing['cloud_type']
        parsed_billing['consistent_level'] = billing['consistent_level']\
            if billing.get('consistent_level') else self.fail_json(msg="'consistent_level' is required for 'billing'")
        parsed_billing['object_type'] = billing['object_type'] \
            if billing.get('object_type') else self.fail_json(msg="'object_type' is required for 'billing'")
        parsed_billing['protect_type'] = billing['protect_type'] \
            if billing.get('protect_type') else self.fail_json(msg="'protect_type' is required for 'billing'")
        parsed_billing['size'] = billing['size'] \
            if billing.get('size') else self.fail_json(msg="'size' is required for 'billing'")
        if billing.get('charging_mode'):
            parsed_billing['charging_mode'] = billing['charging_mode']
        if billing.get('is_auto_renew'):
            parsed_billing['is_auto_renew'] = billing['is_auto_renew']
        if billing.get('is_auto_pay'):
            parsed_billing['is_auto_pay'] = billing['is_auto_pay']
        if billing.get('console_url'):
            parsed_billing['console_url'] = billing['console_url']
        return parsed_billing

    def run(self):
        attrs = {}
        action = None
        policy = None
        state = self.params['state']
        if self.params['description']:
            attrs['description'] = self.params['description']
        if self.params['auto_bind']:
            attrs['auto_bind'] = self.params['auto_bind']
        if self.params['auto_expand']:
            attrs['auto_expand'] = self.params['auto_expand']
        if self.params['smn_notify']:
            attrs['smn_notify'] = self.params['smn_notify']
        if self.params['threshold']:
            attrs['threshold'] = self.params['threshold']
        if self.params['policy']:
            policy = self.conn.cbr.find_policy(name_or_id=self.params['policy'])
            if policy:
                attrs['policy_id'] = policy.id
            else:
                self.fail_json("'policy' not found")
        if self.params['resources']:
            attrs['resources'] = self._parse_resources()
        else:
            attrs['resources'] = []
        if self.params['billing']:
            attrs['billing'] = self._parse_billing()
        if self.params['tags']:
            attrs['tags'] = self._parse_tags()
        if self.params['action']:
            action = self.params['action']

        vault = self.conn.cbr.find_vault(name_or_id=self.params['name_or_id'],
                                         ignore_missing=True)
        if vault:
            if self.ansible.check_mode:
                self.exit_json(changed=True)

            if action == 'associate_resources':
                resources = self._parse_resources()
                self.conn.cbr.associate_resources(vault=vault.id,
                                                  resources=resources)

            if action == 'dissociate_resources':
                resource_ids = self.params['resource_ids']
                self.conn.cbr.dissociate_resources(
                    vault=vault, resources=resource_ids)

            if action == 'bind_policy':
                self.conn.cbr.bind_policy(vault=vault, policy=policy)

            if action == 'unbind_policy':
                self.conn.cbr.unbind_policy(vault=vault, policy=policy)

            if state == 'absent':
                self.conn.cbr.delete_vault(vault=vault)
            self.exit(changed=True)

        if state == 'absent':
            if self.ansible.check_mode:
                self.exit_json(changed=False)

        if action in ('associate_resources', 'dissociate_resources',
                      'bind_policy', 'unbind_policy') or state == 'absent':
            if self.ansible.check_mode:
                self.exit_json(changed=False)
            self.fail_json('vault not found')

        attrs['name'] = self.params['name_or_id']
        if self.ansible.check_mode:
            self.exit_json(changed=True)
        created_vault = self.conn.cbr.create_vault(**attrs)
        self.exit(changed=True, vault=created_vault)


def main():
    module = CBRVaultModule()
    module()


if __name__ == '__main__':
    main()
