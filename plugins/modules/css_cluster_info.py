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
module: cs_cluster_info
short_description: Get info about CSS clusters.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.8.1"
author: "Yustina Kvrivishvili (@YustinaKvr)"
description:
  - Get CSS cluster info from the OTC.
options:
  id:
    description:
      - ID of the cluster to be queried.
    type: str
  start:
    description:
      - Start value of the query. The default value is 1, indicating that the query starts from the\
        first cluster.
    type: int
  limit:
    description:
      - Number of clusters to be queried. The default value is 10, indicating that 10 clusters are\
        queried at a time.
    type: int
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
'''

EXAMPLES = '''
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule

class CSSClusterInfoModule(OTCModule):

		argument_spec = dict(
				id=dict(required=False),
				start=dict(required=False),
				limit=dict(required=False)
			)
		module_kwargs = dict(
				supports_check_mode=True,
				# required_if=
			)

		def run(self):

				data = []
				query = {}
				cluster = None

				if self.params['id']:
						query['id'] = self.params['id']
				if self.params['start']:
						query['start'] = self.params['id']
				if self.params['limit']:
						query['limit'] = self.params['limit']

				# for raw in self.conn.css.clusters(**query):
				# 	dt = raw.to_dict()
				# 	dt.pop('location')
				# 	data.append(dt)

				self.exit(
					changed=False,
					cluster=data
					)

def main():
		module = CSSClusterInfoModule()
		module()


if __name__ == '__main__':
		main()
