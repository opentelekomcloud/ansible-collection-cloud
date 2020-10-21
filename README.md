# ansible-collections
Ansible Collections for using with OTC (addition to the native OpenStack modules)

* cloud - collection containing additional ansible modules for managing OTC
  specific resources (or modified OpenStack modules in case of behavioral
  differencies)

## Requirements

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
