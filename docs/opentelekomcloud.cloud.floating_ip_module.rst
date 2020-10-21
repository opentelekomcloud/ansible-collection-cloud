.. _opentelekomcloud.cloud.floating_ip_module:


**********************************
opentelekomcloud.cloud.floating_ip
**********************************

**Manage floating IP**


Version added: 0.0.1

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Add, Allocate or Remove a floating IP
- Returns the floating IP parameters



Requirements
------------
The below requirements are needed on the host that executes this module.

- openstacksdk
- openstacksdk >= 0.36.0
- otcextensions
- python >= 3.6


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>api_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>How long should the socket layer wait before timing out for API calls. If this is omitted, nothing will be passed to the requests library.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>auth</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Dictionary containing auth information as needed by the cloud&#x27;s auth plugin strategy. For the default <em>password</em> plugin, this would contain <em>auth_url</em>, <em>username</em>, <em>password</em>, <em>project_name</em> and any information about domains (for example, <em>os_user_domain_name</em> or <em>os_project_domain_name</em>) if the cloud supports them. For other plugins, this param will need to contain whatever parameters that auth plugin requires. This parameter is not needed if a named cloud is provided or OpenStack OS_* environment variables are present.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>auth_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the auth plugin to use. If the cloud uses something other than password authentication, the name of the plugin should be indicated here and the contents of the <em>auth</em> parameter should be updated accordingly.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ca_cert</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A path to a CA Cert bundle that can be used as part of verifying SSL API requests.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: cacert</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>client_cert</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A path to a client certificate to use as part of the SSL transaction.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: cert</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>client_key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A path to a client key to use as part of the SSL transaction.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: key</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cloud</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Named cloud or cloud config to operate against. If <em>cloud</em> is a string, it references a named cloud config as defined in an OpenStack clouds.yaml file. Provides default values for <em>auth</em> and <em>auth_type</em>. This parameter is not needed if <em>auth</em> is provided or if OpenStack OS_* environment variables are present. If <em>cloud</em> is a dict, it contains a complete cloud configuration like would be in a section of clouds.yaml.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>fixed_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>To which fixed IP of server the floating IP address should be attached to.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>floating_ip_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A floating IP address to attach or to detach. Required only if <em>state</em> is absent. When <em>state</em> is present can be used to specify a IP address to attach.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>admin</li>
                                    <li>internal</li>
                                    <li><div style="color: blue"><b>public</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Endpoint URL type to fetch from the service catalog.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: endpoint_type</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>nat_destination</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name or id of a neutron private network that the fixed IP to attach floating IP is on</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: fixed_network, internal_network</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>network</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name or ID of a neutron external network or a nova pool name.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>purge</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>When <em>state</em> is absent, indicates whether or not to delete the floating IP completely, or only detach it from the server. Default is to detach only.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>region_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the region.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>reuse</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>When <em>state</em> is present, and <em>floating_ip_address</em> is not present, this parameter can be used to specify whether we should try to reuse a floating IP address already allocated to the project.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>server</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name or ID of the instance to which the IP address should be assigned.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                    <li>absent</li>
                        </ul>
                </td>
                <td>
                        <div>Should the resource be present or absent.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">60</div>
                </td>
                <td>
                        <div>Time to wait for an IP address to appear as attached. See wait.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>validate_certs</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Whether or not SSL API requests should be verified.</div>
                        <div>Before Ansible 2.3 this defaulted to <code>yes</code>.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: verify</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>wait</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>When attaching a floating IP address, specify whether to wait for it to appear as attached.</div>
                        <div>Must be set to <code>yes</code> for the module to return the value of the floating IP.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - The standard OpenStack environment variables, such as ``OS_USERNAME`` may be used instead of providing explicit values.
   - Auth information is driven by openstacksdk, which means that values can come from a yaml config file in /etc/ansible/openstack.yaml, /etc/openstack/clouds.yaml or ~/.config/openstack/clouds.yaml, then from standard environment variables, then finally by explicit parameters in plays. More information can be found at https://docs.openstack.org/openstacksdk/



Examples
--------

.. code-block:: yaml+jinja

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



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>floating_ip</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>changed truea</td>
                <td>
                            <div>Floating IP</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">AnsibleMapping([(&#x27;floating_ip&#x27;, AnsibleMapping([(&#x27;attached&#x27;, True), (&#x27;created_at&#x27;, &#x27;2020-10-14T16:16:35&#x27;), (&#x27;description&#x27;, &#x27;&#x27;), (&#x27;dns_domain&#x27;, &#x27;domain.com.&#x27;), (&#x27;dns_name&#x27;, &#x27;ecs-80-158-49-123&#x27;), (&#x27;fixed_ip_address&#x27;, &#x27;192.168.0.123&#x27;), (&#x27;floating_ip_address&#x27;, &#x27;80.158.49.123&#x27;), (&#x27;floating_network_id&#x27;, &#x27;0a2228f2-7f8a-45f1-8e09-9039e1d09123&#x27;), (&#x27;id&#x27;, &#x27;c1d2e3e3-7d21-49c8-a54a-1f68ebf50123&#x27;), (&#x27;network&#x27;, &#x27;0a2228f2-7f8a-45f1-8e09-9039e1d09123&#x27;), (&#x27;port&#x27;, &#x27;68a6f030-23d7-4233-b48f-a965318ae123&#x27;), (&#x27;port_id&#x27;, &#x27;68a6f030-23d7-4233-b48f-a965318ae123&#x27;), (&#x27;project_id&#x27;, &#x27;16d53a84a13b49529d2e2c3646691123&#x27;), (&#x27;properties&#x27;, AnsibleMapping([(&#x27;dns_domain&#x27;, &#x27;domain.com.&#x27;), (&#x27;dns_name&#x27;, &#x27;ecs-80-158-49-123&#x27;)])), (&#x27;revision_number&#x27;, None), (&#x27;router&#x27;, &#x27;26ca2783-dc40-4e3a-95b1-5a0756441123&#x27;), (&#x27;router_id&#x27;, &#x27;26ca2783-dc40-4e3a-95b1-5a0756441123&#x27;), (&#x27;status&#x27;, &#x27;DOWN&#x27;), (&#x27;tenant_id&#x27;, &#x27;16d53a84a13b49529d2e2c3646691123&#x27;), (&#x27;updated_at&#x27;, &#x27;2020-10-14T16:16:35&#x27;)]))])</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- OpenStack Ansible SIG, forked and changed by Tino Schreiber (@tischrei)
