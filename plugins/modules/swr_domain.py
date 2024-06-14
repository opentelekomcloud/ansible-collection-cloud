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
module: swr_domain
short_description: Create, update or delete domains in SWR
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.14.2"
author: "Ziukina Valeriia (@RusselSand)"
description:
  - Create, update or delete domains in Software Repository for Containers
options:
  namespace:
    description: Mandatory name of organization.
    type: str
    required: true
  repository:
    description: Mandatory name of repository
    type: str
    required: true
  access_domain:
    description: Mandatory name of existing domain you want to share
    type: str
    required: true
  permit:
    description:
      - Access permission. Currently supported only read
      - Mandatory for CREATE and UPDATE operations
    choices: ['read']
    type: str
    default: 'read'
  deadline:
    description:
      - Valid until.
      - If sharing is permanent, the value is forever.
      - Mandatory for CREATE and UPDATE operations
    type: str
    default: 'forever'
  description:
    description: Description for domain
    type: str
  state:
    description:
      - Whether resource should be present or absent.
    choices: ['present', 'absent']
    type: str
    default: 'present'
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
domain:
    description: Domain object.
    type: complex
    returned: On Success.
    contains:
        exist:
          description: Domain exists or not
          type: bool
          sample: true
        namespace:
          description: Organization name
          type: str
          sample: "org_name"
        repository:
          description: Repository name
          type: str
          sample: "repo_name"
        access_domain:
          description: Domain name
          type: str
          sample: "domain_name"
        permit:
          description: Permission
          type: str
          sample: "read"
        deadline:
          description: Expiration time
          type: str
          sample: "2021-10-01T16:00:00Z"
        description:
          description: Description
          type: str
          sample: "description"
        creator_id:
          description: ID of the creator
          type: str
          sample: "0504186e6a8010e01f3ec009a7279baa"
        creator_name:
          description: Name of the creator
          type: str
          sample: "xxx"
        created:
          description: Time when an image is created. It is the UTC standard time.
          type: str
          sample: "2021-06-10T08:14:42.56632Z"
        updated:
          description: Time when an image is updated. It is the UTC standard time.
          type: str
          sample: "2021-06-10T08:14:42.56632Z"
        status:
          description: Status. Valid of true, expired if false
          type: bool
          sample: true
'''

EXAMPLES = '''
# Create or delete SWR domain
- name: Create new organization
  opentelekomcloud.cloud.swr_domain:
    namespace: org_name
    repository: repo_name
    access_domain: domain_name

- name: Delete the domain
  opentelekomcloud.cloud.swr_domain:
    namespace: org_name
    repository: repo_name
    access_domain: domain_name
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule
from ansible_collections.openstack.cloud.plugins.module_utils.resource import StateMachine


class SwrDomainMachine(StateMachine):
    def _build_update(self, resource, attributes, updateable_attributes,
                      non_updateable_attributes, **kwargs):
        update = {}
        resource_attributes = {'repository': attributes['repository'], 'namespace': attributes['namespace'],
                               'access_domain': attributes['access_domain'], 'permit': attributes['permit'],
                               'deadline': attributes['deadline']}
        if resource['description']:
            resource_attributes['description'] = attributes['description']

        if resource_attributes:
            update['resource_attributes'] = resource_attributes

        return update

    def _update(self, resource, timeout, update, wait, **kwargs):
        resource_attributes = update.get('resource_attributes')
        if resource_attributes:
            resource = self.update_function(**resource_attributes)
        if wait:
            resource = self.sdk.resource.wait_for_status(self.session,
                                                         resource,
                                                         status='active',
                                                         failures=['error'],
                                                         wait=timeout,
                                                         attribute='status')

        return resource

    def _delete(self, resource, attributes, timeout, wait, **kwargs):
        attrs = {
            'namespace': attributes['namespace'],
            'repository': attributes['repository'],
            'access_domain': attributes['access_domain']
        }
        self.delete_function(**attrs)

    def _find(self, attributes, **kwargs):
        domain = self.get_function(attributes['namespace'],
                                   attributes['repository'],
                                   attributes['access_domain'])
        if domain.exist:
            return domain
        else:
            return None


class SwrDomainModule(OTCModule):
    argument_spec = dict(
        namespace=dict(required=True),
        repository=dict(required=True),
        access_domain=dict(required=True),
        permit=dict(required=False,
                    type='str',
                    choices=['read'],
                    default='read'),
        deadline=dict(required=False,
                      type='str',
                      default='forever'),
        description=dict(required=False),
        state=dict(type='str',
                   required=False,
                   choices=['present', 'absent'],
                   default='present'),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        service_name = "swr"
        type_name = "domain"
        session = getattr(self.conn, service_name)
        create_function = getattr(session, 'create_{0}'.format(type_name))
        delete_function = getattr(session, 'delete_{0}'.format(type_name))
        get_function = getattr(session, 'get_{0}'.format(type_name))
        list_function = getattr(session, 'domains')
        update_function = getattr(session, 'update_{0}'.format(type_name))
        crud = dict(
            create=create_function,
            delete=delete_function,
            find=get_function,
            get=get_function,
            list=list_function,
            update=update_function, )
        sm = SwrDomainMachine(connection=self.conn,
                              sdk=self.sdk,
                              service_name=service_name,
                              type_name=type_name,
                              crud_functions=crud)
        kwargs = {'state': self.params['state'],
                  'attributes': dict((k, self.params[k]) for k in
                                     ['namespace', 'repository', 'access_domain', 'permit', 'deadline', 'description']
                                     if self.params[k] is not None)}
        domain, is_changed = sm(check_mode=self.ansible.check_mode,
                                non_updateable_attributes=['namespace', 'repository', 'access_domain'],
                                updateable_attributes=['permit', 'deadline', 'description'],
                                wait=False,
                                timeout=600,
                                **kwargs)
        self.exit_json(domain=domain, changed=is_changed)


def main():
    module = SwrDomainModule()
    module()


if __name__ == "__main__":
    main()
