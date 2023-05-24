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
module: sfsturbo_share
short_description: Manage SFS Turbo file system.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.12.4"
author: "Gubina Polina (@Polina-Gubina)"
description:
    - Manage SFS Turbo file system from the OTC.
options:
  id:
    description:
      - Specifies the id of the SFS Turbo file system.
    type: str
  name:
    description:
      - Specifies the name of the SFS Turbo file system.
    type: str
  share_proto:
    description:
      - Specifies the protocol of the file system. The valid value is NFS.
        Network File System (NFS) is a distributed file system protocol that
        allows different computers and operating systems to share data over a
        network.
    type: str
  share_type:
    description:
        - Specifies the file system type.  Standard file system, corresponding
          to the media of SAS disks. Performance file system, corresponding
          to the media of SSD disks.
    type: str
    choices: ['STANDARD', 'PERFORMANCE']
  size:
    description:
      - For a common file system, the value of capacity ranges from 500 to
        32768 (in the unit of GB). For an enhanced file system where the
        expand_type field is specified for metadata, the capacity ranges
        from 10240 to 327680. 
    type: int
  availability_zone:
    description:
      - Specifies the code of the AZ where the file system is located.
    type: str
  vpc_id:
    description:
      - Specifies the VPC ID of a tenant in a region. 
    type: str
  subnet_id:
    description:
      - Specifies the network ID of the subnet of a tenant in a VPC.
    type: str
  security_group_id:
    description:
      - Specifies the security group ID of a tenant in a region.
    type: str
  description:
    description:
      - Specifies the file system description. The length is 0-255 characters.
    type: str
  metadata:
    description:
      - Specifies the metadata information used to create the file system.
    type: dict
    suboptions:
      expand_type:
        description:
          - Specifies the extension type. The current valid value is bandwidth,
            indicating that an enhanced file system is created.
        type: str
      crypt_key_id:
        description:
          - Specifies the ID of a KMS professional key when an encrypted
            file system is created. 
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
share:
    description: Share object.
    type: complex
    returned: On Success.
    contains:
      id:
        description: Specifies the ID of the SFS Turbo file system.
        type: str
      name:
        description: Specifies the name of the SFS Turbo file system.
        type: str
      status:
        description: Specifies the status of the SFS Turbo file system. 
        type: str
        description: Creation time.
        type: str
'''

EXAMPLES = '''
- name: Create sfs turbo share
  opentelekomcloud.cloud.sfsturbo_share:
    name: "test_share_1"
    share_proto: "NFS"
    share_type: "STANDARD"
    size: 100
    availability_zone: 'eu-de-01'
    vpc_id: "vpc_uuid"
    subnet_id: "subnet_uuid"
    security_group_id: "security_group_uuid"
  register: share

- name: Delete sfs turbo share
  opentelekomcloud.cloud.sfsturbo_share:
    name: "test_share_1"
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule
from ansible_collections.openstack.cloud.plugins.module_utils.resource import StateMachine


class SfsTurboShareModule(OTCModule):
    argument_spec = dict(
        id=dict(type='str'),
        name=dict(type='str'),
        share_proto=dict(type='str'),
        share_type=dict(type='str', choices=['STANDARD', 'PERFORMANCE']),
        size=dict(type='int'),
        availability_zone=dict(type='str'),
        vpc_id=dict(type='str'),
        subnet_id=dict(type='str'),
        security_group_id=dict(type='str'),
        description=dict(type='str'),
        metadata=dict(type='dict', options=dict(expand_type=dict(type='str'),
                                                crypt_key_id=dict(type='str')),
        state=dict(type='str', required=False, choices=['present', 'absent'],
                   default='present'))
    )

    module_kwargs = dict(
        supports_check_mode=True,
    )

    def run(self):
        session = getattr(self.conn, 'network')

        create_function = getattr(session, 'create_{0}'.
                                  format('share'))
        delete_function = getattr(session, 'delete_{0}'.
                                  format('share'))
        find_function = getattr(session, 'find_{0}'.
                                format('share'))
        get_function = getattr(session, 'get_{0}'.
                               format('share'))
        list_function = getattr(session, '{0}'.
                                format('shares'))

        crud_functions = dict(
            create=create_function,
            delete=delete_function,
            find=find_function,
            get=get_function,
            list=list_function,
            update=update_function
        )
        sm = StateMachine(connection=self.conn,
                          service_name='sfsturbo',
                          type_name='share',
                          sdk=self.sdk,
                          crud_functions=crud_functions)
        kwargs = dict((k, self.params[k])
                      for k in ['state', 'timeout']
                      if self.params[k] is not None)

        kwargs['attributes'] = \
            dict((k, self.params[k]) for k in
                 ['id', 'name', 'share_proto', 'share_type',
                  'size', 'availability_zone', 'vpc_id', 'subnet_id',
                  'security_group_id', 'description', 'metadata']
                 if self.params[k] is not None)
        share, is_changed = sm(check_mode=self.ansible.check_mode,
                               updateable_attributes=None,
                               non_updateable_attributes=None,
                               wait=False,
                               **kwargs)

        self.exit_json(share=share, changed=is_changed)


def main():
    module = SfsTurboShareModule()
    module()


if __name__ == '__main__':
    main()
