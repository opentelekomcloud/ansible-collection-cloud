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
module: lb_healthmonitor_info
short_description: Get health checks info from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Get Enhanced Load Balancer health checks from the OTC.
options:
  name:
    description:
      - Optional name or id of the health check
    type: str
  delay:
    description:
      - Optional the interval between health checks in the unit of second.
    type: int
  max_retries:
    description:
      - Optional the number of consecutive health checks when the health check
        result of a backend server changes from fail to success.
    type: int
  admin_state_up:
    description:
      - Optional the administrative status of the health check.
    type: bool
  monitor_timeout:
    description:
      - Optional the health check timeout duration in the unit of second.
    type: int
  type:
    description:
      - Optional health check protocol
    choices: [tcp, udp_connect, http]
    type: str
  monitor_port:
    description:
      - Optional health check port
    type: int
  expected_codes:
    description:
      - Optional health check expected HTTP status code
    type: str
  domain_name:
    description:
      - Optional health domain name of the HTTP request during the health check
    type: str
  url_path:
    description:
      - Optional HTTP request path for the health check
    type: str
  http_method:
    description:
      - Optional health check HTTP request method
    choices: [get, head, post, put, delete, trace, options, connect, patch]
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
healthmonitors:
  description: Dictionary describing members.
  type: complex
  returned: On Success.
  contains:
    id:
      description: Specifies the health check ID.
      type: str
      sample: "39007a7e-ee4f-4d13-8283-b4da2e037c69"
    name:
      description: Specifies the health check name.
      type: str
      sample: "bs_test"
    delay:
      description: Specifies the interval between health checks in the unit of second.
      type: int
    max_retries:
      description: Specifies the number of consecutive health checks when
        the health check result of a backend server changes from fail to success.
      type: int
    pools:
      description: Lists the IDs of backend server groups associated with the health check.
      type: list
    admin_state_up:
      description: Specifies the administrative status of the health check.
      type: bool
    timeout:
      description: Specifies the health check timeout duration in the unit of second.
      type: int
    type:
      description: Specifies the health check protocol.
      type: str
      sample: TCP
    monitor_port:
      description: Specifies the health check port.
      type: int
    expected_codes:
      description: Specifies the expected HTTP status code.
      type: str
    domain_name:
      description: Specifies the domain name of the HTTP request during the health check.
      type: str
    url_path:
      description: Specifies the HTTP request path for the health check.
      type: str
      sample: /test
    http_method:
      description: Specifies the HTTP request method.
      type: str
      sample: GET
    healthmonitors_links:
      description: Provides links to the previous or next page during pagination query, respectively.
      type: list
'''

EXAMPLES = '''
# Get a lb health monitor info.
- lb_healthmonitor_info:
    name: hm-test
  register: healthmonitor
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LoadBalancerHealthMonitorInfoModule(OTCModule):
    argument_spec = dict(
        name=dict(required=False),
        delay=dict(required=False, type='int'),
        max_retries=dict(required=False, type='int'),
        admin_state_up=dict(required=False, type='bool'),
        monitor_timeout=dict(required=False, type='int'),
        type=dict(required=False, choices=['tcp', 'udp_connect', 'http']),
        monitor_port=dict(required=False, type='int'),
        expected_codes=dict(required=False, type='str'),
        domain_name=dict(required=False, type='str'),
        url_path=dict(required=False, type='str'),
        http_method=dict(required=False, choices=['get', 'head', 'post', 'put', 'delete',
                                                  'trace', 'options', 'connect', 'patch'])
    )

    def run(self):
        name_filter = self.params['name']
        delay_filter = self.params['delay']
        max_retries_filter = self.params['max_retries']
        admin_state_filter = self.params['admin_state_up']
        timeout_filter = self.params['monitor_timeout']
        type_filter = self.params['type']
        monitor_port_filter = self.params['monitor_port']
        expected_codes_filter = self.params['expected_codes']
        domain_name_filter = self.params['domain_name']
        http_method_filter = self.params['http_method']

        data = []
        args = {}
        if name_filter:
            args['name'] = name_filter
        if delay_filter:
            args['delay'] = delay_filter
        if max_retries_filter:
            args['max_retries'] = max_retries_filter
        if admin_state_filter:
            args['admin_state_up'] = admin_state_filter
        if timeout_filter:
            args['timeout'] = timeout_filter
        if type_filter:
            args['type'] = type_filter.upper()
        if monitor_port_filter:
            args['monitor_port'] = monitor_port_filter
        if expected_codes_filter:
            args['expected_codes'] = expected_codes_filter
        if domain_name_filter:
            args['domain_name'] = domain_name_filter
        if http_method_filter:
            args['http_method'] = http_method_filter.upper()

        if name_filter:
            raw = self.conn.network.find_health_monitor(name_or_id=name_filter)
            dt = raw.to_dict()
            dt.pop('location')
            data.append(dt)
        else:
            for raw in self.conn.network.health_monitors(**args):
                dt = raw.to_dict()
                dt.pop('location')
                data.append(dt)

        self.exit_json(
            changed=False,
            healthmonitors=data
        )


def main():
    module = LoadBalancerHealthMonitorInfoModule()
    module()


if __name__ == '__main__':
    main()
