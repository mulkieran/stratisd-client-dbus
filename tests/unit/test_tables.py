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
Test invariants on tables in implementation.
"""


import unittest

from stratisd_client_dbus import Cache
from stratisd_client_dbus import Dev
from stratisd_client_dbus import Filesystem
from stratisd_client_dbus import Manager
from stratisd_client_dbus import Pool

from stratisd_client_dbus._implementation import CacheSpec
from stratisd_client_dbus._implementation import DevSpec
from stratisd_client_dbus._implementation import FilesystemSpec
from stratisd_client_dbus._implementation import ManagerSpec
from stratisd_client_dbus._implementation import PoolSpec

_GENERATED_CLASSES = (Cache, Dev, Filesystem, Manager, Pool)
_SPEC_CLASSES = (CacheSpec, DevSpec, FilesystemSpec, ManagerSpec, PoolSpec)

class KeysTestCase(unittest.TestCase):
    """
    Test that every map contains all the designated keys.
    """

    def testSpecTables(self):
        """
        Test that *Spec maps are correct.
        """
        for klass in _SPEC_CLASSES:
            methods = frozenset(klass.MethodNames)
            self.assertEqual(methods, frozenset(klass.INPUT_SIGS.keys()))
            self.assertEqual(methods, frozenset(klass.OUTPUT_SIGS.keys()))
            self.assertEqual(methods, frozenset(klass.XFORMERS.keys()))


class GeneratedClassTestCase(unittest.TestCase):
    """
    Test the structure of generated classes.
    """

    def testParts(self):
        """
        Verify that every class has a Properties attribute.
        """
        for klass in _GENERATED_CLASSES:
            self.assertTrue(hasattr(klass, "Properties"))

    def testProperties(self):
        """
        Verify that every class has the set of property names required by
        corresponding spec.
        """
        for (spec, klass) in zip(_SPEC_CLASSES, _GENERATED_CLASSES):
            properties = getattr(klass, "Properties")
            for name in spec.PropertyNames:
                self.assertTrue(hasattr(properties, name.name))

    def testMethods(self):
        """
        Verify that every class has the set of method names required by the
        corresponding spec.
        """
        for (spec, klass) in zip(_SPEC_CLASSES, _GENERATED_CLASSES):
            for name in spec.MethodNames:
                self.assertTrue(hasattr(klass, name.name))
