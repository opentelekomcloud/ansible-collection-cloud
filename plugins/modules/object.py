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
module: object
short_description: Manage Swift.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.0"
author: "Polina Gubina(@Polina-Gubina)"
description:
  - Create/Delete/Fetch Swift containers and container object from the OTC.
options:
  container:
    description: Name of container in Swift.
    type: str
    required: true
  object:
    description: Name of object in Swift.
    type: str
    required: false
  content:
    description: Content to upload, can be filepath or variable.
    type: str
    required: false
  dest:
    description: The destination file path when downloading an object with a 'fetch' operation.
    type: path
    required: false
  delete_with_all_objects:
    description: 
        - Whether the container should be deleted with all objects or not.
        - Without this parameter set to "true", an attempt to delete a container that contains objects will fail.
    type: bool
    default: False
    required: false
  metadata:
    description:
    type: dict
    required: false
  keys:
    description: Keys from 'metadata' to be deleted. Used with mode='delete-metadata'.
    type: list
    required: false
  mode:
    description: Switches the module behaviour.
    required: true
    choices: ['create', 'delete', 'fetch', 'upload', 'set-metadata', 'delete-metadata']
    type: str
  overwrite:
    description:
      - Whether object should be overwritten or not in case it is already exists.
    type: bool
    default: False
    required: false
  ignore_nonexistent_container:
    description: Whether container should be created or not in case it doesn't exist, but object is set.
    type: bool
    default: False
    required: false
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
container:
  description: Specifies the container.
  type: dict
  sample: 
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
objects:
  description: Specifies the list of objects in container.
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
      "id": "object",
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
'''

EXAMPLES = '''
#

'''

import os
from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class SwiftModule(OTCModule):
    argument_spec = dict(
        container=dict(type='str', required=True),
        object=dict(type='str', required=False),
        content=dict(type='str', required=False),
        dest=dict(type='path', required=False),
        metadata=dict(type='dict', required=False),
        keys=dict(type='list', required=False),
        mode=dict(type='str', required=True, choices=['create', 'delete', 'fetch', 'upload', 'set-metadata', 'delete-metadata']),
        delete_with_all_objects=dict(type='bool', default=False, required=False),
        overwrite=dict(type='bool', default=False, required=False),
        ignore_nonexistent_container=dict(type='bool', default=False, required=False)
    )

    def create(self, container, object):

        content = self.params['content']
        data = {}
        changed = False
        if not object:
            if not self._container_exist(container):
                container_data = self.conn.object_store.create_container(name=container).to_dict()
                container_data.pop('location')
                data['container'] = container_data
                changed = True
                self.exit_json(changed=changed, **data)
            else:
                changed = False
                self.exit_json(changed=changed)

        if not self._container_exist(container):
            if self.params['ignore_nonexistent_container']:
                container_data = self.conn.object_store.create_container(name=container).to_dict()
                container_data.pop('location')
                data['container'] = container_data
            else:
                self.fail_json("Container doesn't exist")

        if self._object_exist(object, container):
            if self.params['overwrite']:
                self.conn.object_store.delete_object(obj=object, container=container)
            else:
                self.fail_json(msg="Object already exists")
        if os.path.isfile(content):
            with open(content) as file:
                content = file.read()
        raw = self.conn.object_store.create_object(
            container=container,
            name=object,
            data=content
        )
        object_data = raw.to_dict()
        object_data.pop('location')
        object_data['content'] = content
        data['object'] = object_data
        changed = True
        self.exit(changed=changed, **data)

    def set_metadata(self, container, object):

        metadata = self.params["metadata"]
        changed = False
        data = {}
        if not object:
            if self._container_exist(container):
                new_container = self.conn.object_store.set_container_metadata(container, **metadata).to_dict()
                new_container.pop('location')
                data['container'] = new_container
                changed = True
                self.exit(changed=changed, **data)
            else:
                self.fail_json(msg="Container doesn't exist")

        if self._object_exist(object, container):
            new_object = self.conn.object_store.set_object_metadata(object, container, **metadata).to_dict()
            new_object.pop('location')
            data['object'] = new_object
            changed = True
        else:
            self.fail_json(msg="Object doesn't exist")

        self.exit(changed=changed, **data)

    def delete_metadata(self, container, object):
        keys = self.params["keys"]
        changed = False
        if not object:
            if self._container_exist(container):
                self.conn.object_store.delete_container_metadata(container=container, keys=keys)
                changed = True
                self.exit(changed=changed)
            else:
                self.fail_json(msg="Container doesn't exist")

        if self._object_exist(object, container):
            self.conn.object_store.delete_object_metadata(obj=object, container=container, keys=keys)
            changed = True
        else:
            self.fail_json(msg="Object doesn't exist")

        self.exit(changed=changed)

    def _container_exist(self, container):
        try:
            self.conn.object_store.get_container_metadata(container)
            return True
        except self.sdk.exceptions.ResourceNotFound:
            return False

    def _object_exist(self, object, container):
        try:
            self.conn.object_store.get_object_metadata(object, container)
            return True
        except self.sdk.exceptions.ResourceNotFound:
            return False

    def delete(self, container, object):

        if not object:

            if self._container_exist(container):
                objects = []
                for raw in self.conn.object_store.objects(container):
                    dt = raw.to_dict()
                    dt.pop('location')
                    objects.append(dt)
                if len(objects) > 0:
                    if self.params['delete_with_all_objects']:
                        for obj in objects:
                            self.conn.object_store.delete_object(container=container, obj=obj['id'])
                    else:
                        self.fail_json(msg="Container has objects")

                self.conn.object_store.delete_container(container=container)
                changed = True
            else:
                changed = False

            self.exit(changed=changed)

        try:
            self.conn.object_store.delete_object(container=container, obj=object)
            changed = True
        except self.sdk.exceptions.ResourceNotFound:
            changed = False
        self.exit(changed=changed)

    def fetch(self, container, object):

        dest = self.params['dest']
        changed = False

        if self._object_exist(object, container):

            content = self.conn.object_store.download_object(object, container)
            changed = True

            if dest:
                with open(dest, 'wb+') as f:
                    f.write(content)
                self.exit(changed=changed)
            else:
                data = content
                self.exit(changed=changed, data=data)

        else:
            self.fail_exit(msg="This object doesn't exist")

    def run(self):
        container = self.params['container']
        object = self.params['object']
        mode = self.params['mode']

        if mode == 'create':
            self.create(container, object)
        if mode == 'delete':
            self.delete(container, object)
        if mode == 'fetch':
            self.fetch(container, object)
        if mode == 'set-metadata':
            self.set_metadata(container, object)
        if mode == 'delete-metadata':
            self.delete_metadata(container, object)


def main():
    module = SwiftModule()
    module()


if __name__ == '__main__':
    main()
