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
module: dds_database_version_info
short_description: Obtain database version information about a specified type of a DB instance.
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.3.0"
author: "Yustina Kvrivishvili (@YustinaKvr)"
description:
  - Get Metric Data
options:
  project_id:
    description:
      - Specifies the project ID of a tenant in a region.
    type: str
    required: true
  datastore_name:
    description:
      - Specifies the database type. DDS Community Edition is supported.
    type: str
    required: true
requirements: ["openstacksdk", "otcextensions"]
'''
