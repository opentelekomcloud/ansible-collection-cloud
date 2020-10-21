# ansible-collections
Ansible Collections for using with OTC (addition to the native OpenStack
modules)

* ``cloud`` - collection containing additional ansible modules for managing
  OTC specific resources (or modified OpenStack modules in case of behavioral
  differencies)

## Requirements

- otcextension
- openstacksdk (installed via otcextensions)

## Installation of the ansible collecton opentelekomcloud.cloud

.. code-block:: none

   $ ansible-galaxy collection install opentelekomcloud.cloud

## Installation on a blank system in a Python virtual environment

Installation was tested on Ubuntu 20.04

Install ``python3-venv`` for Python virtual environment:

.. code-block:: bash

   $ sudo apt-get install python3-venv

Create virtual environment ``ansiblevenv``:

.. code-block:: bash

   $ python3 -m venv ansiblevenv

Install dependencies for python package
`otcextensions <https://github.com/opentelekomcloud/python-otcextensions>`_
which are described in its
`documentation <https://python-otcextensions.readthedocs.io/en/latest/>`_:

.. code-block:: bash

   $ sudo apt-get install gcc libssl-dev python3-dev

Enable virtual environment ``ansiblevenv``:

.. code-block:: bash

   $ source ansiblevenv/bin/activate

Install ``wheel``, ``ansible`` and ``otcextensions``:

.. code-block:: bash

   (ansiblevenv) $ pip install wheel ansible otcextensions

Install opentelekomcloud.cloud collection from Ansible-Galaxy:

.. code-block:: bash

   (ansiblevenv) $ ansible-galaxy collection install opentelekomcloud.cloud

Prepare credential file ``clouds.yaml`` and necessary folders to connect to
your cloud:

.. code-block:: bash

   (ansiblevenv) $ mkdir -p .config/openstack/
   (ansiblevenv) $ touch .config/openstack/clouds.yaml
   (ansiblevenv) $ chmod 700 -R .config/
 
Paste in the following content with your credentials:

.. code-block:: bash

   # clouds.yaml
 
   clouds:
   otc:
     profile: otc
     auth:
       username: '<USER_NAME>'
       password: '<PASSWORD>'
       project_name: '<eu-de_project>'
       # or project_id: '<123456_PROJECT_ID>'
       user_domain_name: 'OTC00000000001000000xxx'
       # or user_domain_id: '<123456_DOMAIN_ID>'
       auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'
     interface: 'public'
     identity_api_version: 3 # !Important
     ak: '<AK_VALUE>' # AK/SK pair for access to OBS
     sk: '<SK_VALUE>'

Verify the installation process by creating a sample playbook which invokes
all dependencies:

.. code-block:: bash

   (ansiblevenv) $ vim opentelekomcloud.yaml
 
   # opentelekomcloud.yaml
 
   - hosts: localhost
   tasks:
     - name: Get NAT gateway info
       opentelekomcloud.cloud.nat_gateway_info:
         cloud: otc
       register: gw
 
     - name: debug configs
       debug:
         var: gw.nat_gateways

Run the playbook to verify the functionality:

.. code-block:: bash

   (ansiblevenv) $ ansible-playbook opentelekomcloud.yaml
 
   # output without NAT gateways enabled
 
   PLAY [localhost] ***************************************************************
 
   TASK [Gathering Facts] *********************************************************
   ok: [localhost]
 
   TASK [Get NAT gateway info] ****************************************************
   ok: [localhost]
 
   TASK [debug configs] ***********************************************************
   ok: [localhost] => {
       "gw.nat_gateways": []
   }


<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## Collection: opentelekomcloud.cloud

<!--start collection content-->
### Modules
Name | Description
--- | ---
[opentelekomcloud.cloud.as_config_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.as_config_info_module.rst)|Get AutoScaling configs
[opentelekomcloud.cloud.as_group_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.as_group_info_module.rst)|Get AutoScaling groups
[opentelekomcloud.cloud.cce_cluster](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.cce_cluster_module.rst)|Add/Delete CCE Cluster
[opentelekomcloud.cloud.cce_cluster_cert_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.cce_cluster_cert_info_module.rst)|Get Certificates of a CCE cluster
[opentelekomcloud.cloud.cce_cluster_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.cce_cluster_info_module.rst)|Get information about CCE clusters
[opentelekomcloud.cloud.floating_ip](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.floating_ip_module.rst)|Manage floating IP
[opentelekomcloud.cloud.lb_healthmonitor](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.lb_healthmonitor_module.rst)|Add//Update/Delete a health check for a backend server group in load balancer from OpenTelekomCloud
[opentelekomcloud.cloud.lb_healthmonitor_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.lb_healthmonitor_info_module.rst)|Get health checks info from OpenTelekomCloud
[opentelekomcloud.cloud.lb_listener](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.lb_listener_module.rst)|Add/Delete listener for load balancer from OpenTelekomCloud
[opentelekomcloud.cloud.lb_listener_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.lb_listener_info_module.rst)|Get listener info from OpenTelekomCloud
[opentelekomcloud.cloud.lb_member](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.lb_member_module.rst)|Add/Delete a member for a pool in load balancer from OpenTelekomCloud
[opentelekomcloud.cloud.lb_member_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.lb_member_info_module.rst)|Get backend server group member info from OpenTelekomCloud
[opentelekomcloud.cloud.lb_pool](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.lb_pool_module.rst)|Add/Delete backend server group for load balancer from OpenTelekomCloud
[opentelekomcloud.cloud.lb_pool_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.lb_pool_info_module.rst)|Get load balancer backend server group info from OpenTelekomCloud
[opentelekomcloud.cloud.loadbalancer](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.loadbalancer_module.rst)|Add/Delete load balancer from OpenTelekomCloud
[opentelekomcloud.cloud.loadbalancer_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.loadbalancer_info_module.rst)|Get load balancer info
[opentelekomcloud.cloud.nat_dnat_rule](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.nat_dnat_rule_module.rst)|Manage NAT DNAT rules
[opentelekomcloud.cloud.nat_dnat_rule_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.nat_dnat_rule_info_module.rst)|Get DNAT rule details
[opentelekomcloud.cloud.nat_gateway](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.nat_gateway_module.rst)|Manage NAT gateway instances
[opentelekomcloud.cloud.nat_gateway_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.nat_gateway_info_module.rst)|Get NAT gateways
[opentelekomcloud.cloud.nat_snat_rule](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.nat_snat_rule_module.rst)|Manage NAT SNAT rule instances
[opentelekomcloud.cloud.nat_snat_rule_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.nat_snat_rule_info_module.rst)|Get SNAT rule details
[opentelekomcloud.cloud.rds_backup_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.rds_backup_info_module.rst)|Get RDS Backup info
[opentelekomcloud.cloud.rds_datastore_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.rds_datastore_info_module.rst)|Get supported RDS datastore versions
[opentelekomcloud.cloud.rds_flavor_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.rds_flavor_info_module.rst)|Get RDS flavor info
[opentelekomcloud.cloud.rds_instance](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.rds_instance_module.rst)|Manage RDS instance
[opentelekomcloud.cloud.rds_instance_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.rds_instance_info_module.rst)|Get RDS Instance info
[opentelekomcloud.cloud.tag](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.tag_module.rst)|Manage tags on diverse OpenStack/OTC resources
[opentelekomcloud.cloud.volume_backup](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.volume_backup_module.rst)|Add/Delete Volume backup
[opentelekomcloud.cloud.volume_backup_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.volume_backup_info_module.rst)|Get Backups
[opentelekomcloud.cloud.volume_snapshot_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.volume_snapshot_info_module.rst)|Get information about volume snapshots
[opentelekomcloud.cloud.vpc_peering_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.vpc_peering_info_module.rst)|Get information about vpc peerings
[opentelekomcloud.cloud.waf_certificate](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.waf_certificate_module.rst)|Manage WAF certificates
[opentelekomcloud.cloud.waf_certificate_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.waf_certificate_info_module.rst)|Get WAF certificate info
[opentelekomcloud.cloud.waf_domain](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.waf_domain_module.rst)|Add/Modify/Delete WAF domain
[opentelekomcloud.cloud.waf_domain_info](http://github.com/OpenTelekomCloud/ansible_collections/blob/master/docs/opentelekomcloud.cloud.waf_domain_info_module.rst)|Get WAF domain info

<!--end collection content-->
