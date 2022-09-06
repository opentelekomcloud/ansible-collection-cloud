Open Telekom Cloud Manuals
==========================


This document contains examples of implementing OTC modules. Besides playbooks itself, we also
put here tips and tricks helping you to understand how exactly the code works.
For raw playbooks please go to [Playbooks](https://github.com/opentelekomcloud/ansible-collection-cloud/tree/docs_module_examples/examples/playbooks).

**Modules are used in this doc:**

* [opentelekomcloud.cloud.as_config](#opentelekomcloud.cloud.as_config)
* [opentelekomcloud.cloud.as_group](#opentelekomcloud.cloud.as_group)
* [opentelekomcloud.cloud.as_instance](#opentelekomcloud.cloud.as_instance)
* [opentelekomcloud.cloud.as_instance_info](#opentelekomcloud.cloud.as_instance_info)
* [opentelekomcloud.cloud.as_policy](#opentelekomcloud.cloud.as_policy)
* [opentelekomcloud.cloud.as_policy_info](#opentelekomcloud.cloud.as_policy_info)
* [opentelekomcloud.cloud.as_quota_info](#opentelekomcloud.cloud.as_quota_info)
* [opentelekomcloud.cloud.cce_cluster](#opentelekomcloud.cloud.cce_cluster)
* [opentelekomcloud.cloud.cce_cluster_cert_info](#opentelekomcloud.cloud.cce_cluster_cert_info)
* [opentelekomcloud.cloud.cce_cluster_info](#opentelekomcloud.cloud.cce_cluster_info)
* [opentelekomcloud.cloud.cce_cluster_node](#opentelekomcloud.cloud.cce_cluster_node)
* [opentelekomcloud.cloud.cce_cluster_node_info](#opentelekomcloud.cloud.cce_cluster_node_info)
* [opentelekomcloud.cloud.cce_node_pool](#opentelekomcloud.cloud.cce_node_pool)
* [opentelekomcloud.cloud.cce_node_pool_info](#opentelekomcloud.cloud.cce_node_pool_info)
* [opentelekomcloud.cloud.ces_alarms](#opentelekomcloud.cloud.ces_alarms)
* [opentelekomcloud.cloud.ces_alarms](#opentelekomcloud.cloud.ces_alarms)
* [opentelekomcloud.cloud.ces_alarms_info](#opentelekomcloud.cloud.ces_alarms_info)
* [opentelekomcloud.cloud.css_cluster](#opentelekomcloud.cloud.css_cluster)
* [opentelekomcloud.cloud.css_cluster_info](#opentelekomcloud.cloud.css_cluster_info)
* [opentelekomcloud.cloud.css_snapshot](#opentelekomcloud.cloud.css_snapshot)
* [opentelekomcloud.cloud.css_snapshot_info](#opentelekomcloud.cloud.css_snapshot_info)
* [opentelekomcloud.cloud.dds_datastore_info](#opentelekomcloud.cloud.dds_datastore_info)
* [opentelekomcloud.cloud.dds_flavor_info](#opentelekomcloud.cloud.dds_flavor_info)
* [opentelekomcloud.cloud.dds_instance](#opentelekomcloud.cloud.dds_instance)
* [opentelekomcloud.cloud.dds_instance_info](#opentelekomcloud.cloud.dds_instance_info)
* [opentelekomcloud.cloud.deh_host](#opentelekomcloud.cloud.deh_host)
* [opentelekomcloud.cloud.deh_host_info](#opentelekomcloud.cloud.deh_host_info)
* [opentelekomcloud.cloud.deh_host_type_info](#opentelekomcloud.cloud.deh_host_type_info)
* [opentelekomcloud.cloud.deh_server_info](#opentelekomcloud.cloud.deh_server_info)
* [opentelekomcloud.cloud.floating_ip](#opentelekomcloud.cloud.floating_ip)
* [opentelekomcloud.cloud.lb_certificate](#opentelekomcloud.cloud.lb_certificate)
* [opentelekomcloud.cloud.lb_certificate_info](#opentelekomcloud.cloud.lb_certificate_info)
* [opentelekomcloud.cloud.lb_healthmonitor](#opentelekomcloud.cloud.lb_healthmonitor)
* [opentelekomcloud.cloud.lb_healthmonitor_info](#opentelekomcloud.cloud.lb_healthmonitor_info)
* [opentelekomcloud.cloud.lb_listener](#opentelekomcloud.cloud.lb_listener)
* [opentelekomcloud.cloud.lb_listener_info](#opentelekomcloud.cloud.lb_listener_info)
* [opentelekomcloud.cloud.lb_member](#opentelekomcloud.cloud.lb_member)
* [opentelekomcloud.cloud.lb_member_info](#opentelekomcloud.cloud.lb_member_info)
* [opentelekomcloud.cloud.lb_pool](#opentelekomcloud.cloud.lb_pool)
* [opentelekomcloud.cloud.lb_pool_info](#opentelekomcloud.cloud.lb_pool_info) 
* [opentelekomcloud.cloud.loadbalancer](#opentelekomcloud.cloud.loadbalancer)
* [opentelekomcloud.cloud.loadbalancer_info](#opentelekomcloud.cloud.loadbalancer_info)
* [opentelekomcloud.cloud.rds_backup](#opentelekomcloud.cloud.rds_backup)
* [opentelekomcloud.cloud.rds_backup_info](#opentelekomcloud.cloud.rds_backup_info)
* [opentelekomcloud.cloud.rds_datastore_info](#opentelekomcloud.cloud.rds_datastore_info)
* [opentelekomcloud.cloud.rds_flavor_info](#opentelekomcloud.cloud.rds_flavor_info)
* [opentelekomcloud.cloud.rds_instance](#opentelekomcloud.cloud.rds_instance)
* [opentelekomcloud.cloud.rds_instance_info](#opentelekomcloud.cloud.rds_instance_info)
* [opentelekomcloud.cloud.security_group](#opentelekomcloud.cloud.security_group)
* [opentelekomcloud.cloud.subnet](#opentelekomcloud.cloud.subnet)
* [opentelekomcloud.cloud.volume_backup](#opentelekomcloud.cloud.volume_backup)
* [opentelekomcloud.cloud.volume_backup_info](#opentelekomcloud.cloud.volume_backup_info)
* [opentelekomcloud.cloud.volume_snapshot_info](#opentelekomcloud.cloud.volume_snapshot_info)
* [opentelekomcloud.cloud.vpc](#opentelekomcloud.cloud.vpc)
* [openstack.cloud.keypair](#openstack.cloud.keypair)
* [openstack.cloud.server](#openstack.cloud.server)



Initial Infrastructure
======================

Initial infrastructure contains basic resources. In most of all cases these resources are
mandatory for every kind of systems, so let's start with them.

First, we need to create ecosystem for further infrastructure. Its include network entities, such
as VPC and subnet, security group and a couple of ECSs.

<a name="opentelekomcloud.cloud.vpc"></a>

#### opentelekomcloud.cloud.vpc

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
<a name="opentelekomcloud.cloud.subnet"></a>

#### opentelekomcloud.cloud.subnet

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
---
**NOTE**
<details>
  <summary>Native OpenStack Modules</summary>

  <p>

 There are a few mismatches in resources logic and naming  between native Openstack and
 Opentelekomcloud. To make it clear we placed examples using native Openstack resources.

> Creating a network. In Open Telekom Cloud infrastructure this entity is hidden inside
> Subnet summary, and isn't create separately, but only querying from the existing Subnet.

```diff
  - name: Create network
    openstack.cloud.os_network:
       name: "{{ network_name }}"
       state: present
    register: network

   - name: Create subnet. Openstack's Subnet is equal Open Telekom Cloud Subnet.
     openstack.cloud.os_subnet:
       name: "{{ subnet_name }}"
       state: present
       network_name: "{{ network.network.name }}"
       cidr: "192.168.110.0/24"
       dns_nameservers: "{{ ['100.125.4.25', '8.8.8.8'] }}"
     register: subnet
```
> Creating a router. In Open Telekom Cloud terms it's a VPC. Please pay attention that
> Network argument here is not an Network created on previous step, but constanta for OTC.

```diff
 - name: Create router
   openstack.cloud.os_router:
     name: "{{ router_name }}"
     state: present
     network: admin_external_net
     enable_snat: true
       interfaces:
          - net: "{{ network.network.name }}"
            subnet: "{{ subnet.subnet.name }}"
   register: router
```
  </p>
  </details>

---

<a name="opentelekomcloud.cloud.security_group"></a>

#### opentelekomcloud.cloud.security_group

Exclusive mode guarantee that only explicitly passed rules are will take effect, and all of the
 existing before will be deleted. To disable this behavior set ``Exclusive`` option as ``false``.
```yaml
    - name: Create new security group
      opentelekomcloud.cloud.security_group:
        state: present
        name: "{{ security_group_name }}"
        description: "Security group for testing purposes"
        security_group_rules:
          - direction: "egress"
            ethertype: "IPv4"
            protocol: "tcp"
          - direction: "egress"
            ethertype: "IPv6"
          - direction: "ingress"
            ethertype: "IPv4"
            protocol: "tcp"
            port_range_max: 22
            port_range_min: 22
        exclusive: true
      register: secgroup
      tags:
        - security_group
```

<a name="openstack.cloud.server"></a>

#### openstack.cloud.server

For the time being, you can create ECS with native OpenStack module. Here we'll create two ECSs 
to show you how they could be involved into infrastructure.
```yaml
- name: Create first ECS and attach it to the resources
  openstack.cloud.server:
    name: "{{ ecs1_name }}"
    image: "{{ ecs_image }}"
    network: "{{  newvpc.vpc.id  }}"
    flavor: "s3.medium.1"
    availability_zone: "eu-de-01"
    volume_size: 6
    security_groups: "{{ security_group_name }}"
    auto_ip: false
    state: present
  register: ecs1
  tags:
    - server1
```
```yaml
- name: Create second ECS and attach it to the resources
  openstack.cloud.server:
    name: "{{ ecs2_name }}"
    image: "{{ ecs_image }}"
    network: "{{  newvpc.vpc.id  }}"
    flavor: "s3.medium.1"
    availability_zone: "eu-de-01"
    volume_size: 6
    security_groups: "{{ security_group_name }}"
    auto_ip: false
    state: present
  register: ecs2
  tags:
    - server2
```

<a name="opentelekomcloud.cloud.volume_backup"></a>

#### opentelekomcloud.cloud.volume_backup

You're able to backup both types of disks: system and additionally attached. Cloud Server
Backups will be cover in a next examples.
```yaml
- name: Create a backup of the system volume
  opentelekomcloud.cloud.volume_backup:
    display_name: "{{ backup_name }}"
    display_description: "Full backup of the test instance"
    state: absent
    volume: "{{ ecs_1_vol }}"
    force: true
    wait: true
    timeout: 123
  register: bckp
  tags:
    - volume_backup
```

<a name="opentelekomcloud.cloud.volume_backup_info"></a>

#### opentelekomcloud.cloud.volume_backup_info

Let's check whether we have a backup of the ECS volume.
```yaml
- name: Get info about volume backup
  opentelekomcloud.cloud.volume_backup_info:
    volume: "{{ ecs_1_vol }}"
  tags: backup_info
```

<a name="opentelekomcloud.cloud.volume_snapshot_info"></a>

#### opentelekomcloud.cloud.volume_snapshot_info

Snapshot is mandatory for any kind of backup, both full or incremental. If there are no any
backups created before, and current backup is the first one for this volume, snapshot will be
create automatically.
```yaml
- name: Get info about volume shapshot
  opentelekomcloud.cloud.volume_snapshot_info:
    name: "yet_another**"
  tags:
    - snapshot_info
```

<a name="openstack.cloud.keypair"></a>

#### openstack.cloud.keypair

Keypair is mandatory condition for creating and modifying AS configurations and groups. Be avoid
of accidental deleting of this entity, because in this case you'll lost control on your AS
entities.
```yaml
- name: Create new keypair for accessing AS config
  openstack.cloud.keypair:
    name: "{{ keypair_name }}"
  register: kp
  tags:
    - create_keypair
```

<a name="opentelekomcloud.cloud.as_config"></a>

#### opentelekomcloud.cloud.as_config

You're able to create a new AS config based on existing ECS, using it as a template. For this,
point ECS's id as a parameter. Here is example of a new AS config, taken from scratch.
```yaml
- name: Create new AS config
  opentelekomcloud.cloud.as_config:
    scaling_configuration: "{{ as_new_config_name }}"
    key_name: "{{ keypair_name }}"
    image: "Standard_CentOS_7_latest"
    flavor: "s3.medium.1"
    disk:
      - size: 10
        volume_type: 'SAS'
        disk_type: 'SYS'
  register: as_config_new
  tags:
    - create_as_config
```

<a name="opentelekomcloud.cloud.as_group"></a>

#### opentelekomcloud.cloud.as_group

Please pay attention to numbers of desiring instances. It should fall within range given in CIDR
block of attaching subnet. Router parameter points to VPC ID.
```yaml
- name: Create AS Group
  opentelekomcloud.cloud.as_group:
    scaling_group:
      name: "{{ as_group_name }}"
    scaling_configuration: "{{ as_config_new.as_config.name }}"
    min_instance_number: 0
    desire_instance_number: 2
    max_instance_number: 4
    availability_zones: ["eu-de-01"]
    networks: [{"id": "{{ network_id }}"}]
    security_groups: [{"id": "{{ secgroup_id }}"}]
    router: "{{ router }}"
    delete_publicip: true
    delete_volume: true
    action: "resume"
    state: "present"
    wait: true
    timeout: 400
  register: as_group
  tags:
    - create_as_group
```
If you want to change AS group's name, you can do it with the same module:
```yaml
- name: Rename AS group
  opentelekomcloud.cloud.as_group:
    scaling_group:
      id: "{{ as_group.as_group.id }}"
      name: "{{ new_as_group_name }}"
    max_instance_number: 4
  register: as_group_new
```

<a name="opentelekomcloud.cloud.as_instance"></a>

#### opentelekomcloud.cloud.as_instance

Besides creating instances directly from AS group module, you can add already existing ECSs to 
the AS group. Please pay attention that instances to be added **must be** in the same AZ as AS group.
Let's add two ECSs created before.
```yaml
- name: Add AS instances to the AS group
  opentelekomcloud.cloud.as_instance:
    scaling_group: "{{ as_group_new.as_group.id }}"
    scaling_instances:
      - "{{ ecs1.server.id }}"
      - "{{ ecs2.server.id }}"
    action: "add"
    state: present
  register: as_instances
  tags:
    - add_instances
```

<a name="opentelekomcloud.cloud.as_instance_info"></a>

#### opentelekomcloud.cloud.as_instance_info

You can query info about instances in the ``AS group``.
```yaml
- name: Get list of AS Instances after adding new instances
  opentelekomcloud.cloud.as_instance_info:
    scaling_group: "{{ as_group.as_group.id }}"
  register: as_inst_list_af
```

<a name="opentelekomcloud.cloud.floating_ip"></a>

#### opentelekomcloud.cloud.floating_ip

We can obtain a public IP and assign it to the resource you want to. Please note that 
``network`` is the constant value, and always equals ``admin_external_net``.
```yaml
- name: Assign Floating IP
  opentelekomcloud.cloud.floating_ip:
    network: admin_external_net
  register: fl
```

<a name="opentelekomcloud.cloud.ces_alarms"></a>

#### opentelekomcloud.cloud.ces_alarms

There are many services interconnected with Cloud eye. All the services are logically united
into groups named ``Namespaces``. Every ``Namespace`` supports plenty of ``metrics``, and each of them can
be monitored. You can get comprehensive information regarding ``Namespaces`` and ``metrics``
here: [Services Interconnected with Cloud Eye.](https://docs.otc.t-systems.com/usermanual/ces/en-us_topic_0202622212.html)
Besides particular metric you want to check up, you need to know ``Dimension`` -
this entity specifies the metric dimension of the selected resource type. In this example we 
want to monitor inbound bandwidth of public IP connected to our VPC. So first of all we will 
assign a new public IP for further monitoring.
First we need to create an Alarm, which will be included in AS Policy.
```yaml
- name: Create Cloud Eye Alarm
  opentelekomcloud.cloud.ces_alarms:
    alarm_name: "{{ alarm_name }}"
    state: present
    metric:
      namespace: "SYS.VPC"
      dimensions:
        - name: "publicip_id"
          value: "{{ fl.floating_ip.id }}"
      metric_name: "down_stream"
    condition:
      period: 300
      filter: average
      comparison_operator: ">="
      value: 6
      unit: "B"
      count: 1
    alarm_enabled: true
    alarm_action_enabled: false
  register: alarm
```

<a name="opentelekomcloud.cloud.as_policy"></a>

#### opentelekomcloud.cloud.as_policy

Now we're ready to create AS policy. This policy based on alarms, that indicates that the 
scaling action is triggered by an alarm.
```yaml
- name: Create AS policy
  opentelekomcloud.cloud.as_policy:
    scaling_group: "{{ as_group_name }}"
    scaling_policy: "{{ as_policy_name }}"
    scaling_policy_type: "alarm"
    alarm: "{{ alarm_name }}"
    state: "present"
  register: as_policy
```
Besides that, you can set ``scaling_policy_type`` to **``SCHEDULED``**, which indicates that the 
scaling action is triggered as scheduled, or **``RECURRENCE``** - in this case scaling action is 
triggered periodically. This is how play looks like if policy type **``SCHEDULED``** or
**``RECURRENCE``** is choosen:
```yaml
- name: Create AS policy
  opentelekomcloud.cloud.as_policy:
    scaling_group: "{{ as_group_name }}"
    scaling_policy: "{{ as_policy_name }}"
    scaling_policy_type: "recurrence"
    scheduled_policy:
      recurrence_type: "weekly"
      recurrence_value: "7"
      launch_time: "01:00"
      start_time: "2022-08-27T00:00Z"
    scaling_policy_action:
      operation: "add"
      instance_number: "1"
    state: present
  register: as_policy
```
Once being created, AS policy is changeable: policy name, type and actions are able to adjust,
with all its suboptions. Also you can change policy's name.
```yaml
- name: Update AS policy (add scaling_policy_action)
  opentelekomcloud.cloud.as_policy:
    scaling_group: "{{ as_group_name }}"
    scaling_policy: "{{ new_as_policy_name }}"
    scaling_policy_type: "alarm"
    alarm: "{{ alarm_name }}"
    state: "present"
    scaling_policy_action:
      operation: "add"
      instance_number: 1
  register: as_policy
```

<a name="opentelekomcloud.cloud.as_policy_info"></a>

#### opentelekomcloud.cloud.as_policy_info

You can query info about AS policies, providing its type, name or ID. Also you're able to query
policy info providing ``scaling group`` name or ID.
```yaml
- name: Get list of AS Policies
  opentelekomcloud.cloud.as_policy_info:
    scaling_group: "{{ as_group_name }}"
  register: as_policies
```

<a name="opentelekomcloud.cloud.as_quota_info"></a>

#### opentelekomcloud.cloud.as_quota_info

This module This API is used to query the total quotas and used quotas of AS groups, AS
configurations, bandwidth scaling policies, AS policies, and instances for a specified tenant.
```yaml
- name: Check AS group quotas
  opentelekomcloud.cloud.as_quota_info:
    scaling_group_id: "{{ scaling_group_id }}"
```

<a name="opentelekomcloud.cloud.cce_cluster"></a>

#### opentelekomcloud.cloud.cce_cluster

 Let's create a Cloud Container Engine cluster and attach it to the previously deployed infrastructure.
```yaml
- name: Create CCE Cluster
  opentelekomcloud.cloud.cce_cluster:
    name: "{{ cce_cluster_name }}"
    description: "Cloud Container Engine test cluster"
    type: "virtualmachine"
    version: "v1.21"
    flavor: "{{ cce_flavor }}"
    authentication_mode: "rbac"
    kube_proxy_mode: "iptables"
    router: "{{ router }}"
    network: "{{ network_id }}"
    container_network_mode: "{{ container_network_mode }}"
    container_network_cidr: "10.0.0.0/16"
    availability_zone: "multi_az"
    state: present
  register: cluster
```

<a name="opentelekomcloud.cloud.cce_cluster_cert_info"></a>

#### opentelekomcloud.cloud.cce_cluster_cert_info

You can use open-source Kubernetes APIs for accessing cluster. For this, you should obtain the
**cluster's X.509 Certificate** via web console. Create and download it. The downloaded
certificate contains three files: ***client.key, client.crt, and ca.crt.*** Of course, you 
should keep it in a safe place, but you are able to get an info about cluster's certificates.
```yaml
- name: Get info about cluster certificate
  opentelekomcloud.cloud.cce_cluster_cert_info:
    cluster: "{{ cluster.cce_cluster.id }}"
```

<a name="opentelekomcloud.cloud.cce_node_pool"></a>

#### opentelekomcloud.cloud.cce_node_pool

After cluster creating is finished, you should create a node pool, which will contain some number
of working nodes.
```yaml
- name: Create node pool
  opentelekomcloud.cloud.cce_node_pool:
    name: "{{ node_pool_name }}"
    availability_zone: "eu-de-01"
    autoscaling_enabled: false
    cluster: "{{ cluster.cce_cluster.id }}"
    data_volumes:
      - volumetype: "SSD"
        size: 120
      - volumetype: "SATA"
        size: 100
        encrypted: false
    flavor: "{{ node_flavor }}"
    initial_node_count: 0
    k8s_tags:
      mytag: "myvalue"
      mysecondtag: "mysecondvalue"
    min_node_count: 1
    max_node_count: 3
    network: "{{ network_id }}"
    priority: 2
    os: "{{ os_cluster_name }}"
    ssh_key: "{{ keypair_name }}"
    tags:
      - key: "my_first_key"
        value: "my_first_value"
      - key: "my_second_key"
        value: "my_secound_value"
    taints:
      - key: "first_taint_key"
        value: "first_taint_value"
        effect: "NoSchedule"
      - key: "second_taint_key"
        value: "second_taint_value"
        effect: "NoExecute"
    state: present
  register: pool
```

<a name="opentelekomcloud.cloud.cce_cluster_node"></a>

#### opentelekomcloud.cloud.cce_cluster_node

Now you can add to the node pool nodes. Please pay attention that AZ of these nodes must be
equal to node pool's AZ.
```yaml
- name: Create CCE Cluster Node
  opentelekomcloud.cloud.cce_cluster_node:
    annotations:
      annotation1: "Test cluster nodes"
    availability_zone: "eu-de-01"
    cluster: "{{ cce_cluster_name }}"
    count: 1
    data_volumes:
      - volumetype: "SATA"
        size: 100
        encrypted: false
      - volumetype: "SAS"
        size: 120
    flavor: "{{ node_flavor }}"
    k8s_tags:
      testtag: "value"
    ssh_key: "{{ keypair_name }}"
    labels:
      mein: "label"
    max_pods: 16
    name: "{{ cce_node_name }}"
    network: "{{ network_id }}"
    os: "{{ os_cluster_name }}"
    root_volume_size: 40
    root_volume_type: SATA
    tags:
      - key: "key1"
        value: "value1"
      - key: "key2"
        value: "value2"
    wait: true
    state: present
  register: node
```

<a name="opentelekomcloud.cloud.cce_cluster_info"></a>

#### opentelekomcloud.cloud.cce_cluster_info

This example shows how to obtain info about ``cce cluster``.
```yaml
- name: Get info about cluster
  opentelekomcloud.cloud.cce_cluster_info:
    name: "{{ cluster.cce_cluster.id }}"
```

<a name="opentelekomcloud.cloud.cce_node_pool_info"></a>

#### opentelekomcloud.cloud.cce_node_pool_info

...and about ``node pool``:
```yaml
- name: Get info about node pool
  opentelekomcloud.cloud.cce_node_pool_info:
    cce_cluster: "{{ cluster.cce_cluster.id }}"
```

<a name="opentelekomcloud.cloud.cce_cluster_node_info"></a>

#### opentelekomcloud.cloud.cce_cluster_node_info

And cce ``cluster node``, indeed:
```yaml
- name: Get info about cluster nodes
  opentelekomcloud.cloud.cce_cluster_node_info:
    cce_cluster: "{{ cluster.cce_cluster.id }}"
```

<a name="opentelekomcloud.cloud.loadbalancer"></a>

#### opentelekomcloud.cloud.loadbalancer

This loadbalancer would be attached to the couple of ECSs united into one backend server group.
```yaml
- name: Create loadbalancer for cluster
  opentelekomcloud.cloud.loadbalancer:
    state: present
    auto_public_ip: true
    name: "{{ lb_name }}"
    vip_subnet: "{{ vpc_subnet_name }}"
  register: lb
```

<a name="opentelekomcloud.cloud.lb_certificate"></a>

#### opentelekomcloud.cloud.lb_certificate

This module just integrate public and private keys into certificate for listener. Both public
and private keys you should obtain before on third-party resources, for instance, Letsencrypt,
and put in available for Ansible engine place.
```yaml
- name: Create certificate for HTTPS connections
  opentelekomcloud.cloud.lb_certificate:
    name: "elb_https_cert"
    type: "server"
    content: "/home/user/files/rootCA.pem"
    private_key: "/home/user/files/rootCA.key"
  register: elb_cert
```

<a name="opentelekomcloud.cloud.lb_listener"></a>

#### opentelekomcloud.cloud.lb_listener

For every type of protocol you can create its own listener. In case of HTTP listener, please pay
attention on your subnet addresses pool, it must be sufficient for all the instances including
listener itself.
```yaml
- name: Create listener for HTTPS traffic
  opentelekomcloud.cloud.lb_listener:
    name: "{{ listener_https_name }}"
    protocol: terminated_https
    protocol_port: 443
    loadbalancer: "{{ lb.loadbalancer.id }}"
    default_tls_container_ref: "{{ elb_cert.elb_certificate.id }}"
  register: listener_https
```

<a name="opentelekomcloud.cloud.lb_pool"></a>

#### opentelekomcloud.cloud.lb_pool

This backend server group will contain multiple ECSs. Here we use roundrobin algorithm, as we
use http protocol, but you can choose source_ip or least_connection.
```yaml
- name: Create backend server group
  opentelekomcloud.cloud.lb_pool:
    state: present
    name: "{{ backend_server_name }}"
    protocol: http
    lb_algorithm: round_robin
    listener: "{{ listener_https }}"
    loadbalancer: "{{ lb.loadbalancer.id }}"
  register: backend
```

<a name="opentelekomcloud.cloud.lb_member"></a>

#### opentelekomcloud.cloud.lb_member

Ok, we created load balancer pool, but it's empty. You can add to the pool ECSs created before.
```yaml
- name: Add first ECS to the backend server group
  opentelekomcloud.cloud.lb_member:
    name: "{{ ecs1_name }}"
    address: "10.10.0.18"
    protocol_port: 443
    subnet: "{{ vpc_subnet_name }}"
    pool: "{{ backend.server_group.id }}"
  register: bcknd_1
```
And as we chose ``round-robin`` algorithm, at least two servers should be in the pool.
```yaml
- name: Add second ECS to the backend server group
  opentelekomcloud.cloud.lb_member:
    name: "{{ ecs2_name }}"
    address: "10.10.0.23"
    protocol_port: 443
    subnet: "{{ vpc_subnet_name }}"
    pool: "{{ backend_group_id }}"
  register: bcknd_2
```

<a name="opentelekomcloud.cloud.lb_healthmonitor"></a>

#### opentelekomcloud.cloud.lb_healthmonitor

After setting up an backend server group, it's highly recommend that you attach health check
monitoring to it.
```yaml
- name: Add HTTPS health check for the backend server group
  opentelekomcloud.cloud.lb_healthmonitor:
    name: "{{ health_https_name }}"
    state: present
    delay: 9
    max_retries: 3
    pool: "{{ backend_group_id }}"
    monitor_timeout: 5
    type: http
    monitor_port: 443
    expected_codes: 200
    http_method: get
  register: https_health
```

<a name="opentelekomcloud.cloud.loadbalancer_info"></a>

#### opentelekomcloud.cloud.loadbalancer_info

You're all set. Let's get some info regarding load balancer and its subentities.
```yaml
- name: Get info about specified load balancer
  opentelekomcloud.cloud.loadbalancer_info:
    name: "{{ lb_name }}"
  register: lb_info
```

<a name="opentelekomcloud.cloud.lb_certificate"></a>

#### opentelekomcloud.cloud.lb_certificate_info

```yaml
- name: Get info about specified certificate
  opentelekomcloud.cloud.lb_certificate_info:
    name: "elb_https_cert"
  register: elb_cert_info
```

<a name="opentelekomcloud.cloud.lb_listener_info"></a>

#### opentelekomcloud.cloud.lb_listener_info

```yaml
- name: Get info about specified litener
  opentelekomcloud.cloud.lb_listener_info:
    name: "{{ listener_https_name }}"
  register: listener_https_info
```

<a name="opentelekomcloud.cloud.lb_pool_info"></a>

#### opentelekomcloud.cloud.lb_pool_info

<a name="opentelekomcloud.cloud.lb_member_info"></a>

```yaml
- name: Get info about specified backend server group
  opentelekomcloud.cloud.lb_pool_info:
    name: "{{ backend_server_name }}"
  register: backend_group_info
```

#### opentelekomcloud.cloud.lb_member_info

```yaml
- name: Get info about specified pool members
  opentelekomcloud.cloud.lb_member_info:
    pool: "{{ backend_server_name }}"
  register: bcknd_members_info
```

<a name="opentelekomcloud.cloud.lb_healthmonitor_info"></a>

#### opentelekomcloud.cloud.lb_healthmonitor_info

```yaml
- name: Get info about health checks for HTTP protocol
  opentelekomcloud.cloud.lb_healthmonitor_info:
    type: http
  register: https_health_info
```

<a name="opentelekomcloud.cloud.ces_alarms"></a>

#### opentelekomcloud.cloud.ces_alarms

Now we'll create several alarms to watch our infrastructure. Mind that ``alarm_name`` is given by
user, and ``dimensions``` name and ``metric_name`` are embedded and constant for each kind of resource, and can be
taken from user's guide on docs portal here: [Services Interconnected with Cloud Eye.](https://docs.otc.t-systems.com/usermanual/ces/en-us_topic_0202622212.html)
SMN topic here has been created beforehand via web console.
```yaml
# SMN topic here has been created beforehand.
- name: Create alarm for ECS CPU utilization
  opentelekomcloud.cloud.ces_alarms:
    alarm_name: "ecs1_cpu_load"
    state: present
    metric:
      namespace: "SYS.ECS"
      dimensions:
        - name: "instance_id"
          value: "{{ ecs_1_id }}"
      metric_name: "CPU_usage"
    condition:
      period: 300
      filter: average
      comparison_operator: ">="
      value: 50
      unit: "Percent"
      count: 1
    alarm_enabled: true
    alarm_action_enabled: false
    alarm_actions:
      - type: "notification"
        notificationList: "urn:smn:eu-de:5dd3c0b24cdc4d31952c49589182a89d:yet_another_topic"
  register: ecs_cpu_alarm
```
As we're watching ECS, ``namespace`` attribute is the same, but ``metric_name`` is different.
```yaml
- name: Create alarm for ECS CPU and memory usage
  opentelekomcloud.cloud.ces_alarms:
    alarm_name: "ecs1_mem_util"
    state: present
    metric:
      namespace: "SYS.ECS"
      dimensions:
        - name: "instance_id"
          value: "{{ ecs_1_id }}"
      metric_name: "Memory_usage"
    condition:
      period: 300
      filter: average
      comparison_operator: ">="
      value: 50
      unit: "Percent"
      count: 1
    alarm_enabled: true
    alarm_action_enabled: true
    alarm_actions:
      - type: "notification"
        notificationList: "urn:smn:eu-de:5dd3c0b24cdc4d31952c49589182a89d:yet_another_topic"
  register: ecs_mem_alarm
```
Let's set up alarm for upstream bandwidth for ELB.
```yaml
- name: Create watchdog alarm for Load Balancer
  opentelekomcloud.cloud.ces_alarms:
    alarm_name: "lb_watchdog"
    state: present
    metric:
      namespace: "SYS.ELB"
      dimensions:
        - name: "lbaas_instance_id"
          value: "{{ elb_id }}"
      metric_name: "m16_l7_upstream_5xx"
    condition:
      period: 300
      filter: average
      comparison_operator: ">="
      value: 5
      unit: "Count/s"
      count: 1
    alarm_enabled: true
    alarm_action_enabled: true
    alarm_actions:
      - type: "notification"
        notificationList: "urn:smn:eu-de:5dd3c0b24cdc4d31952c49589182a89d:yet_another_topic"
  register: elb_5xx_alarm
```
Here type of 'alarm_actions' has been switched to 'autoscaling'. In this case you should set
field 'notificationList' to empty list.
```yaml
- name: Create load alarm for Auto Scaling Group to adjust number of instances
  opentelekomcloud.cloud.ces_alarms:
    alarm_name: "as_load"
    state: present
    metric:
      namespace: "SYS.AS"
      dimensions:
        - name: "AutoScalingGroup"
          value: "{{ as_group_name }}"
      metric_name: "mem_util"
    condition:
      period: 300
      filter: average
      comparison_operator: ">="
      value: 50
      unit: "Percent"
      count: 2
    alarm_enabled: true
    alarm_action_enabled: true
    alarm_actions:
      - type: "autoscaling"
        notificationList: []
  register: as_mem_alarm
```

<a name="opentelekomcloud.cloud.ces_alarms_info"></a>

#### opentelekomcloud.cloud.ces_alarms_info

You can easily get info about any alarm passing its name:
```yaml
- name: Get Alarm Infos
  opentelekomcloud.cloud.ces_alarms_info:
    name: "{{ alarm_name }}"
  register: ces_al_info
```

<a name="opentelekomcloud.cloud.css_cluster"></a>

#### opentelekomcloud.cloud.css_cluster

Here we'll create Cloud Search cluster contained 1 node. Attribute 'cmk_id' is the Master
Key, which encrypts system. This attribute has been created beforehand via web console. Please pay
attention that backup strategy is setting up also in this module.
```yaml
- name: Create Cloud Search cluster
  opentelekomcloud.cloud.css_cluster:
    name: "{{ css_cluster_name }}"
    state: present
    flavor: "{{ css_flavour }}"
    instance_num: 1
    datastore_version: "7.6.2"
    datastore_type: "elasticsearch"
    volume_type: "common"
    volume_size: 40
    system_encrypted: 1
    system_cmkid: "{{ cmk_id }}"
    https_enable: false
    authority_enable: false
    admin_pwd: "{{ password }}"
    router: "{{ router }}"
    net: "{{ network_id }}"
    security_group: "{{ secgroup_id }}"
    backup_period: "00:00 GMT+03:00"
    backup_prefix: "yetanother"
    backup_keepday: 1
  register: css_cluster
```

<a name="opentelekomcloud.cloud.css_cluster_info"></a>

#### opentelekomcloud.cloud.css_cluster_info

Querying info about cluster is available with name or ID of a cluster.
```yaml
- name: Get info about created cluster
  opentelekomcloud.cloud.css_cluster_info:
    name: "{{ css_cluster.id }}"
  register: css_info
```

<a name="opentelekomcloud.cloud.css_snapshot"></a>

#### opentelekomcloud.cloud.css_snapshot

By default, data of all indices is backed up. You can use the asterisk (*) to back up data of
certain indices.
```yaml
- name: Create snapshot of the cluster
  opentelekomcloud.cloud.css_snapshot:
    cluster: "{{ css_cluster.id }}"
    name: "{{ css_snapshot_name }}"
    description: "Example snapshot of the CSS cluster"
    state: present
    indices: "yetanother*"
  register: css_snapshot
```

<a name="opentelekomcloud.cloud.css_snapshot_info"></a>

#### opentelekomcloud.cloud.css_snapshot_info

Ifo module provides info about snapshots.
```yaml
- name: Get info about CSS snapshot
  opentelekomcloud.cloud.css_snapshot_info:
    cluster: "{{ css_cluster.id }}"
```

<a name="opentelekomcloud.cloud.rds_flavor_info"></a>

#### opentelekomcloud.cloud.rds_flavor_info

First of all, let's choose type and version of DB of an RDS instance. For example, we want it
to be a MySQL (besides that you can choose postgresql or sqlserver on Microsoft) in HA (or single or
replica) mode.
```yaml
- name: Get info about choosen type of DB
  opentelekomcloud.cloud.rds_flavor_info:
    datastore: "mysql"
    instance_mode: "ha"
  register: rds_flavors
```

<a name="opentelekomcloud.cloud.rds_instance"></a>

#### opentelekomcloud.cloud.rds_instance

In this debug you can see all the flavors of the chosen DB type, and now you can decide what
flavor exactly fits your needs.
```yaml
- name: debug
  ansible.builtin.debug:
    msg: "{{ rds_flavors.rds_flavors[0].name }}"
```

<a name="opentelekomcloud.cloud.rds_instance_info"></a>

#### opentelekomcloud.cloud.rds_instance_info

Now let's create RDS instance. You can locate it in two or more availability zones.
Password you pass to the module handles in secure mode: this means that it won't be shown in
module's output. Please pay attention that automatic backup strategy is setting here, too.
Attribute 'cmk_id' needed for system encryption, has been created beforehand via web console.
```yaml
- name: Create RDS instance
  opentelekomcloud.cloud.rds_instance:
    name: "{{ rds_instance_name }}"
    state: present
    region: "eu-de"
    availability_zone: "eu-de-01,eu-de-02"
    datastore_type: "mysql"
    datastore_version: "8.0"
    flavor: "{{ rds_flavors.rds_flavors[0].name }}"
    ha_mode: "semisync"
    router: "{{ router }}"
    network: "{{ network_id }}"
    port: 8080
    security_group: "{{ secgroup_id }}"
    password: "{{ password }}"
    volume_type: "ultrahigh"
    volume_size: 40
    disk_encryption: "{{ cmk_id }}"
    backup_keepdays: 1
    backup_timeframe: "02:00-03:00"
    wait: true
    timeout: 777
  register: rds
```

<a name="opentelekomcloud.cloud.rds_datastore_info"></a>

#### opentelekomcloud.cloud.rds_datastore_info

With this info module you can get info about datastore.
```yaml
- name: Let's get info about datastore
  opentelekomcloud.cloud.rds_datastore_info:
    name: "{{ rds.instance.id }}"
```

<a name="opentelekomcloud.cloud.rds_instance_info"></a>

#### opentelekomcloud.cloud.rds_instance_info

And about your instance.
```yaml
- name: Let's get info about whole RDS instance
  opentelekomcloud.cloud.rds_instance_info:
    name: "{{ rds.instance.name }}"
```

<a name="opentelekomcloud.cloud.rds_backup"></a>

#### opentelekomcloud.cloud.rds_backup

With this module you can manually create backup of the instance.
```yaml
- name: Create backup of the instance
  opentelekomcloud.cloud.rds_backup:
    instance: "{{ rds.instance.id }}"
    name: "{{ rds_backup_name }}"
    state: present
    description: "Backup of the RDS instance"
    wait: true
  register: rds_bckp
```

<a name="opentelekomcloud.cloud.rds_backup_info"></a>

#### opentelekomcloud.cloud.rds_backup_info

Queirying RDS backup info. You can use any of specified attributes, together or separately.
```yaml
- name: Get RDS backup info
  opentelekomcloud.cloud.rds_backup_info:
    instance: "{{ rds.instance.id }}"
    backup: "{{ rds_bckp.backup.id }}"
    backup_type: "{{ rds_bckp.backup.type }}"

```

<a name="opentelekomcloud.cloud.dds_flavor_info"></a>

#### opentelekomcloud.cloud.dds_flavor_info

Here we'll allocate Document Database cluster. First, check what are flavors are available in
chosen region.
```yaml
- name: Query info about flavors in region
  opentelekomcloud.cloud.dds_flavor_info:
    region: "eu-de"
  register: dds_flavor
```

<a name="opentelekomcloud.cloud.dds_datastore_info"></a>

#### opentelekomcloud.cloud.dds_datastore_info

Also query supporting datastore versions. Datastore name is the constant: DDS-Community.
```yaml
- name: Query database version
  opentelekomcloud.cloud.dds_datastore_info:
    datastore_name: "DDS-Community"
  register: dds_ds
```

<a name="opentelekomcloud.cloud.dds_instance"></a>

#### opentelekomcloud.cloud.dds_instance

Now we're ready to create DDS cluster. Each cluster consists of mongos, config and shard nodes.
First config node should be allocated. For this kind of node storage size is fixed and equals 20 GB.
Spec code you can find in dds_flavor_info module's output. Please mind that you cannot connect
to config node.
```yaml
- name: Create config node for DDS cluster
  opentelekomcloud.cloud.dds_instance:
    name: "{{ dds_instance_name }}"
    state: present
    region: "eu-de"
    availability_zone: "eu-de-01"
    datastore_version: "{{ dds_ds.datastores[1].version }}"
    router: "{{ router }}"
    network: "{{ network_id }}"
    security_group: "{{ secgroup_id }}"
    password: "{{ password }}"
    disk_encryption: "{{ cmk_id }}"
    mode: "Sharding"
    flavors:
      - type: "config"
        num: 1
        size: 20
        spec_code: "dds.mongodb.s2.large.2.config"
    backup_timeframe: "18:00 GMT+03:00"
    backup_keepdays: 3
    ssl_option: 1
  register: dds_conf
```
Now let's create shards. Each DDS cluster supports from 2 to 16 shards. Storage size varies
from 10 to 1000 GB. Spec code you can find in dds_flavor_info module's output. Please mind that
you cannot connect to a shard node.
```yaml
- name: Create shard instances for DDS cluster
  opentelekomcloud.cloud.dds_instance:
    name: "{{ dds_instance_name }}"
    state: present
    region: "eu-de"
    availability_zone: "eu-de-01"
    datastore_version: "{{ dds_ds.datastores[1].version }}"
    router: "{{ router }}"
    network: "{{ network_id }}"
    security_group: "{{ secgroup_id }}"
    password: "{{ password }}"
    disk_encryption: "{{ cmk_id }}"
    mode: "Sharding"
    flavors:
      - type: "shard"
        num: 2
        size: "10"
        spec_code: "dds.mongodb.s2.medium.4.shard"
    backup_timeframe: "20:00"
    backup_keepdays: 1
    ssl_option: 1
  register: dds_shard
```
For mongos instances storage size is invalid parameter. Mongos instances are the only one which
you could be connect to.
```yaml
- name: Create mongos instances for DDS cluster
  opentelekomcloud.cloud.dds_instance:
    name: "{{ dds_instance_name }}"
    state: present
    region: "eu-de"
    availability_zone: "eu-de-01"
    datastore_version: "{{ dds_ds.datastores[1].version }}"
    router: "{{ router }}"
    network: "{{ network_id }}"
    security_group: "{{ secgroup_id }}"
    password: "{{ password }}"
    disk_encryption: "{{ cmk_id }}"
    mode: "Sharding"
    flavors:
      - type: "mongos"
        num: 2
        spec_code: "dds.mongodb.s2.medium.4.mongos"
    backup_timeframe: "22:00"
    backup_keepdays: 1
    ssl_option: 1
  register: dds_mng
```

<a name="opentelekomcloud.cloud.dds_instance_info"></a>

#### opentelekomcloud.cloud.dds_instance_info

Now we're all set. Creating of cluster takes 15 minutes approximately. After that, you can get
info about your cluster.
```yaml
- name: Get info about DDS cluster
  opentelekomcloud.cloud.dds_instance_info:
    instance: "{{ dds_instance_name }}"
```

<a name="opentelekomcloud.cloud.deh_host_type_info"></a>

#### opentelekomcloud.cloud.deh_host_type_info

This and next plays shows how to allocate dedicated host in OTC. First, query list of available host
types to choose one of them.
```yaml
- name: Query list of available host types
  opentelekomcloud.cloud.deh_host_type_info:
    az: "eu-de-01"
  register: deh_type
```

<a name="opentelekomcloud.cloud.deh_host"></a>

#### opentelekomcloud.cloud.deh_host

This play is allocating Dedicated host. Set 'auto_placement' to true to allow an ECS to be placed
on any available DeH if its DeH ID is not specified during its creation. And please pay
attention that more than one DEHs with the same name are possible!
```yaml
- name: Allocate Dedicated host
  opentelekomcloud.cloud.deh_host:
    name: "{{ deh_name }}"
    state: present
    auto_placement: true
    availability_zone: "eu-de-01"
    quantity: 1
    host_type: "s2"
    tags:
      - key: "First"
        value: "101"
  register: deh
```
In this play we'll change the hostname. For this, you need an host's ID as the only attribute to
unequivocally define the host.
```yaml
- name: Change host name
  opentelekomcloud.cloud.deh_host:
    id: "{{ deh.deh_host.dedicated_host_ids[0] }}"
    name: "{{ deh_new_name }}"
  register: deh_change
```

<a name="opentelekomcloud.cloud.deh_host_info"></a>

#### opentelekomcloud.cloud.deh_host_info

Let's check whether hostname has been changed, and assure in it.
```yaml
- name: Get info about host after name changing
  opentelekomcloud.cloud.deh_host_info:
    host: "{{ deh_change.deh_host.name }}"
  register: deh_new_info

- name: Assert result
  ansible.builtin.assert:
    that:
      - deh.deh_host.name != deh_change.deh_host.name
      - deh_new_info.deh_hosts[0].name == deh_change.deh_host.name
```

<a name="opentelekomcloud.cloud.deh_server_info"></a>

#### opentelekomcloud.cloud.deh_server_info

Let's see, which ECSs are allocated on dedicated host.
```yaml
- name: Get info about ECSs allocated on dedicated host
  opentelekomcloud.cloud.deh_server_info:
    dedicated_host: "{{ deh_change.deh_host.id }}"
```
