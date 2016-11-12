""" This module defines unit tests that can be run from within Quantum's
interactive console.

To run these tests from interactive console:
>>> import test_symengine_cell
>>> test_symengine_cell.run_test()

Alternatively:
>>> exec(open('plugins/PyCell/tests/test_symengine_cell.py').read())
"""
import unittest
import symengine_cell
import symengine
from Quantum import *
from ctrl_command import console_printer


class Test_SymengineCells(unittest.TestCase):

    def setUp(self):
        self.adder = symengine_cell.Add()
        self.adder_cell = QuCell("Quantum::PyCell::Custom::Add")

    def test_add(self):
        x, y = symengine.var('x y')
        self.adder.inputs['a'] = x
        self.adder.inputs['b'] = y
        done = self.adder.process()
        self.assertEqual(done, 0)
        self.assertEqual(self.adder.outputs['f(x)'], (x + y))

    def test_add_cell(self):
        x, y = symengine.var('x y')
        self.adder_cell.inputs['a'] << x
        self.adder_cell.inputs['b'] << y
        done = self.adder_cell.process(0)
        self.assertEqual(done, 0)
        result = []
        self.adder_cell.outputs['f(x)'] >> result
        self.assertEqual(result[-1], (x + y))

@console_printer
def run_test():
    # unittest.main(exit=False)
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_SymengineCells)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == 'builtins':
    run_test()
