#!/usr/bin/python
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = '''
module: dds_datastore_info
short_description: Obtain database version information about a specified type of a DB instance.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.9.0"
author: "Yustina Kvrivishvili (@YustinaKvr)"
description:
  - Get datastore info
options:
  datastore_name:
    description:
      - Specifies the database type. DDS Community Edition is supported.
    type: str
    required: true
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
datastores:
    description: Info about datastore
    returned: On Success
    type: complex
    contains:
        datastore_name:
            description: Specifies the database type.
            type: str
        storage_engine:
            description: Storage engine.
            type: str
        type:
            description: Datastore type.
            type: str
        version:
            description: Datastore version.
            type: str
'''

EXAMPLES = '''
# Get info about datastore
- opentelekomcloud.cloud.dds_datastore_info:
    datastore_name: "test_ds"
  register: result
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DDSDatastoreInfo(OTCModule):
    argument_spec = dict(
        datastore_name=dict(required=True)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        datastore_name = self.params['datastore_name']

        data = []
        for raw in self.conn.dds.datastores(datastore_name):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

            self.exit(
                changed=False,
                dns_recordset=data
            )


def main():
    module = DDSDatastoreInfo()
    module()


if __name__ == '__main__':
    main()
