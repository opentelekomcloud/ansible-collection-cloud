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

import openstack as sdk
import otcextensions
from otcextensions import sdk as otc_sdk


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


def openstack_module_kwargs(**kwargs):
    ret = {}
    for key in ('mutually_exclusive', 'required_together', 'required_one_of'):
        if key in kwargs:
            if key in ret:
                ret[key].extend(kwargs[key])
            else:
                ret[key] = kwargs[key]

    return ret


def openstack_cloud_from_module(module, min_version='0.6.9'):
    from distutils.version import StrictVersion

    if min_version:
        min_version = max(StrictVersion('0.6.9'), StrictVersion(min_version))
    else:
        min_version = StrictVersion('0.6.9')

    if StrictVersion(otcextensions.__version__) < min_version:
        module.fail_json(
            msg="To utilize this module, the installed version of "
                "the otcextensions library MUST be >={min_version}.".format(
                    min_version=min_version))

    cloud_config = module.params.pop('cloud', None)
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
                if module.params[param] is not None:
                    module.fail_json(msg=fail_message.format(param=param))
            # For 'interface' parameter, fail if we receive a non-default value
            if module.params['interface'] != 'public':
                module.fail_json(msg=fail_message.format(param='interface'))
                conn = sdk.connect(**cloud_config)
                otc_sdk.load(conn)
                return sdk, conn
        else:
            conn = sdk.connect(
                cloud=cloud_config,
                auth_type=module.params['auth_type'],
                auth=module.params['auth'],
                region_name=module.params['region_name'],
                verify=module.params['validate_certs'],
                cacert=module.params['ca_cert'],
                key=module.params['client_key'],
                api_timeout=module.params['api_timeout'],
                interface=module.params['interface'],
            )
            otc_sdk.load(conn)
            return sdk, conn
    except sdk.exceptions.SDKException as e:
        # Probably a cloud configuration/login error
        module.fail_json(msg=str(e))
