# Copyright 2016 Red Hat, Inc.
#
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

"""
Classes to implement dbus interface.
"""

import abc
import enum
import types

import dbus

from into_dbus_python import xformer


def _xformers(key_to_sig):
    """
    Get a map from keys to functions from a map of names to signatures.

    :param key_to_sig: a map from keys to signatures
    :type key_to_sig: dict of object * str
    :returns: a map from keys to functions
    :rtype: dict of object * xformation function
    """
    sig_to_xformers = \
       dict((sig, xformer(sig)) for (_, sig) in key_to_sig.values())
    return dict((method, (names, sig_to_xformers[sig])) for \
       (method, (names, sig)) in key_to_sig.items())


class InterfaceSpec(abc.ABC):
    """
    Parent class for an interface hierarchy.
    """
    # pylint: disable=too-few-public-methods

    INTERFACE_NAME = abc.abstractproperty(doc="interface name")
    INPUT_SIGS = \
       abc.abstractproperty(doc="map from method name to input signatures")
    OUTPUT_SIGS = \
       abc.abstractproperty(doc="map from method name to output signatures")
    XFORMERS = abc.abstractproperty(doc="map from method name to xformer")
    PROPERTY_NAMES = abc.abstractproperty(doc="list of property names")


class CacheSpec(InterfaceSpec):
    """
    Cache device interface.
    """
    # pylint: disable=too-few-public-methods

    class MethodNames(enum.Enum):
        """
        Names of the methods of the dev interface.
        """
        pass

    class PropertyNames(enum.Enum):
        """
        Names of the properties of the Filesystem interface.
        """
        Size = "Size"

    INTERFACE_NAME = 'org.storage.stratis1.cache'

    INPUT_SIGS = {
    }
    OUTPUT_SIGS = {
    }
    XFORMERS = _xformers(INPUT_SIGS)


class DevSpec(InterfaceSpec):
    """
    Blockdev interface.
    """
    # pylint: disable=too-few-public-methods

    class MethodNames(enum.Enum):
        """
        Names of the methods of the dev interface.
        """
        pass

    class PropertyNames(enum.Enum):
        """
        Names of the properties of the Filesystem interface.
        """
        Size = "Size"

    INTERFACE_NAME = 'org.storage.stratis1.dev'

    INPUT_SIGS = {
    }
    OUTPUT_SIGS = {
    }
    XFORMERS = _xformers(INPUT_SIGS)


class FilesystemSpec(InterfaceSpec):
    """
    Filesystem interface.
    """
    # pylint: disable=too-few-public-methods

    class MethodNames(enum.Enum):
        """
        Names of the methods of the Filesystem class.
        """
        CreateSnapshot = "CreateSnapshot"
        Rename = "Rename"
        SetMountpoint = "SetMountpoint"
        SetQuota = "SetQuota"

    class PropertyNames(enum.Enum):
        """
        Names of the properties of the Filesystem interface.
        """
        pass

    INTERFACE_NAME = 'org.storage.stratis1.filesystem'

    INPUT_SIGS = {
       MethodNames.CreateSnapshot: (("name", ), "s"),
       MethodNames.Rename: (("name", ), "s"),
       MethodNames.SetMountpoint: ((), ""),
       MethodNames.SetQuota: (("quota", ), "s")
    }
    OUTPUT_SIGS = {
       MethodNames.CreateSnapshot: "oqs",
       MethodNames.Rename: "oqs",
       MethodNames.SetMountpoint: "oqs",
       MethodNames.SetQuota: "oqs"
    }
    XFORMERS = _xformers(INPUT_SIGS)


class ManagerSpec(InterfaceSpec):
    """
    Manager interface.
    """
    # pylint: disable=too-few-public-methods

    class MethodNames(enum.Enum):
        """
        The method names of the manager interface.
        """
        ConfigureSimulator = "ConfigureSimulator"
        CreatePool = "CreatePool"
        DestroyPool = "DestroyPool"
        GetCacheObjectPath = "GetCacheObjectPath"
        GetDevObjectPath = "GetDevObjectPath"
        GetDevTypes = "GetDevTypes"
        GetErrorCodes = "GetErrorCodes"
        GetFilesystemObjectPath = "GetFilesystemObjectPath"
        GetPoolObjectPath = "GetPoolObjectPath"
        GetRaidLevels = "GetRaidLevels"
        ListPools = "ListPools"

    class PropertyNames(enum.Enum):
        """
        Names of the properties of the manager interface.
        """
        pass

    INTERFACE_NAME = 'org.storage.stratis1.Manager'

    INPUT_SIGS = {
        MethodNames.ConfigureSimulator : (("denominator", ), "u"),
        MethodNames.CreatePool :
           (("name", "redundancy", "force", "devices"), "sqbas"),
        MethodNames.DestroyPool : (("name", ), "s"),
        MethodNames.GetCacheObjectPath : (("name", ), "s"),
        MethodNames.GetDevObjectPath : (("name", ), "s"),
        MethodNames.GetDevTypes : ((), ""),
        MethodNames.GetErrorCodes : ((), ""),
        MethodNames.GetFilesystemObjectPath :
           (("pool_name", "filesystem_name"), "ss"),
        MethodNames.GetPoolObjectPath : (("name", ), "s"),
        MethodNames.GetRaidLevels : ((), ""),
        MethodNames.ListPools : ((), ""),
    }
    OUTPUT_SIGS = {
        MethodNames.ConfigureSimulator : "qs",
        MethodNames.CreatePool : "oqs",
        MethodNames.DestroyPool : "qs",
        MethodNames.GetCacheObjectPath : "oqs",
        MethodNames.GetDevObjectPath : "oqs",
        MethodNames.GetDevTypes : "",
        MethodNames.GetErrorCodes : "a(sqs)",
        MethodNames.GetFilesystemObjectPath : "oqs",
        MethodNames.GetPoolObjectPath : "oqs",
        MethodNames.GetRaidLevels : "a(sqs)",
        MethodNames.ListPools : "asqs",
    }
    XFORMERS = _xformers(INPUT_SIGS)


class PoolSpec(InterfaceSpec):
    """
    Pool interface.
    """
    # pylint: disable=too-few-public-methods

    class MethodNames(enum.Enum):
        """
        Names of the methods of the Pool class.
        """
        AddCacheDevs = "AddCacheDevs"
        AddDevs = "AddDevs"
        CreateFilesystems = "CreateFilesystems"
        DestroyFilesystems = "DestroyFilesystems"
        ListCacheDevs = "ListCacheDevs"
        ListDevs = "ListDevs"
        ListFilesystems = "ListFilesystems"
        RemoveCacheDevs = "RemoveCacheDevs"
        RemoveDevs = "RemoveDevs"

    class PropertyNames(enum.Enum):
        """
        Names of the properties of the manager interface.
        """
        pass

    INTERFACE_NAME = 'org.storage.stratis1.pool'

    INPUT_SIGS = {
       MethodNames.AddCacheDevs: (("force", "devices", ), "bas"),
       MethodNames.AddDevs: (("force", "devices", ), "bas"),
       MethodNames.CreateFilesystems: (("specs", ), "a(sst)"),
       MethodNames.DestroyFilesystems: (("names", ), "as"),
       MethodNames.ListCacheDevs: ((), ""),
       MethodNames.ListDevs: ((), ""),
       MethodNames.ListFilesystems: ((), ""),
       MethodNames.RemoveCacheDevs: (("names", ), "as"),
       MethodNames.RemoveDevs: (("names", ), "as")
    }
    OUTPUT_SIGS = {
       MethodNames.AddCacheDevs: "a(oqs)qs",
       MethodNames.AddDevs: "a(oqs)qs",
       MethodNames.CreateFilesystems: "a(oqs)qs",
       MethodNames.DestroyFilesystems: "a(qs)qs",
       MethodNames.ListCacheDevs: "asqs",
       MethodNames.ListDevs: "asqs",
       MethodNames.ListFilesystems: "asqs",
       MethodNames.RemoveCacheDevs: "a(qs)qs",
       MethodNames.RemoveDevs: "a(qs)qs"
    }
    XFORMERS = _xformers(INPUT_SIGS)


def _prop_builder(spec):
    """
    Returns a function that builds a property interface based on 'spec'.

    :param spec: the interface specification
    :type spec: type, a subtype of InterfaceSpec
    """

    def builder(namespace):
        """
        The property class's namespace.

        :param namespace: the class's namespace
        """

        def build_property(prop):
            """
            Build a single property getter for this class.

            :param prop: the property
            """

            def dbus_func(proxy_object):
                """
                The property getter.
                """
                return proxy_object.Get(
                   spec.INTERFACE_NAME,
                   prop.name,
                   dbus_interface=dbus.PROPERTIES_IFACE
                )

            return dbus_func

        for prop in spec.PropertyNames:
            namespace[prop.name] = staticmethod(build_property(prop))

    return builder


def _iface_builder(spec):
    """
    Returns a function that builds a method interface based on 'spec'.

    :param spec: the interface specification
    :type spec: type, a subtype of InterfaceSpec
    """

    def builder(namespace):
        """
        Builds the class.

        :param namespace: the class's namespace
        """

        def build_method(method):
            """
            Build a single method for this class.

            :param method: the method
            """
            (names, func) = spec.XFORMERS[method]

            def dbus_func(proxy_object, **kwargs):
                """
                The function method spec.
                """
                if frozenset(names) != frozenset(kwargs.keys()):
                    raise ValueError("Bad keys")
                args = \
                   [v for (k, v) in \
                   sorted(kwargs.items(), key=lambda x: names.index(x[0]))]
                xformed_args = func(args)
                dbus_method = getattr(proxy_object, method.name)
                return dbus_method(
                   *xformed_args,
                   dbus_interface=spec.INTERFACE_NAME
                )

            return dbus_func

        for method in spec.MethodNames:
            namespace[method.name] = staticmethod(build_method(method))

        namespace['Properties'] = \
           types.new_class(
              "Properties",
              bases=(object,),
              exec_body=_prop_builder(spec)
           )

    return builder


Cache = types.new_class(
   "Cache",
   bases=(object,),
   exec_body=_iface_builder(CacheSpec)
)
Dev = types.new_class("Dev", bases=(object,), exec_body=_iface_builder(DevSpec))
Filesystem = types.new_class(
   "Filesystem",
   bases=(object,),
   exec_body=_iface_builder(FilesystemSpec)
)
Manager = types.new_class(
   "Manager",
   bases=(object,),
   exec_body=_iface_builder(ManagerSpec)
)
Pool = \
   types.new_class("Pool", bases=(object,), exec_body=_iface_builder(PoolSpec))
