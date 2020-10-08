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
module: lb_healthmonitor
short_description:  Add//Update/Delete a health check for a backend server group in load balancer from OpenTelekomCloud
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.3"
author: "Anton Sidelnikov (@anton-sidelnikov)"
description:
  - Add or Remove a health check for a backend server group for Enhanced Load Balancer.
options:
  state:
    description:
      - Should the resource be present or absent.
    choices: [present, absent]
    default: present
    type: str
  name:
    description:
      - Specifies the health check name.
    type: str
    required: true
  delay:
    description:
      - Specifies the interval between health checks in the unit of second (1-50).
    type: int
  max_retries:
    description:
      - Specifies the number of consecutive health checks when the health check
        result of a backend server changes from fail to success (1-10).
    type: int
  pool:
    description:
      - Specifies the ID or Name of the backend server group.
    type: str
  admin_state_up:
    description:
      - Specifies the administrative status of the health check.
    type: bool
  monitor_timeout:
    description:
      - Specifies the health check timeout duration in the unit of second (1-50).
    type: int
  type:
    description:
      - Specifies the health check protocol.
    choices: [tcp, upd_connect, http]
    type: str
  monitor_port:
    description:
      - Specifies the health check port.
    type: int
  domain_name:
    description:
      - Specifies the domain name of the HTTP request during the health check.
    type: str
  url_path:
    description:
      - Specifies the HTTP request path for the health check.
    type: str
  expected_codes:
    description:
      - Specifies the expected HTTP status code.
    type: str
  http_method:
    description:
      - Specifies the HTTP request method.
    choices: [get, head, post, put, delete, trace, options, connect, patch]
    type: str
requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
lb_healthmonitor:
  description: Specifies the health check.
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
'''

EXAMPLES = '''
# Add a health check to backed server group in ELB.
- lb_healthmonitor:
    state: present
    name: member
    pool: "{{ pool_name_or_id }}"
    delay: 5
    max_retries: 3
    monitor_timeout: 15
    type: tcp

# Update a health check to backed server group in ELB.
- lb_healthmonitor:
    state: present
    name: member
    pool: "{{ pool_name_or_id }}"
    delay: 1
    max_retries: 1
    monitor_timeout: 1
    type: tcp

# Delete a server group member from load balancer.
- lb_healthmonitor:
    state: absent
    name: healthcheck
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class LoadBalancerHealthmonitorModule(OTCModule):
    argument_spec = dict(
        state=dict(default='present', choices=['absent', 'present']),
        name=dict(required=True),
        delay=dict(required=False, type='int'),
        max_retries=dict(required=False, type='int'),
        pool=dict(required=False, type='str'),
        admin_state_up=dict(required=False, type='bool'),
        monitor_timeout=dict(required=False, type='int'),
        type=dict(required=False, choices=['tcp', 'upd_connect', 'http']),
        monitor_port=dict(required=False, type='int'),
        domain_name=dict(required=False, type='str'),
        url_path=dict(required=False, type='str'),
        expected_codes=dict(required=False, type='str'),
        http_method=dict(required=False, choices=['get', 'head', 'post', 'put', 'delete',
                                                  'trace', 'options', 'connect', 'patch'])
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):
        name_filter = self.params['name']
        delay_filter = self.params['delay']
        max_retries_filter = self.params['max_retries']
        pool_filter = self.params['pool']
        admin_state_filter = self.params['admin_state_up']
        timeout_filter = self.params['monitor_timeout']
        type_filter = self.params['type']
        monitor_port_filter = self.params['monitor_port']
        domain_name_filter = self.params['domain_name']
        url_path_filter = self.params['url_path']
        expected_codes_filter = self.params['expected_codes']
        http_method_filter = self.params['http_method']

        lb_monitor = None
        attrs = {}
        changed = False
        lb_monitor = self.conn.network.find_health_monitor(name_or_id=name_filter)

        if self.params['state'] == 'present':
            if name_filter:
                attrs['name'] = name_filter
            if pool_filter:
                pool = self.conn.network.find_pool(name_or_id=pool_filter)
                if pool:
                    attrs['pool_id'] = pool.id
            if delay_filter:
                attrs['delay'] = delay_filter
            if max_retries_filter:
                attrs['max_retries'] = max_retries_filter
            if timeout_filter:
                attrs['timeout'] = timeout_filter
            if type_filter:
                attrs['type'] = type_filter.upper()
            if admin_state_filter:
                attrs['admin_state_up'] = admin_state_filter
            if monitor_port_filter:
                attrs['monitor_port'] = monitor_port_filter
            if domain_name_filter:
                attrs['domain_name'] = domain_name_filter
            if url_path_filter:
                attrs['url_path'] = url_path_filter
            if expected_codes_filter:
                attrs['expected_codes'] = expected_codes_filter
            if http_method_filter:
                attrs['http_method'] = http_method_filter.upper()

            if lb_monitor:
                changed = True
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                lb_monitor = self.conn.network.update_health_monitor(health_monitor=lb_monitor, **attrs)
                self.exit_json(
                    changed=changed,
                    member=lb_monitor.to_dict(),
                    id=lb_monitor.id
                )

            if not pool_filter and not delay_filter and not max_retries_filter\
                    and not timeout_filter and not type_filter:
                self.fail_json(msg='Pool, delay, max_retries, timeout and type must be specified.')
            if self.ansible.check_mode:
                self.exit_json(changed=True)

            lb_monitor = self.conn.network.create_health_monitor(**attrs)
            changed = True
            self.exit_json(
                changed=changed,
                member=lb_monitor.to_dict(),
                id=lb_monitor.id
            )

        elif self.params['state'] == 'absent':
            changed = False
            if lb_monitor:
                if self.ansible.check_mode:
                    self.exit_json(changed=True)
                self.conn.network.delete_health_monitor(health_monitor=lb_monitor)
                changed = True
            self.exit_json(changed=changed)


def main():
    module = LoadBalancerHealthmonitorModule()
    module()


if __name__ == '__main__':
    main()
