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
Test DestroyPool.
"""

import time
import unittest

from stratisd_client_dbus import Manager
from stratisd_client_dbus import Pool
from stratisd_client_dbus import StratisdErrorsGen
from stratisd_client_dbus import get_object

from stratisd_client_dbus._implementation import ManagerSpec

from stratisd_client_dbus._constants import TOP_OBJECT

from .._constants import _DEVICES


from .._misc import checked_call
from .._misc import _device_list
from .._misc import Service


_MN = ManagerSpec.MethodNames

class Destroy1TestCase(unittest.TestCase):
    """
    Test 'destroy' on empty database.

    'destroy' should always succeed on an empty database.
    """
    _POOLNAME = 'deadpool'

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()
        time.sleep(1)
        self._proxy = get_object(TOP_OBJECT)
        self._errors = StratisdErrorsGen.get_object()
        Manager.ConfigureSimulator(self._proxy, denominator=8)

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testExecution(self):
        """
        Destroy should succeed.
        """
        (rc, _) = checked_call(
           Manager.DestroyPool(self._proxy, name=self._POOLNAME),
           ManagerSpec.OUTPUT_SIGS[_MN.DestroyPool]
        )
        self.assertEqual(rc, self._errors.OK)

        (_, rc1, _) = checked_call(
           Manager.GetPoolObjectPath(self._proxy, name=self._POOLNAME),
           ManagerSpec.OUTPUT_SIGS[_MN.GetPoolObjectPath]
        )

        self.assertEqual(rc1, self._errors.POOL_NOTFOUND)


class Destroy2TestCase(unittest.TestCase):
    """
    Test 'destroy' on database which contains the given pool.
    """
    _POOLNAME = 'deadpool'

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()
        time.sleep(1)
        self._proxy = get_object(TOP_OBJECT)
        self._errors = StratisdErrorsGen.get_object()
        Manager.CreatePool(
           self._proxy,
           name=self._POOLNAME,
           redundancy=0,
           force=False,
           devices=[d.device_node for d in _device_list(_DEVICES, 1)]
        )
        Manager.ConfigureSimulator(self._proxy, denominator=8)

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testExecution(self):
        """
        The pool was just created, so must be destroyable.
        """
        (rc, _) = checked_call(
           Manager.DestroyPool(self._proxy, name=self._POOLNAME),
           ManagerSpec.OUTPUT_SIGS[_MN.DestroyPool]
        )

        (_, rc1, _) = checked_call(
           Manager.GetPoolObjectPath(self._proxy, name=self._POOLNAME),
           ManagerSpec.OUTPUT_SIGS[_MN.GetPoolObjectPath],
        )

        if rc is self._errors.OK:
            expected_rc = self._errors.POOL_NOTFOUND
        else:
            expected_rc = self._errors.OK

        self.assertEqual(rc1, expected_rc)


class Destroy3TestCase(unittest.TestCase):
    """
    Test 'destroy' on database which contains the given pool and a volume.
    """
    _POOLNAME = 'deadpool'
    _VOLNAME = 'vol'

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        Create a pool and a filesystem.
        """
        self._service = Service()
        self._service.setUp()

        time.sleep(1)
        self._proxy = get_object(TOP_OBJECT)
        self._errors = StratisdErrorsGen.get_object()
        (poolpath, _, _) = Manager.CreatePool(
           self._proxy,
           name=self._POOLNAME,
           redundancy=0,
           force=False,
           devices=[d.device_node for d in _device_list(_DEVICES, 1)]
        )
        Pool.CreateFilesystems(
           get_object(poolpath),
           specs=[(self._VOLNAME, '', 0)]
        )
        Manager.ConfigureSimulator(self._proxy, denominator=8)

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testExecution(self):
        """
        This should fail since it has a filesystem on it.
        """
        (rc, _) = checked_call(
           Manager.DestroyPool(self._proxy, name=self._POOLNAME),
           ManagerSpec.OUTPUT_SIGS[_MN.DestroyPool]
        )
        self.assertEqual(rc, self._errors.BUSY)
