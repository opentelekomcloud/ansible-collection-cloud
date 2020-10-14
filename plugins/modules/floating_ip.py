#!/usr/bin/python

# forked by @tischrei
# Copyright: (c) 2015, Hewlett-Packard Development Company, L.P.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = '''
---
module: floating_ip
author: "OpenStack Ansible SIG, forked and changed by Tino Schreiber (@tischrei)"
short_description: Manage floating IP
extends_documentation_fragment: opentelekomcloud.cloud.otc
version_added: "0.0.1"
description:
   - Add, Allocate or Remove a floating IP
   - Returns the floating IP parameters
options:
   server:
     description:
        - The name or ID of the instance to which the IP address
          should be assigned.
     type: str
   network:
     description:
        - The name or ID of a neutron external network or a nova pool name.
     type: str
   floating_ip_address:
     description:
        - A floating IP address to attach or to detach. Required only if I(state)
          is absent. When I(state) is present can be used to specify a IP address
          to attach.
     type: str
   reuse:
     description:
        - When I(state) is present, and I(floating_ip_address) is not present,
          this parameter can be used to specify whether we should try to reuse
          a floating IP address already allocated to the project.
     type: bool
     default: 'no'
   fixed_address:
     description:
        - To which fixed IP of server the floating IP address should be
          attached to.
     type: str
   nat_destination:
     description:
        - The name or id of a neutron private network that the fixed IP to
          attach floating IP is on
     aliases: ["fixed_network", "internal_network"]
     type: str
   wait:
     description:
        - When attaching a floating IP address, specify whether to wait for it to appear as attached.
        - Must be set to C(yes) for the module to return the value of the floating IP.
     type: bool
     default: 'no'
   timeout:
     description:
        - Time to wait for an IP address to appear as attached. See wait.
     required: false
     default: 60
     type: int
   state:
     description:
       - Should the resource be present or absent.
     choices: [present, absent]
     default: present
     type: str
   purge:
     description:
        - When I(state) is absent, indicates whether or not to delete the floating
          IP completely, or only detach it from the server. Default is to detach only.
     type: bool
     default: 'no'

requirements: ["openstacksdk", "otcextensions"]
'''

RETURN = '''
floating_ip:
    description: Floating IP
    returned: changed truea
    type: dict
    sample: {
        floating_ip: {
            "attached": true,
            "created_at": "2020-10-14T16:16:35",
            "description": "",
            "dns_domain": "domain.com.",
            "dns_name": "ecs-80-158-49-123",
            "fixed_ip_address": "192.168.0.123",
            "floating_ip_address": "80.158.49.123",
            "floating_network_id": "0a2228f2-7f8a-45f1-8e09-9039e1d09123",
            "id": "c1d2e3e3-7d21-49c8-a54a-1f68ebf50123",
            "network": "0a2228f2-7f8a-45f1-8e09-9039e1d09123",
            "port": "68a6f030-23d7-4233-b48f-a965318ae123",
            "port_id": "68a6f030-23d7-4233-b48f-a965318ae123",
            "project_id": "16d53a84a13b49529d2e2c3646691123",
            "properties": {
                "dns_domain": "domain.com.",
                "dns_name": "ecs-80-158-49-123"
            },
            "revision_number": null,
            "router": "26ca2783-dc40-4e3a-95b1-5a0756441123",
            "router_id": "26ca2783-dc40-4e3a-95b1-5a0756441123",
            "status": "DOWN",
            "tenant_id": "16d53a84a13b49529d2e2c3646691123",
            "updated_at": "2020-10-14T16:16:35"
        }
    }
'''

EXAMPLES = '''
# Allocate floating IP without attaching it to any resource
- opentelekomcloud.cloud.floating_ip:
    cloud: "{{ test_cloud }}"
    network: admin_external_net
    server: ecs-tino-test
  register: fip

# Assign a floating IP to the first interface of `cattle001` from an existing
# external network or nova pool. A new floating IP from the first available
# external network is allocated to the project.
- opentelekomcloud.cloud.floating_ip:
     cloud: dguerri
     server: cattle001

# Assign a new floating IP to the instance fixed ip `192.0.2.3` of
# `cattle001`. If a free floating IP is already allocated to the project, it is
# reused; if not, a new one is created.
- opentelekomcloud.cloud.floating_ip:
     cloud: dguerri
     state: present
     reuse: yes
     server: cattle001
     network: ext_net
     fixed_address: 192.0.2.3
     wait: true
     timeout: 180

# Assign a new floating IP from the network `ext_net` to the instance fixed
# ip in network `private_net` of `cattle001`.
- opentelekomcloud.cloud.floating_ip:
     cloud: dguerri
     state: present
     server: cattle001
     network: ext_net
     nat_destination: private_net
     wait: true
     timeout: 180

# Detach a floating IP address from a server
- opentelekomcloud.cloud.floating_ip:
     cloud: dguerri
     state: absent
     floating_ip_address: 203.0.113.2
     server: cattle001
'''

from ansible_collections.opentelekomcloud.cloud.plugins.module_utils.otc import OTCModule


def _get_floating_ip(cloud, floating_ip_address):
    f_ips = cloud.search_floating_ips(
        filters={'floating_ip_address': floating_ip_address})
    if not f_ips:
        return None

    return f_ips[0]


class FloatingIpModule(OTCModule):
    argument_spec = dict(
        server=dict(required=False),
        state=dict(default='present', choices=['absent', 'present']),
        network=dict(required=False, default=None),
        floating_ip_address=dict(required=False, default=None),
        reuse=dict(required=False, type='bool', default=False),
        fixed_address=dict(required=False, default=None),
        nat_destination=dict(required=False, default=None,
                             aliases=['fixed_network', 'internal_network']),
        wait=dict(required=False, type='bool', default=False),
        timeout=dict(required=False, type='int', default=60),
        purge=dict(required=False, type='bool', default=False),
    )

    def _system_state_change(self, obj):
        state = self.params['state']
        if state == 'present':
            if not obj:
                return True
        elif state == 'absent' and obj:
            return True
        return False

    def run(self):
        server_name_or_id = self.params['server']
        state = self.params['state']
        network = self.params['network']
        floating_ip_address = self.params['floating_ip_address']
        reuse = self.params['reuse']
        fixed_address = self.params['fixed_address']
        nat_destination = self.params['nat_destination']
        wait = self.params['wait']
        timeout = self.params['timeout']
        purge = self.params['purge']

        cloud = self.conn
        sdk = self.sdk

        if state == 'present':
            changed = False

            if not network and not server_name_or_id:
                self.fail_json(
                    msg="Either server and/or network are required")

            # Allocate floating IP without attaching it to any resource
            if self.params['network'] and not self.params['server']:
                nw = cloud.network.find_network(network, ignore_missing=True)
                if nw:
                    fip = cloud.network.create_ip(
                        floating_network_id=nw.id
                    )
                    self.exit_json(changed=True, floating_ip=fip)
                else:
                    self.fail_json(
                        msg="network {0} not found".format(network)
                    )

            # default way of attaching floating ip
            if self.params['server']:
                server = cloud.get_server(server_name_or_id)
                if server is None:
                    self.fail_json(
                        msg="server {0} not found".format(server_name_or_id)
                    )
                # If f_ip already assigned to server, check that it matches
                # requirements.

                public_ip = cloud.get_server_public_ip(server)
                f_ip = _get_floating_ip(cloud, public_ip) if public_ip else public_ip
                if f_ip:
                    if network:
                        network_id = cloud.get_network(name_or_id=network)["id"]
                    else:
                        network_id = None
                    # check if we have floating ip on given nat_destination network
                    if nat_destination:
                        nat_floating_addrs = [
                            addr for addr in server.addresses.get(
                                cloud.get_network(nat_destination)['name'], [])
                            if addr['addr'] == public_ip
                            and addr['OS-EXT-IPS:type'] == 'floating'
                        ]

                        if len(nat_floating_addrs) == 0:
                            self.fail_json(msg="server {server} already has a "
                                           "floating-ip on a different "
                                           "nat-destination than '{nat_destination}'"
                                           .format(server=server_name_or_id,
                                                   nat_destination=nat_destination))

                    if all([fixed_address, f_ip.fixed_ip_address == fixed_address,
                            network, f_ip.network != network_id]):
                        # Current state definitely conflicts with requirements
                        self.fail_json(msg="server {server} already has a "
                                       "floating-ip on requested "
                                       "interface but it doesn't match "
                                       "requested network {network}: {fip}"
                                       .format(server=server_name_or_id,
                                               network=network,
                                               fip=f_ip))
                    if not network or f_ip.network == network_id:
                        # Requirements are met
                        self.exit_json(changed=False, floating_ip=f_ip)

                    # Requirements are vague enough to ignore existing f_ip and try
                    # to create a new f_ip to the server.

                server = cloud.add_ips_to_server(
                    server=server, ips=floating_ip_address, ip_pool=network,
                    reuse=reuse, fixed_address=fixed_address, wait=wait,
                    timeout=timeout, nat_destination=nat_destination)
                fip_address = cloud.get_server_public_ip(server)
                # Update the floating IP status
                f_ip = _get_floating_ip(cloud, fip_address)
                self.exit_json(changed=True, floating_ip=f_ip)
            self.exit_json(changed=changed)

        elif state == 'absent':

            # Release floating ip
            if floating_ip_address and not server_name_or_id:
                f_ip = _get_floating_ip(cloud, floating_ip_address)

                if not f_ip:
                    # Nothing to detach
                    self.exit_json(changed=False)
                if purge:
                    cloud.delete_floating_ip(f_ip['id'])
                    self.exit_json(changed=True)

            if floating_ip_address is None:
                if not server_name_or_id:
                    self.fail_json(msg="either server or floating_ip_address are required")
                server = cloud.get_server(server_name_or_id)
                floating_ip_address = cloud.get_server_public_ip(server)

            f_ip = _get_floating_ip(cloud, floating_ip_address)

            if not f_ip:
                # Nothing to detach
                self.exit_json(changed=False)
            changed = False
            if f_ip["fixed_ip_address"]:
                cloud.detach_ip_from_server(
                    server_id=server['id'], floating_ip_id=f_ip['id'])
                # Update the floating IP status
                f_ip = cloud.get_floating_ip(id=f_ip['id'])
                changed = True
            if purge:
                cloud.delete_floating_ip(f_ip['id'])
                self.exit_json(changed=True)
            self.exit_json(changed=changed, floating_ip=f_ip)


def main():
    module = FloatingIpModule()
    module()


if __name__ == "__main__":
    main()
