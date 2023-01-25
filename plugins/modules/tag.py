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
module: tag
short_description: Manage tags on diverse OpenStack/OTC resources
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
author: Artem Goncharov (@gtema)
description:
    - set or delete tags on the OpenStack/OTC resources
options:
   server:
      description:
        - Name or id of the Nova Server resource.
      type: str
   floating_ip:
      description:
        - Name or id of the Floating IP resource.
      type: str
   network:
      description:
        - Name or id of the Neutron Network resource.
      type: str
   port:
      description:
        - Name or id of the Neutron Port resource.
      type: str
   router:
      description:
        - Name or id of the Neutron Router resource.
      type: str
   security_group:
      description:
        - Name or id of the Neutron SecurityGroup resource.
      type: str
   security_group_rule:
      description:
        - Name or id of the Neutron SecurityGroupRule resource.
      type: str
   subnet:
      description:
        - Name or id of the Neutron Subnet resource.
      type: str
   trunk:
      description:
        - Name or id of the Neutron Trunk resource.
      type: str
   state:
     description:
       - Should the resource be present or absent.
     choices: [ present, absent ]
     default: present
     type: str
   tags:
     description:
       - List of tags
     default: []
     type: list
     elements: str
   mode:
     description:
       - Mode to be used for tags presence ('replace' or 'set'). 'replace'
         will replace all existing tags, while 'set' only ensures given tags
         are present.
     choices: [replace, set]
     default: replace
     type: str
notes:
    - One and only one of C(server), C(floating_ip), C(network), C(port),
      C(router), C(security_group), C(security_group_rule), C(subnet),
      C(trunk) should be set.
requirements:
    - "python >= 2.7"
    - "openstacksdk"
    - "otcextensions"
'''
EXAMPLES = '''
---
- name: replace all tags with a single tag on a server
  opentelekomcloud.cloud.tag:
    server: "{{ server_name }}"
    state: present
    tags:
        - new_tag
    mode: replace

- name: replace all tags with a single tag on a network
  opentelekomcloud.cloud.tag:
    network: "{{ network_name }}"
    state: present
    tags:
        - new_tag
    mode: replace

- name: append tags on instance
  opentelekomcloud.cloud.tag:
    server: "{{ server_name }}"
    state: present
    mode: set
    tags:
        - new_tag1
        - new_tag2

- name: remove all tags
  opentelekomcloud.cloud.tag:
    server: "{{ server_name }}"
    state: present
    tags:

- name: remove only given tags
  opentelekomcloud.cloud.tag:
    server: "{{ server_name }}"
    state: present
    tags:
      - new_tag1
'''

RETURN = '''
tags:
    description: Present tags on the instance.
    returned: success
    type: list
    sample: ["tag1", "tag2"]
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


class TagModule(OTCModule):

    argument_spec = dict(
        server=dict(default=None),
        floating_ip=dict(default=None),
        network=dict(default=None),
        port=dict(default=None),
        router=dict(default=None),
        security_group_rule=dict(default=None),
        security_group=dict(default=None),
        subnet=dict(default=None),
        trunk=dict(default=None),
        state=dict(default='present', choices=['absent', 'present']),
        tags=dict(default=[], elements='str', type='list'),
        mode=dict(default='replace', choices=['replace', 'set'])
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    @staticmethod
    def _get_tags_url(url_prefix, instance):
        """Construct direct REST query URL for tags"""
        return (
            '%(url_prefix)s/%(instance)s/tags'
            % {'url_prefix': url_prefix, 'instance': instance.id}
        )

    @staticmethod
    def _get_tag_url(url_prefix, instance, tag):
        """Construct direct REST query URL for individual tag"""
        return (
            '%(url_prefix)s/%(instance)s/tags/%(tag)s'
            % {
                'url_prefix': url_prefix,
                'instance': instance.id,
                'tag': tag
            }
        )

    def fetch_tags(self, url_prefix, microver, instance):
        """Get current tags"""
        result = None
        try:
            inst = instance.fetch_tags(self.conn)
            result = inst.tags
        except AttributeError:
            # Try a low-level access if SDK version is old
            response = self.conn.get(
                self._get_tags_url(url_prefix, instance),
                microversion=microver)

            if response.content and response.status_code < 400:
                result = response.json()['tags']
            else:
                self.fail_json(msg='Request failed: %s' % response.reason)

        return result

    def replace_tags(self, url_prefix, microver, instance, tags):
        """Replace all tags at once"""
        result = None
        try:
            inst = instance.set_tags(self.conn, tags)
            result = inst.tags
        except AttributeError:
            # Try a low-level access if SDK version is old
            data = {'tags': tags}
            response = self.conn.put(
                self._get_tags_url(url_prefix, instance),
                json=data, microversion=microver)
            if response.content and response.status_code < 400:
                result = response.json()['tags']
            else:
                self.fail_json(
                    msg='API returned something bad %s' % response.reason)
        return result

    def set_tags(self, url_prefix, microver, instance, tags):
        """Set tag on a server one by one"""
        try:
            for tag in tags:
                instance.add_tag(self.conn, tag)
        except AttributeError:
            # Try a low-level access if SDK version is old
            for tag in tags:
                response = self.conn.put(
                    self._get_tag_url(url_prefix, instance, tag),
                    microversion=microver)
                if response.status_code not in [201, 204]:
                    self.fail_json(
                        msg='API returned something bad %s' % response.reason)
        return self.fetch_tags(url_prefix, microver, instance)

    def delete_tags(self, url_prefix, microver, instance, tags):
        """Set tag on a resource one by one"""
        try:
            for tag in tags:
                instance.remove_tag(self.conn, tag)
        except AttributeError:
            # Try a low-level access if SDK version is old
            for tag in tags:
                response = self.conn.delete(
                    self._get_tag_url(url_prefix, instance, tag),
                    microversion=microver)
                if response.status_code not in [204, 404]:
                    self.fail_json(
                        msg='API returned something bad %s' % response.reason)
        return self.fetch_tags(url_prefix, microver, instance)

    def run(self):
        server = self.params['server']
        floating_ip = self.params['floating_ip']
        network = self.params['network']
        port = self.params['port']
        router = self.params['router']
        security_group_rule = self.params['security_group_rule']
        security_group = self.params['security_group']
        subnet = self.params['subnet']
        trunk = self.params['trunk']
        state = self.params['state']
        new_tags = self.params['tags'] or []
        mode = self.params['mode']
        changed = False
        resource = None
        microver = None

        if server:
            instance = self.conn.get_server(server)
            url_prefix = '/servers'
            endpoint = self.conn.compute
            resource = server
            microver = '2.26'
        elif floating_ip:
            instance = self.conn.get_floating_ip(floating_ip)
            url_prefix = '/floatingips'
            endpoint = self.conn.network
            resource = floating_ip
        elif network:
            instance = self.conn.get_network(network)
            url_prefix = '/networks'
            endpoint = self.conn.network
            resource = network
        elif port:
            instance = self.conn.get_port(port)
            url_prefix = '/ports'
            endpoint = self.conn.network
            resource = port
        elif router:
            instance = self.conn.get_router(router)
            url_prefix = '/routers'
            endpoint = self.conn.network
            resource = router
        elif security_group_rule:
            instance = self.conn.get_security_group_rule(security_group_rule)
            url_prefix = '/security-group-rules'
            endpoint = self.conn.network
            resource = security_group_rule
        elif security_group:
            instance = self.conn.get_security_group(security_group)
            url_prefix = '/security-groups'
            endpoint = self.conn.network
            resource = security_group
        elif subnet:
            instance = self.conn.get_subnet(subnet)
            url_prefix = '/subnets'
            endpoint = self.conn.network
            resource = subnet
        elif trunk:
            instance = self.conn.get_trunk(trunk)
            url_prefix = '/trunks'
            endpoint = self.conn.network
            resource = trunk
        else:
            self.fail_json(msg='Any of the supported should be given')

        if instance:
            current_tags = self.fetch_tags(
                self, endpoint, url_prefix, microver, instance)
            if state == 'present':
                if mode == 'replace' and set(current_tags) != set(new_tags):
                    # Any of the tags mismatch
                    changed = True
                elif mode == 'set' and any(
                        x not in current_tags for x in new_tags):
                    # At least one tag should be set
                    changed = True
            elif state == 'absent' and any(
                    x in current_tags for x in new_tags):
                # At least one tag should be removed
                changed = True

            if self.ansible.check_mode or not changed:
                self.exit_json(
                    changed=changed,
                    tags=new_tags)

            if state == 'present':
                if mode == 'replace':
                    tags = self.replace_tags(
                        self, endpoint, url_prefix, microver,
                        instance, new_tags)
                elif mode == 'set':
                    tags = self.set_tags(
                        self, endpoint, url_prefix, microver,
                        instance, new_tags)
            elif state == 'absent':
                tags = self.delete_tags(
                    self, endpoint, url_prefix, microver,
                    instance, new_tags)

            self.exit_json(
                changed=changed,
                tags=tags)
        else:
            self.fail_json(msg='Instance %s can not be found' % resource)


def main():
    module = TagModule()
    module()


if __name__ == '__main__':
    main()
