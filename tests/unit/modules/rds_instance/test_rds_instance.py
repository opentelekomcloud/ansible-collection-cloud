import json

from unittest import TestCase, mock

from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes

from ansible_collections.opentelekomcloud.cloud.plugins.modules import (
    rds_instance
)


class FakeCloud(object):
    """This is a fake conn object
    """

    instance = mock.MagicMock()
    instance.to_dict = mock.MagicMock(return_value={'a': 'b'})
    instance.id = 1
    instance.job_id = 'fake_job_id'

    create_rds_instance = mock.MagicMock(return_value=instance)
    delete_rds_instance = mock.MagicMock(return_value=None)
    rds = mock.MagicMock()
    rds.find_instance = mock.MagicMock()
    rds.delete_instance = mock.MagicMock()


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class RdsInstanceTest(TestCase):

    def setUp(self):
        self.mock_module_helper = mock.patch.multiple(
            basic.AnsibleModule,
            exit_json=exit_json,
            fail_json=fail_json)
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

        self.conn = FakeCloud()
        self.module = rds_instance.RdsInstanceModule
        self.module.openstack_cloud_from_module = \
            mock.MagicMock(return_value=(self.conn, self.conn))

    def test_module_fail_when_required_args_missing(self):
        """Ensure we fail with no params"""
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            rds_instance.main()

    def test__system_state_change_present(self):
        """Ensure _system_state_change works properly with state=present"""
        set_module_args({
            'state': 'present',
            'name': 'test'
        })
        self.assertTrue(self.module()._system_state_change(False))
        self.assertFalse(self.module()._system_state_change(True))

    def test__system_state_change_absent(self):
        """Ensure _system_state_change works properly with state=absent"""
        set_module_args({
            'state': 'absent',
            'name': 'test'
        })
        self.assertTrue(self.module()._system_state_change(True))
        self.assertFalse(self.module()._system_state_change(False))

    def test_ensure_created(self):
        """Ensure we sent create request"""
        set_module_args({
            'state': 'present',
            'name': 'test',
        })
        with self.assertRaises(AnsibleExitJson) as result:
            self.conn.rds.find_instance.return_value = None
            self.module().run()
        self.conn.create_rds_instance.assert_called_with(
            api_timeout=None,
            auth=None,
            auth_type=None,
            availability_zone=None,
            backup_keepdays=None,
            backup_timeframe=None,
            ca_cert=None,
            client_cert=None,
            client_key=None,
            cloud=None,
            configuration=None,
            datastore_type='postgresql',
            datastore_version=None,
            disk_encryption=None,
            flavor=None,
            ha_mode=None,
            interface='public',
            name='test',
            network=None,
            password=None,
            port=None,
            region='eu-de',
            region_name=None,
            replica_of=None,
            router=None,
            security_group=None,
            state='present',
            validate_certs=None,
            volume_size=None,
            volume_type=None,
            wait=True,
            wait_timeout=600)
        self.assertTrue(result.exception.args[0]['changed'])

    def test_ensure_not_created(self):
        """Ensure we do not send create request"""
        set_module_args({
            'state': 'present',
            'name': 'test',
        })
        with self.assertRaises(AnsibleExitJson) as result:
            self.conn.rds.find_instance.return_value = self.conn.instance
            self.module().run()
        self.conn.create_rds_instance.assert_not_called()
        self.assertFalse(result.exception.args[0]['changed'])

    def test_ensure_deleted(self):
        """Ensure we send delete request"""
        set_module_args({
            'state': 'absent',
            'name': 'test',
            'wait': 'false'
        })
        with self.assertRaises(AnsibleExitJson) as result:
            self.conn.rds.find_instance.return_value = self.conn.instance
            self.conn.delete_rds_instance.return_value = None
            self.module().run()
        self.conn.delete_rds_instance.assert_called_with(
            instance=self.conn.instance.id,
            wait=False
        )
        self.assertTrue(result.exception.args[0]['changed'])

    def test_ensure_not_deleted(self):
        """Ensure we do not send delete request"""
        set_module_args({
            'state': 'absent',
            'name': 'test',
        })
        with self.assertRaises(AnsibleExitJson) as result:
            self.conn.rds.find_instance.return_value = None
            self.module().run()
        self.conn.delete_rds_instance.assert_not_called()
        self.assertFalse(result.exception.args[0]['changed'])
