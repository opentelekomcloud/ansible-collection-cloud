opentelekomcloud.cloud.vpc_peering
==================================

Configure VPC Peering between 2 routers.

Requirements
------------

Python packages:
  - openstacksdk
  - otcextensions

Ansible collections:
  - openstack.cloud
  - opentelekomcloud.cloud

Role Variables
--------------

cloud_a: Connection to cloud A
local_router: Name or ID of the router on side A
local_project: Name or ID of the project of the side A
local_cidr: CIDR for the route
cloud_b: Connection to the cloud B
remote_router: Name or ID of the router on side B
remote_cidr: CIDR for the route

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Role is designed to work best looping over the structure of peering
definitions:
.. code-block:: yaml

   cloud_peerings:
     - cloud: "cloud_a"
       name: "peering_cloud_a_cloud_b"
       local_router: "router_a"
       local_project: "project_a"
       local_cidr: "192.168.1.0/24"
       remote_cloud: "cloud_b"
       remote_router: "router_b"
       remote_project: "project_b"
       remote_cidr: "192.168.2.0/24"

.. code-block:: yaml

   - hosts: localhost
     name: "Manage cloud VPC peerings"
     tasks:
       - name: Manage VPC Peerings
         include_role:
           name: opentelekomcloud.cloud.vpc_peering
         loop: "{{ cloud_peerings }}"
         loop_control:
           loop_var: vpcp

License
-------

Apache-2.0
