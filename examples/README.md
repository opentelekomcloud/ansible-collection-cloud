Open Telekom Cloud Manuals
==========================


This document contains examples of implementing OTC modules. Besides playbooks itself, we also
put here tips and tricks helping you to understand how exactly the code works.
For raw playbooks please go to [Playbooks](https://github
.com/opentelekomcloud/ansible-collection-cloud/tree/master/examples/playbooks).

https://github.com/opentelekomcloud/ansible-collection-cloud/tree/master/examples/README.md#

**Modules are used in this doc:**

* [opentelekomcloud.cloud.vpc](https://github.com/opentelekomcloud/ansible-collection-cloud/tree/master/examples/README.md#opentelekomcloudcloudvpc)
* [opentelekomcloud.cloud.subnet](https://github.com/opentelekomcloud/ansible-collection-cloud/tree/master/examples/README.md#opentelekomcloudcloudsubnet)


Initial Infrastructure
======================

Initial infrastructure contains basic resources. In most of all cases these resources are
mandatory for every kind of systems, so let's start with them.

First, we need to create ecosystem for further infrastructure. Its include network entities, such
as VPC and subnet, security group and a couple of ECSs.

opentelekomcloud.cloud.vpc
--------------------------
```yaml
   - name: Create VPC
     opentelekomcloud.cloud.vpc:
     name: "{{ vpc_name }}"
     cidr: "10.10.0.0/24"
     state: present
    register: newvpc
    tags:
    - vpc
```
opentelekomcloud.cloud.subnet
-----------------------------
Please pay attention on CIDR block: in case of insufficient numbers of available hosts there
could be errors in autoscaling groups behavior.
```yaml
    - name: Create subnet for VPC
      opentelekomcloud.cloud.subnet:
        name: "{{ vpc_subnet_name }}"
        vpc: "{{ vpc_name }}"
        cidr: "10.10.0.0/27"
        gateway_ip: "10.10.0.1"
        dns_list:
          - "100.125.4.25"
          - "100.125.129.199"
      register: sn
      tags:
        - subnet
```
