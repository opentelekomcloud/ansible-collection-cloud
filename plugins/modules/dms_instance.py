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
module: dms_queue
short_description: Manage DMS Queues on Open Telekom Cloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.1.2"
author: "Sebastian Gode (@SebastianGode)"
description:
  - Manage DMS Queues on Open Telekom Cloud
options:
  name:
    description:
      - Name of the Queue. Can also be ID for deletion.
    type: str
    required: true
  queue_mode:
    description:
      - Indicates the queue type.
    type: str
    default: NORMAL
  description:
    description:
      - Description.
    type: str
  redrive_policy:
    description:
      - This parameter specifies whether to enable dead letter messages.
      - Dead letter messages are messages that cannot be normally consumed.
      - This parameter is valid only when queue_mode is set to NORMAL or FIFO.
    type: str
    default: disable
  max_consume_count:
    description:
      - Indicates the maximum number of allowed message consumption failures.
      - This parameter is mandatory only when redrive_policy is set to enable.
    type: int
  retention_hours:
    description:
      - Indicates the hours of storing messages in the Kafka queue.
      - This parameter is valid only when queue_mode is set to KAFKA_HA or KAFKA_HT.
    type: int
  state:
    choices: [present, absent]
    default: present
    description: Instance state
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
deh_host:
    description: Dictionary of DMS Queue
    returned: changed
    type: dict
    sample: {
        "queue": {
            "created": null,
            "description": null,
            "id": "c28ff35a-dbd4-460a-a30d-cf31a6013eb0",
            "location": {
                "cloud": "otc",
                "project": {
                    "domain_id": null,
                    "domain_name": null,
                    "id": "16d53a84a13b49529d2e2c3646691288",
                    "name": "eu-de"
                },
                "region_name": "eu-de",
                "zone": null
            },
            "max_consume_count": null,
            "name": "test-queue",
            "queue_mode": "NORMAL",
            "redrive_policy": "disable",
            "retention_hours": null
        }
    }
'''

EXAMPLES = '''
# Create Queue
- opentelekomcloud.cloud.dms_queue:
    name: 'test-queue'
    state: present

# Delete Queue
- opentelekomcloud.cloud.dms_queue:
    name: 'test-queue'
    state: absent
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DmsQueueModule(OTCModule):
    argument_spec = dict(
        name=dict(required=True),
        description=dict(required=False),
        engine=dict(required=False, default='kafka'),
        engine_version=dict(required=False, default='2.3.0'),
        storage_space=dict(required=False, type='int'),
        access_user=dict(required=False),
        password=dict(required=False),
        vpc_id=dict(required=False),
        security_group_id=dict(required=False),
        subnet_id=dict(required=False),
        product_id=dict(required=False),
        available_zones=dict(required=False, type='list'),
        maintain_begin=dict(required=False),
        maintain_end=dict(required=False),
        ssl_enable=dict(required=False, type='bool', default='False'),
        enable_publicip=dict(required=False, type='bool'),
        public_bandwidth=dict(required=False),
        retention_policy=dict(required=False),
        storage_spec_code=dict(required=False),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        attrs = {}
        instance = self.conn.dms.find_instance(name_or_id=self.params['name'], ignore_missing=True)

        if self.params['state'] == 'present':

            # Instance creation
            if not instance:
                attrs['name'] = self.params['name']
                if self.params['description']:
                    attrs['description'] = self.params['description']
                if self.params['engine']:
                    attrs['engine'] = self.params['engine']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No engine param provided')
                    )
                if self.params['engine_version']:
                    attrs['engine_version'] = self.params['engine_version']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No engine_version param provided')
                    )
                if self.params['storage_space']:
                    attrs['storage_space'] = self.params['storage_space']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No storage_space param provided')
                    )
                if self.params['access_user'] and self.params['ssl_enable'] is True:
                    attrs['access_user'] = self.params['access_user']
                elif self.params['access_user'] and self.params['ssl_enable'] is False:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('access_user specified but ssl_enable is false')
                    )
                if self.params['password'] and self.params['ssl_enable'] is True:
                    attrs['password'] = self.params['password']
                elif self.params['password'] and self.params['ssl_enable'] is False:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('Password specified but ssl_enable is false')
                    )
                if self.params['vpc_id']:
                    attrs['vpc_id'] = self.params['vpc_id']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No vpc_id param provided')
                    )
                if self.params['security_group_id']:
                    attrs['security_group_id'] = self.params['security_group_id']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No security_group_id param provided')
                    )
                if self.params['subnet_id']:
                    attrs['subnet_id'] = self.params['subnet_id']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No subnet_id param provided')
                    )
                if self.params['available_zones']:
                    attrs['available_zones'] = self.params['available_zones']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No available_zones param provided')
                    )
                if self.params['product_id']:
                    attrs['product_id'] = self.params['product_id']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No product_id param provided')
                    )
                if self.params['maintain_begin'] and self.params['maintain_end']:
                    attrs['maintain_begin'] = self.params['maintain_begin']
                    attrs['maintain_end'] = self.params['maintain_end']
                elif self.params['maintain_end'] or self.params['maintain_begin']:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('Both maintain_end and maintain_begin need to be defined.')
                    )
                if self.params['ssl_enable'] is True and self.params['password']:
                    attrs['ssl_enable'] = self.params['ssl_enable']
                elif self.params['ssl_enable'] is True and not self.params['password']:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('ssl_enable is true, but no password defined')
                    )
                if self.params['enable_publicip']:
                    attrs['enable_publicip'] = self.params['enable_publicip']
                if self.params['public_bandwidth']:
                    attrs['public_bandwidth'] = self.params['public_bandwidth']
                if self.params['retention_policy']:
                    attrs['retention_policy'] = self.params['retention_policy']
                if self.params['storage_spec_code']:
                    attrs['storage_spec_code'] = self.params['storage_spec_code']
                else:
                    self.exit(
                        changed=False,
                        failed=True,
                        message=('No storage_spec_code param provided')
                    )


                if self.ansible.check_mode:
                    self.exit(changed=True)
                #raise Exception(attrs)
                instance = self.conn.dms.create_instance(**attrs)
                self.exit(changed=True, instance=instance.to_dict())

            # Queue Modification - not possible
            elif queue:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('A Queue with this name already exists. Aborting')
                )

        if self.params['state'] == 'absent':

            # Queue Deletion
            if queue:
                if self.ansible.check_mode:
                    self.exit(changed=True)
                queue = self.conn.dms.delete_queue(queue=queue.id)
                self.exit(changed=True)

            elif not queue:
                self.exit(
                    changed=False,
                    failed=True,
                    message=('No Queue with name or ID %s found') % (self.params['name'])
                )


def main():
    module = DmsQueueModule()
    module()


if __name__ == "__main__":
    main()
