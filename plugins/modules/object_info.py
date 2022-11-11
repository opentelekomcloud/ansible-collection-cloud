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
module: object_info
short_description: Get Swift info.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.0"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Get Swift containers,
    container object, object metadata info from the OTC.
options:
  container:
    description: Name of container in Swift.
    type: str
  object_name:
    description: Name of object in Swift.
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
swift:
  description: List of dictionaries describing containers, objects
    and object metadata in container.
  type: complex
  returned: On Success.
  contains:
    containers:
      description: Specifies the list of available containers.
        Shows when no params passed.
      type: list
      sample: [
        {
          "bytes": 5449,
          "bytes_used": 5449,
          "content_type": null,
          "count": 1,
          "id": "otc",
          "if_none_match": null,
          "is_content_type_detected": null,
          "is_newest": null,
          "meta_temp_url_key": null,
          "meta_temp_url_key_2": null,
          "name": "otc",
          "object_count": 1,
          "read_ACL": null,
          "sync_key": null,
          "sync_to": null,
          "timestamp": null,
          "versions_location": null,
          "write_ACL": null
        }
      ]
    objects:
      description: Specifies the list of objects in container.
        Shows when container param is not Null
      type: list
      sample: [
        {
          "_bytes": 273,
          "_content_type": "text/plain",
          "_hash": "58c6362a0e013dae97594abe7b06d801",
          "_last_modified": "2021-02-18T14:23:55.259610",
          "accept_ranges": null,
          "content_disposition": null,
          "content_encoding": null,
          "content_length": 273,
          "content_type": "text/plain",
          "copy_from": null,
          "delete_after": null,
          "delete_at": null,
          "etag": "58c6362a0e013dae97594abe7b06d801",
          "expires_at": null,
          "id": "my.txt",
          "last_modified_at": "2021-02-18T14:23:55.259610",
          "multipart_manifest": null,
          "name": "my.txt",
          "object_manifest": null,
          "range": null,
          "signature": null,
          "timestamp": null,
          "transfer_encoding": null
        }
      ]
    metadata:
      description: Specifies the object metadata.
        Shows when container and object_name params is not Null
      type: dict
      sample: {
        "_bytes": null,
        "_content_type": null,
        "_hash": null,
        "_last_modified": null,
        "accept_ranges": "bytes",
        "container": "test",
        "content_disposition": null,
        "content_encoding": null,
        "content_length": 5,
        "content_type": "text/plain",
        "copy_from": null,
        "delete_after": null,
        "delete_at": null,
        "etag": "e1cbb0c3879af8347246f12c559a86b5",
        "expires_at": null,
        "id": "my2.txt",
        "if_match": null,
        "if_modified_since": null,
        "if_none_match": null,
        "if_unmodified_since": null,
        "is_content_type_detected": null,
        "is_newest": null,
        "is_static_large_object": null,
        "last_modified_at": "Thu, 18 Feb 2021 13:40:09 GMT",
        "multipart_manifest": null,
        "name": null,
        "object_manifest": null,
        "range": null,
        "signature": null,
        "timestamp": "1613655609.64076",
        "transfer_encoding": null
      }
'''

EXAMPLES = '''
# Get swift containers/objects/object content.
- opentelekomcloud.cloud.object_info:
  register: sw

- opentelekomcloud.cloud.object_info:
    container: my_container
  register: sw

- opentelekomcloud.cloud.object_info:
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

    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        container = self.params['container']
        object_name = self.params['object_name']
        if container and object_name:
            metadata = self.conn.object_store.get_object(object_name, container)
            metadata.pop('location')
            self.exit(changed=False, swift=dict(metadata=metadata))

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
