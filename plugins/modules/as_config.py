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
module: as_config
short_description: Create/Remove AutoScaling configuration from the OTC
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: "Polina Gubina (@Polina-Gubina)"
description:
  - Create/Remove AutoScaling configuration from the OTC.
options:
  scaling_configuration_name:
    description:
      - Specifies the AS configuration name.
      - Mandatory for creating AS configuration.
    type: str
  scaling_configuration_id:
      - Specifies the AS configuration id.
      - Mandatory for deleting AS configuration.
    type: str
  instance_id:
    description:
      - Specifies the ECS ID.
      - When using the existing ECS specifications as the template to create AS configurations, specify this parameter. In this case, the flavorRef, imageRef, disk, and security_groups fields do not take effect.
      - If not specified, flavorRef, imageRef, and disk fields are mandatory.
    type: str
  flavor:
    description:
      - Specifies the ECS flavor ID or name. A maximum of 10 flavors can be selected. Use a comma (,) to separate multiple flavor IDs.
    type: str
  image:
    description:
      - Specifies the image ID or name. Its value is the same as that of image_id for specifying the image selected during ECS creation.
    type: str
  disk:
    description:
      - Specifies the disk group information. System disks are mandatory and data disks are optional.
    type: list
    elements: dict
    suboptions:
        size:
            description: 
                - Specifies the disk size. The unit is GB.
                - Mandatory.
            type: int
            required: true
        volume_type:
            description: 
                - Specifies the ECS system disk type.
                - Mandatory.
            type: str
            choices: ['sata', 'sas', 'ssd', 'co-p1', 'uh-l1']
            required: true
        disk_type:
            description: 
                - Specifies a disk type.
                - Mandatory.
            type: str
            choices: ['data', 'sys']
            required: true
        dedicated_storage_id:
            description: 
                - Specifies a DSS device ID for creating an ECS disk.
            type: str
        data_disk_image_id:
            description: 
                - Specifies the ID of a data disk image used to export data disks of an ECS.
            type: str
        snapshot_id:
            description: 
                - Specifies the disk backup snapshot ID for restoring the system disk and data disks using a full-ECS backup when a full-ECS image is used.
            type: str
        metadata:
            description: 
                - Specifies the metadata for creating disks.
            type: dict
            suboptions:
                __system__encrypted:
                    description: 
                        - Specifies encryption in metadata. The value can be 0 (encryption disabled) or 1 (encryption enabled).
                    type: str
                    choices: [ 0, 1 ]
                    default: 0
                __system__cmkid:
                    description: 
                        - Specifies the CMK ID, which indicates encryption in metadata.
                    type: str
  key_name:
    description:
      - Specifies the name of the SSH key pair used to log in to the ECS.
      - Mandatory for creating.
    type: str
  personality:
    description:
      - Specifies information about the injected file. Only text files can be injected. A maximum of five files can be injected at a time and the maximum size of each file is 1 KB.
    type: list
    elements: dict
    suboptions:
        path:
            description: 
                - Specifies the path of the injected file.
                - Mandatory.
            type: str
            required: true
        content:
            description: 
                - Specifies the content of the injected file.
                - Mandatory.
            type: str
            required: true
  public_ip:
    description:
      - Specifies the EIP of the ECS.
      - The EIP can be configured in two ways. 1.Do not use an EIP. 2. Automatically assign an EIP. You need to specify the information about the new EIP.
    type: dict
    suboptions:
        eip:
            description: 
                - Specifies the EIP automatically assigned to the ECS.
                - Mandatory.
            type: dict
            required: true
            suboptions:
                ip_type:
                    description: 
                        - Specifies the EIP type.
                        - Mandatory.
                    type: str
                    required: true
                bandwidth:
                    description: 
                        - Specifies the bandwidth of an IP address.
                        - Mandatory.
                    type: dict
                    required: true
                    suboptions:
                        size:
                            description: 
                                - Specifies the bandwidth (Mbit/s).
                                - Mandatory.
                            type: int
                            required: true
                        share_type:
                            description: 
                                - Specifies the bandwidth sharing type.
                                - Mandatory.
                            type: str
                            required: true
                        charging_mode:
                            description: 
                                - Specifies the bandwidth billing mode.
                                - Mandatory.
                            type: str
                            required: true
  user_data:
    description:
      - Specifies the user data to be injected during the ECS creation process. Text, text files, and gzip files can be injected.
      - The content to be injected must be encoded with base64. The maximum size of the content to be injected (before encoding) is 32 KB.
    type: str
  metadata:
    description:
      - Specifies the ECS metadata.
    type: dict
    suboptions:
        admin_pass:
            description: 
                - Specifies the initial login password of the administrator account for logging in to an ECS using password authentication. The Linux administrator is root, and the Windows administrator is Administrator.
            type: str
  security_groups:
    description:
      - Specifies security groups.
      - If the security group is specified both in the AS configuration and AS group, the security group specified in the AS configuration prevails. If the security group is not specified in either of them, the default security group is used.
    type: list
    elements: dict
    suboptions:
        id:
            description: 
                - Specifies the ID of the security group.
                - Mandatory.
            type: str
            required: true
  state:
    description:
      - Whether resource should be present or absent.
    choices: ['present', 'absent']
    type: str
    default: 'present'
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
as_group:
    description: AS groups object.
    type: complex
    returned: On Success.
    contains:
        scaling_configuration_id:
            description: Specifies the AS configuration ID.
            type: str
            sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
'''

EXAMPLES = '''
# Create as group.
- as_config:
    name: my_prod_as_group
  register: data
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class ASGroupModule(OTCModule):
    argument_spec = dict(
        scaling_configuration_name=dict(required=False),
        scaling_configuration_id=dict(required=False),
        instance_id=dict(required=False),
        flavor=dict(required=False),
        image=dict(required=False),
        disk=dict(required=False, type='list', elements='dict'),
        key_name=dict(required=False),
        personality=dict(required=False, type='list', elements='dict'),
        public_ip=dict(required=False, type='dict'),
        user_data=dict(required=False),
        metadata=dict(required=False, type='dict'),
        security_groups=dict(required=False, type='list', elements='dict'),
        state=dict(required=False, choices=['present', 'absent'], default='present'),
    )
    module_kwargs = dict(
        required_if=[
            ('state', 'present', ['scaling_configuration_name', 'key_name']),
            ('instance_id', None, ['flavor', 'image', 'disk']),
            ('scaling_group_name', None, ['scaling_configuration_id'])
        ],
        supports_check_mode=True
    )

    def run(self):

        scaling_configuration_name = self.params['scaling_configuration_name']
        scaling_configuration_id = self.params['scaling_configuration_id']
        instance_id = self.params['instance_id']
        flavor = self.params['flavor']
        image = self.params['image']
        disk = self.params['disk']
        key_name = self.params['key_name']
        personality = self.params['personality']
        public_ip = self.params['public_ip']
        user_data = self.params['user_data']
        metadata = self.params['metadata']
        security_groups = self.params['security_groups']
        state = self.params['state']

        as_config = None

        if scaling_configuration_name:
            as_config = self.conn.auto_scaling.find_config(scaling_configuration_name, ignore_missing=True)
        else:
            as_config = self.conn.auto_scaling.find_config(scaling_configuration_id, ignore_missing=True)

        if self.params['state'] == 'present':

            attrs = {
                'key_name': key_name
            }

            if self.params['instance_id']:
                attrs['instance_id'] = self.params['instance_id']
            if self.params['flavor']:
                flavor = self.conn.compute.find_flavor(self.params['flavor'], ignore_missing=True)
                if flavor:
                    attrs['flavorRef'] = flavor.id
                else:
                    self.fail_json(msg="Flavor not found")
            if self.params['image']:
                image = self.conn.image.find_image(self.params['image'], ignore_missing=True)
                if image:
                    attrs['imageRef'] = image.id
                else:
                    self.fail_json(msg="Image not found")
            if self.params['disk']:
                attrs['disk'] = self.params['disk']
            if self.params['personality']:
                attrs['personality'] = self.params['personality']
            if self.params['public_ip']:
                attrs['public_ip'] = self.params['public_ip']
            if self.params['user_data']:
                attrs['user_data'] = self.params['user_data']
            if self.params['metadata']:
                attrs['metadata'] = self.params['metadata']
            if self.params['security_groups']:
                attrs['security_groups'] = self.params['security_groups']

            if not as_config:

                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                as_config = self.conn.auto_scaling.create_config(scaling_configuration_name, **attrs)

                changed = True

                self.exit_json(
                    changed=changed,
                    as_config=as_config
                )

            else:
                if self.ansible.check_mode:
                    self.exit_json(changed=False)
                self.fail_json("AS configuration already exists")

        elif self.params['state'] == 'absent':
            if as_config:
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                self.conn.auto_scaling.delete_config()
            else:
                if self.ansible.check_mode:
                    self.exit_json(changed=False)
                self.fail_json("The AS configuration doesn't exist")




def main():
    module = ASGroupModule()
    module()


if __name__ == '__main__':
    main()
