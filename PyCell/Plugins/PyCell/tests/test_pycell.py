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
from command import SingletonCommand
import Quantum
from threading import Thread

class TestPyCell(SingletonCommand):
    """
    Run PyCell unit tests.
    """
    def run_all_tests(self):
        test_dataframe_cell.run_test()

    def execute(self):
        self.run_all_tests()
#        t = Thread(target=self.run_all_tests)
#        t.start()

    @property
    def name(self):
        return "test_pycell"

Q = Quantum.QuKernel()
test_pycell = TestPyCell()
Q.COMMANDS[test_pycell.name] = test_pycell.execute
SingletonCommand().app.main.names.update(Q.COMMANDS)
# test_symengine_cell.run_test()
#test_sympy_cell.run_test()
#test_utility_cell.run_test()
#test_projection_cell.run_test()
#test_logic_cell.run_test()
#test_dataframe_cell.run_test()
