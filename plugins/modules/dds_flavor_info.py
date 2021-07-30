#!/usr/bin/python
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions,
# limitations under the License.

DOCUMENTATION = '''
module: dds_flavor_info
short_description: Obtain flavor type information about a specified region and DB type.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.9.0"
author: "Yustina Kvrivishvili (@YustinaKvr)"
description:
  - Get DDS flavor info
options:
  region:
    description:
      - Specifies the region where the DB instance exists.
    type: str
    required: true
  engine_name:
    description:
      - Specifies the database type. The value is DDS-Community.
    type: str
    required: false
    default: 'DDS-Community'
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
flavors:
    description: Info about flavor.
    returned: On Success
    type: complex
    contains:
        az_status:
            description: Indicates the status of specifications in an AZ.
            type: list
        engine_name:
            description: Indicates the engine name.
            type: str
        id:
            description: Datastore version.
            type: str
        name:
            description: Name of the datastore.
            type: str
        ram:
            description: Indicates the memory size in gigabyte (GB).
            type: str
        spec_code:
            description: Indicates the resource specifications code.
            type: str
        type:
            description: Indicates the node type.
            type: str
        vcpus:
            description: Number of vCPUs.
            type: str
'''

EXAMPLES = '''
# Get info about datastore
- opentelekomcloud.cloud.dds_flavor_info:
    region: "eu-de"
  register: result
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class DDSFlavorInfo(OTCModule):
    argument_spec = dict(
        region=dict(required=True),
        engine_name=dict(default='DDS-Community'),
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        region = self.params['region']
        engine_name = self.params['engine_name']

        data = []
        for raw in self.conn.dds.flavors(region=region, engine_name=engine_name):
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)

        self.exit(
            changed=False,
            flavors=data
        )


def main():
    module = DDSFlavorInfo()
    module()


if __name__ == '__main__':
    main()
