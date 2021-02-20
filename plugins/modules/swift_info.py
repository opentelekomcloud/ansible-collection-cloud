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
if container and object:
swift:
  description: List of dictionaries describing object content.
  type: complex
  returned: On Success.
  contains:
    content:
      description: Object content.
      type: str
      sample: "test\n"

if container:
swift:
  description: List of dictionaries describing objects in container.
  type: complex
  returned: On Success.
  contains:
    objects:
      type: list
      elements: dict
        name:
          description: Name of the object.
          type: str
        content_type:
          description: Content type of the object.
          type: str
        _bytes:
          description: Total number of bytes that are stored in OBS for the
            object.
          type: int
        _hash:
          description: MD5 checksum value of the object content.
          type: str
          sample: "e1cbb0c3879af8347246f12c559a86b5"
        accept_ranges:
          description: Type of ranges that the object accepts.
          type: str
        etag:
          description: For ordinary objects, this value is
            the MD5 checksum of the object content.
            For manifest objects, this value is the MD5 checksum of the
            concatenated string of MD5 checksums for each of the segments in
            the manifest.
          type: str
          sample: "e1cbb0c3879af8347246f12c559a86b5"
        last_modified_at:
          description: Modification time and date
          type: str
          sample: "2021-02-18T13:40:09.640760"
        timestamp:
          description: Creation time and date
          type: str
          sample: "2021-02-18T13:40:09.640760"

swift:
  description: List of dictionaries describing containers.
  type: complex
  returned: On Success.
  contains:
    containers:
      type: list
      elements: dict
        bytes:
          description: Total number of bytes that are stored in OBS for the
            object.
          type: int
        content_type:
          description: Content type of the object.
          type: str
        count:
          description: Count of objects in container
          type: int
        name:
          description: Name of the container
          type: str
        timestamp:
          description: Creation time and date
          type: str
          sample: "2021-02-18T13:40:09.640760"
'''

EXAMPLES = '''
# Get swift containers/objects/object content.
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
            content = self.conn.object_store.download_object(object_name, container)
            self.exit(changed=False, swift=dict(content=content))

        if container:
            objects = []
            for raw in self.conn.object_store.objects(container):
                dt = raw.to_dict()
                dt.pop('location')
                objects.append(dt)
            self.exit(changed=False, swift=dict(objects=objects))

        containers = []
        for raw in self.conn.object_store.containers():
            dt = raw.to_dict()
            dt.pop('location')
            containers.append(dt)
        self.exit(changed=False, swift=dict(containers=containers))


def main():
    module = SwiftInfoModule()
    module()


if __name__ == '__main__':
    main()
