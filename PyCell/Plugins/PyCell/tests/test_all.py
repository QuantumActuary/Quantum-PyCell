""" This module defines unit tests that can be run from within Quantum's
interactive console.

To run these tests from interactive console:
>>> exec(open('plugins/PyCell/tests/test_all.py').read())
"""
# import test_symengine_cell
import test_sympy_cell
import test_utility_cell
import test_projection_cell
import test_logic_cell
import test_dataframe_cell

# test_symengine_cell.run_test()
test_sympy_cell.run_test()
test_utility_cell.run_test()
test_projection_cell.run_test()
test_logic_cell.run_test()
test_dataframe_cell.run_test()
