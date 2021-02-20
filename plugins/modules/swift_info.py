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
module: swift_info
short_description: Get Swift info.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.0"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Get Swift containers,
  - container object, object content info from the OTC.
options:
  container:
    description:
      - Name of container in Swift.
    type: str
  object_name:
    description:
      - Name of object in Swift.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
swift_content:
    description: List of dictionaries describing AutoScaling Configs.
    type: complex
    returned: On Success.
    contains:
'''

EXAMPLES = '''
# Get configs versions.
- swift_info:
  register: sw

- swift_info:
    container: my_container
  register: sw

- swift_info:
    container: my_container
    object_name: my_object
  register: sw
'''
from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SwiftInfoModule(OTCModule):
    argument_spec = dict(
        container=dict(type='str', required=False),
        object_name=dict(type='str', required=False),
    )

    def run(self):
        container = self.params['container']
        object_name = self.params['object_name']
        if container and object_name:
            content = self.conn.download_object(object_name, container)
            self.exit(changed=False, swift=dict(content=content))

        if container:
            objects = []
            for raw in self.conn.objects(container):
                dt = raw.to_dict()
                dt.pop('location')
                objects.append(dt)
            self.exit(changed=False, swift=dict(objects=objects))

        containers = []
        for raw in self.conn.containers():
            dt = raw.to_dict()
            dt.pop('location')
            containers.append(dt)
        self.exit(changed=False, swift=dict(containers=containers))


def main():
    module = SwiftInfoModule()
    module()


if __name__ == '__main__':
    main()
