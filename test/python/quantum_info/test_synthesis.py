# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""Tests for quantum synthesis methods."""

import unittest
import math
import scipy.linalg as la
import numpy as np

from qiskit import execute
from qiskit.quantum_info.operators.measures import process_fidelity
from qiskit.quantum_info.synthesis import two_qubit_kak
from qiskit.quantum_info.operators import Unitary
from qiskit.providers.basicaer import UnitarySimulatorPy
from qiskit.exceptions import QiskitError
from qiskit.test import QiskitTestCase


class TestSynthesis(QiskitTestCase):
    """Test synthesis methods."""

    def test_two_qubit_kak(self):
        """Verify KAK decomposition for random Haar 4x4 unitaries.
        """
        for _ in range(100):
            unitary = Unitary.random(4)
            with self.subTest(unitary=unitary):
                decomp_circuit = two_qubit_kak(unitary)
                result = execute(decomp_circuit, UnitarySimulatorPy()).result()
                decomp_unitary = Unitary(result.get_unitary())
                self.assertAlmostEqual(
                        process_fidelity(unitary.representation, decomp_unitary.representation),
                        1.0,
                        places=7
                )


if __name__ == '__main__':
    unittest.main()
