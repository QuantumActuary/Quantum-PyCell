""" This module defines unit tests that can be run from within Quantum's
interactive console.

To run these tests from interactive console:
>>> import test_sympy_cell
>>> test_sympy_cell.run_test()

Alternatively:
>>> exec(open('plugins/PyCell/tests/test_sympy_cell.py').read())
"""
import unittest
from sympy import var, diff, integrate
import sympy_cell
from Quantum import *
from ctrl_console import console_printer


class Test_SympyCells(unittest.TestCase):

    def setUp(self):
        self.differ = sympy_cell.Differentiate()
        self.differ_cell = QuCell("Quantum::PyCell::Custom::Differentiate")
        self.integral = sympy_cell.Integrate()
        self.integral_cell = QuCell("Quantum::PyCell::Custom::Integrate")
        self.x = var('x')

    def test_diff(self):
        self.differ.inputs['f(x)'] = self.x ** 2
        self.differ.inputs['dx'] = self.x
        self.differ.process()
        self.assertEqual(self.differ.outputs['df/dx'], 2 * self.x)

    def test_diff_cell(self):
        self.differ_cell.inputs['f(x)'] << self.x ** 2
        self.differ_cell.inputs['dx'] << self.x
        self.differ_cell.process()
        result = []
        self.differ_cell.outputs['df/dx'] >> result
        self.assertEqual(result[-1], diff(self.x ** 2))

    def test_integral(self):
        self.integral.inputs['f(x)'] = 2 * self.x
        self.integral.inputs['dx'] = self.x
        self.integral.inputs['lower limit'] = 0
        self.integral.inputs['upper limit'] = 2
        self.integral.process()
        self.assertEqual(self.integral.outputs['F(x)'], 4)

    def test_integral_cell(self):
        self.integral_cell.inputs['f(x)'] << 2 * self.x
        self.integral_cell.inputs['dx'] << self.x
        self.integral_cell.inputs['lower limit'] << 0
        self.integral_cell.inputs['upper limit'] << 2
        self.integral_cell.process()
        result = []
        self.integral_cell.outputs['F(x)'] >> result
        self.assertEqual(result[-1], 4)


@console_printer
def run_test():
    # unittest.main(exit=False)
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_SympyCells)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == 'builtins':
    run_test()
