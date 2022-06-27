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

import abc

try:
    import openstack as sdk
    import otcextensions
    from otcextensions import sdk as otc_sdk
    from pkg_resources import parse_version as V
    HAS_LIBRARIES = True
except ImportError:
    HAS_LIBRARIES = False

from ansible.module_utils.basic import AnsibleModule


def openstack_full_argument_spec(**kwargs):
    spec = dict(
        cloud=dict(default=None, type='raw'),
        auth_type=dict(default=None),
        auth=dict(default=None, type='dict', no_log=True),
        region_name=dict(default=None),
        validate_certs=dict(default=None, type='bool', aliases=['verify']),
        ca_cert=dict(default=None, aliases=['cacert']),
        client_cert=dict(default=None, aliases=['cert']),
        client_key=dict(default=None, no_log=True, aliases=['key']),
        wait=dict(default=True, type='bool'),
        timeout=dict(default=180, type='int'),
        api_timeout=dict(default=None, type='int'),
        interface=dict(
            default='public', choices=['public', 'internal', 'admin'],
            aliases=['endpoint_type']),
    )
    spec.update(kwargs)
    return spec


class OTCModule:
    """Openstack Module is a base class for all Openstack Module classes.

    The class has `run` function that should be overriden in child classes,
    the provided methods include:

    Methods:
        params: Dictionary of Ansible module parameters.
        module_name: Module name (i.e. server_action)
        sdk_version: Version of used OpenstackSDK.
        results: Dictionary for return of Ansible module,
            must include `changed` keyword.
        exit, exit_json: Exit module and return data inside, must include
            changed` keyword in a data.
        fail, fail_json: Exit module with failure, has `msg` keyword to
            specify a reason of failure.
        conn: Connection to SDK object.
        log: Print message to system log.
        debug: Print debug message to system log, prints if Ansible Debug is
            enabled or verbosity is more than 2.
        check_deprecated_names: Function that checks if module was called with
            a deprecated name and prints the correct name with deprecation
            warning.
        check_versioned: helper function to check that all arguments are known
            in the current SDK version.
        run: method that executes and shall be overriden in inherited classes.

    Args:
        deprecated_names: Should specify deprecated modules names for current
            module.
        argument_spec: Used for construction of Openstack common arguments.
        module_kwargs: Additional arguments for Ansible Module.
    """

    argument_spec = {}
    module_kwargs = {}
    otce_min_version = None

    def __init__(self):

        self.ansible = AnsibleModule(
            openstack_full_argument_spec(**self.argument_spec),
            **self.module_kwargs)
        self.params = self.ansible.params
        self.module_name = self.ansible._name
        self.sdk_version = None
        self.results = {'changed': False}
        self.exit = self.exit_json = self.ansible.exit_json
        self.fail = self.fail_json = self.ansible.fail_json
        self.sdk, self.conn = self.openstack_cloud_from_module()

    def log(self, msg):
        """Prints log message to system log.

        Arguments:
            msg {str} -- Log message
        """
        self.ansible.log(msg)

    def debug(self, msg):
        """Prints debug message to system log

        Arguments:
            msg {str} -- Debug message.
        """
        if self.ansible._debug or self.ansible._verbosity > 2:
            self.ansible.log(
                " ".join(['[DEBUG]', msg]))

    def openstack_cloud_from_module(self, min_version='0.6.9'):
        if self.otce_min_version:
            min_version = self.otce_min_version

        if not HAS_LIBRARIES:
            self.fail_json(msg='openstacksdk and otcextensions are required for this self')

        if min_version:
            min_version = max(V('0.6.9'), V(min_version))
        else:
            min_version = V('0.6.9')

        if V(otcextensions.__version__) < min_version:
            self.fail_json(
                msg="To utilize this self, the installed version of "
                    "the otcextensions library MUST be >={min_version}".format(
                        min_version=min_version))

        cloud_config = self.params.pop('cloud', None)
        try:
            if isinstance(cloud_config, dict):
                fail_message = (
                    "A cloud config dict was provided to the cloud parameter"
                    " but also a value was provided for {param}. If a cloud"
                    " config dict is provided, {param} should be"
                    " excluded.")
                for param in (
                        'auth', 'region_name', 'validate_certs',
                        'ca_cert', 'client_key', 'api_timeout', 'auth_type'):
                    if self.params[param] is not None:
                        self.fail_json(msg=fail_message.format(param=param))
                # For 'interface' parameter, fail if we receive a non-default value
                if self.params['interface'] != 'public':
                    self.fail_json(msg=fail_message.format(param='interface'))
                conn = sdk.connect(**cloud_config)
                otc_sdk.load(conn)
                return sdk, conn
            else:
                conn = sdk.connect(
                    cloud=cloud_config,
                    auth_type=self.params['auth_type'],
                    auth=self.params['auth'],
                    region_name=self.params['region_name'],
                    verify=self.params['validate_certs'],
                    cacert=self.params['ca_cert'],
                    key=self.params['client_key'],
                    api_timeout=self.params['api_timeout'],
                    interface=self.params['interface'],
                )
                otc_sdk.load(conn)
                return sdk, conn
        except sdk.exceptions.SDKException as e:
            # Probably a cloud configuration/login error
            self.fail_json(msg=str(e))

    # Filter out all arguments that are not from current SDK version
    def check_versioned(self, **kwargs):
        """Check that provided arguments are supported by current SDK version

        Returns:
            versioned_result {dict} dictionary of only arguments that are
                                    supported by current SDK version. All others
                                    are dropped.
        """
        versioned_result = {}
        for var_name in kwargs:
            if ('min_ver' in self.argument_spec[var_name]
                    and V(self.sdk_version) < self.argument_spec[var_name]['min_ver']):
                continue
            if ('max_ver' in self.argument_spec[var_name]
                    and V(self.sdk_version) > self.argument_spec[var_name]['max_ver']):
                continue
            versioned_result.update({var_name: kwargs[var_name]})
        return versioned_result

    @abc.abstractmethod
    def run(self):
        pass

    def __call__(self):
        """Execute `run` function when calling the class.
        """

        try:
            results = self.run()
            if results and isinstance(results, dict):
                self.ansible.exit_json(**results)

        except self.sdk.exceptions.OpenStackCloudException as e:
            params = {
                'msg': str(e),
                'extra_data': {
                    'data': getattr(e, 'extra_data', 'None'),
                    'details': getattr(e, 'details', 'None'),
                    'response': getattr(getattr(e, 'response', ''),
                                        'text', 'None')
                }
            }
            self.ansible.fail_json(**params)
