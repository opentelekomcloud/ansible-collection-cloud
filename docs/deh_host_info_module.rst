.. Document meta

:orphan:

.. Anchors

.. _ansible_collections.opentelekomcloud.cloud.deh_host_info_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

opentelekomcloud.cloud.deh_host_info -- Get Dedicated host info
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `opentelekomcloud.cloud collection <https://galaxy.ansible.com/opentelekomcloud/cloud>`_.

    To install it use: :code:`ansible-galaxy collection install opentelekomcloud.cloud`.

    To use it in a playbook, specify: :code:`opentelekomcloud.cloud.deh_host_info`.

.. version_added

.. versionadded:: 0.1.2 of opentelekomcloud.cloud

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Get Dedicated host info.


.. Aliases


.. Requirements

Requirements
------------
The below requirements are needed on the host that executes this module.

- openstacksdk
- openstacksdk >= 0.36.0
- otcextensions
- python >= 3.6


.. Options

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
                    <div class="ansibleOptionAnchor" id="parameter-api_timeout"></div>
                    <b>api_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-api_timeout" title="Permalink to this option"></a>
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
                    <div class="ansibleOptionAnchor" id="parameter-auth"></div>
                    <b>auth</b>
                    <a class="ansibleOptionLink" href="#parameter-auth" title="Permalink to this option"></a>
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
                    <div class="ansibleOptionAnchor" id="parameter-auth_type"></div>
                    <b>auth_type</b>
                    <a class="ansibleOptionLink" href="#parameter-auth_type" title="Permalink to this option"></a>
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
                    <div class="ansibleOptionAnchor" id="parameter-availability_zone"></div>
                    <b>availability_zone</b>
                    <a class="ansibleOptionLink" href="#parameter-availability_zone" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Availability zone of the Dedicated host.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-ca_cert"></div>
                    <b>ca_cert</b>
                    <a class="ansibleOptionLink" href="#parameter-ca_cert" title="Permalink to this option"></a>
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
                    <div class="ansibleOptionAnchor" id="parameter-changes_since"></div>
                    <b>changes_since</b>
                    <a class="ansibleOptionLink" href="#parameter-changes_since" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Filters the response by date and timestamp when the DeH status</div>
                                            <div>changes.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-client_cert"></div>
                    <b>client_cert</b>
                    <a class="ansibleOptionLink" href="#parameter-client_cert" title="Permalink to this option"></a>
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
                    <div class="ansibleOptionAnchor" id="parameter-client_key"></div>
                    <b>client_key</b>
                    <a class="ansibleOptionLink" href="#parameter-client_key" title="Permalink to this option"></a>
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
                    <div class="ansibleOptionAnchor" id="parameter-cloud"></div>
                    <b>cloud</b>
                    <a class="ansibleOptionLink" href="#parameter-cloud" title="Permalink to this option"></a>
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
                    <div class="ansibleOptionAnchor" id="parameter-flavor"></div>
                    <b>flavor</b>
                    <a class="ansibleOptionLink" href="#parameter-flavor" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Flavor of the Dedicated host.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-host"></div>
                    <b>host</b>
                    <a class="ansibleOptionLink" href="#parameter-host" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Name or ID of the Dedicated host.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-host_type"></div>
                    <b>host_type</b>
                    <a class="ansibleOptionLink" href="#parameter-host_type" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Type of the dedicated host</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-host_type_name"></div>
                    <b>host_type_name</b>
                    <a class="ansibleOptionLink" href="#parameter-host_type_name" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Specifies the name of the host type.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-instance_uuid"></div>
                    <b>instance_uuid</b>
                    <a class="ansibleOptionLink" href="#parameter-instance_uuid" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Specifies the ID of a running VM on this Dedicated host.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-interface"></div>
                    <b>interface</b>
                    <a class="ansibleOptionLink" href="#parameter-interface" title="Permalink to this option"></a>
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
                    <div class="ansibleOptionAnchor" id="parameter-region_name"></div>
                    <b>region_name</b>
                    <a class="ansibleOptionLink" href="#parameter-region_name" title="Permalink to this option"></a>
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
                    <div class="ansibleOptionAnchor" id="parameter-released_at"></div>
                    <b>released_at</b>
                    <a class="ansibleOptionLink" href="#parameter-released_at" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Specifies the time when the DeH is released.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-status"></div>
                    <b>status</b>
                    <a class="ansibleOptionLink" href="#parameter-status" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>available</li>
                                                                                                                                                                                                <li>fault</li>
                                                                                                                                                                                                <li>released</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                            <div>Specifies the status (state) of the Dedicated Host</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-tags"></div>
                    <b>tags</b>
                    <a class="ansibleOptionLink" href="#parameter-tags" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>                                            </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Specifies the tags of the Dedicated Host</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-timeout"></div>
                    <b>timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-timeout" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">180</div>
                                    </td>
                                                                <td>
                                            <div>How long should ansible wait for the requested resource.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>
                    <b>validate_certs</b>
                    <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>
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
                    <div class="ansibleOptionAnchor" id="parameter-wait"></div>
                    <b>wait</b>
                    <a class="ansibleOptionLink" href="#parameter-wait" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                            <div>Should ansible wait until the requested resource is complete.</div>
                                                        </td>
            </tr>
                        </table>
    <br/>

.. Notes

Notes
-----

.. note::
   - The standard OpenStack environment variables, such as ``OS_USERNAME`` may be used instead of providing explicit values.
   - Auth information is driven by openstacksdk, which means that values can come from a yaml config file in /etc/ansible/openstack.yaml, /etc/openstack/clouds.yaml or ~/.config/openstack/clouds.yaml, then from standard environment variables, then finally by explicit parameters in plays. More information can be found at https://docs.openstack.org/openstacksdk/

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    # Query all DeH hosts
    - opentelekomcloud.cloud.deh_host_info:
        cloud: "{{ test_cloud }}"
      register: deh

    # Query specific Dedicated host by ID
    - opentelekomcloud.cloud.deh_host_info:
        cloud: "{{ test_cloud }}"
        host: "9b20bd80-c1aa-438c-a499-f5b5308ac123"
      register: deh

    # Query DeH hosts with flavor s2-medium
    - opentelekomcloud.cloud.deh_host_info:
        cloud: "{{ test_cloud }}"
        host_type: "s2-medium"
      register: deh

    # Query all parameters
    - opentelekomcloud.cloud.deh_host_info:
        cloud: "{{ test_cloud }}"
        availability_zone: az01
        flavor: s2.medium.8
        instance_uuid: a0c4d7d6-a2ae-4519-92d9-f0780e6f1123
        host: "9b20bd80-c1aa-438c-a499-f5b5308ac123"
        released_at: ""
        tags: [mytag, yourtag]
        host_type: "s2-medium"
        host_type_name: "s2-medium"
      register: deh





.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-deh_hosts"></div>
                    <b>deh_hosts</b>
                    <a class="ansibleOptionLink" href="#return-deh_hosts" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>changed</td>
                <td>
                                            <div>Dictionary of DeH hosts</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;allocated_at&#x27;: &#x27;2020-09-30T09:38:15Z&#x27;, &#x27;auto_placement&#x27;: &#x27;on&#x27;, &#x27;availability_zone&#x27;: &#x27;az01&#x27;, &#x27;available_memory&#x27;: 334848, &#x27;available_vcpus&#x27;: 71, &#x27;dedicated_host_ids&#x27;: None, &#x27;host_properties&#x27;: {&#x27;available_instance_capacities&#x27;: [{&#x27;flavor&#x27;: &#x27;s2.8xlarge.2&#x27;, &#x27;id&#x27;: None, &#x27;location&#x27;: None, &#x27;name&#x27;: None}, {&#x27;flavor&#x27;: &#x27;s2.8xlarge.1&#x27;, &#x27;id&#x27;: None, &#x27;location&#x27;: None, &#x27;name&#x27;: None}], &#x27;cores&#x27;: 12, &#x27;host_type&#x27;: &#x27;s2-medium&#x27;, &#x27;host_type_name&#x27;: &#x27;s2-medium&#x27;, &#x27;id&#x27;: None, &#x27;location&#x27;: None, &#x27;memory&#x27;: 335872, &#x27;name&#x27;: None, &#x27;sockets&#x27;: 2, &#x27;vcpus&#x27;: 72}, &#x27;host_type&#x27;: None, &#x27;id&#x27;: &#x27;9b20bd80-c1aa-438c-a499-f5b5308ac123&#x27;, &#x27;instance_total&#x27;: 1, &#x27;instance_uuids&#x27;: [&#x27;a0c4d7d6-a2ae-4519-92d9-f0780e6f1123&#x27;], &#x27;name&#x27;: &#x27;deh-name&#x27;, &#x27;project_id&#x27;: &#x27;16d53a84a13b49529d2e2c3646691123&#x27;, &#x27;quantity&#x27;: None, &#x27;released_at&#x27;: &#x27;&#x27;, &#x27;state&#x27;: &#x27;available&#x27;, &#x27;tags&#x27;: [{&#x27;mytag&#x27;: &#x27;myvalue&#x27;, &#x27;yourtag&#x27;: &#x27;yourvalue&#x27;}]}]</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>

..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Tino Schreiber (@tischrei)



.. Parsing errors

