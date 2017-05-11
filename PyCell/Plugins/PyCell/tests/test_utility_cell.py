import utility_cell
import unittest
import Quantum
from Quantum import QuCell, QuCircuit, QuReturnCode
from ctrl_console import console_printer


class Test_UtilityCells(unittest.TestCase):

    def setUp(self):
        self.sleeper = utility_cell.Sleep()
        self.sleeper_cell = QuCell("Quantum::PyCell::Custom::Sleep")
        self.starter_cell = QuCell("Quantum::PyCell::Custom::Start")
        self.starter_cell.process()
        self.tester = QuCircuit()
        self.tester.insert(self.sleeper_cell)
        self.tester.insert(self.starter_cell)
        self.tester.connect(self.starter_cell, '>>', self.sleeper_cell, '>>')

    def test_sleep(self):
        self.sleeper.inputs['seconds'] = 1
        self.sleeper.process()
        self.assertTrue(self.sleeper.outputs['done'])

    def test_sleep_cell(self):
        self.sleeper_cell.inputs['seconds'] << 1
        self.sleeper_cell.process()
        result = []
        self.sleeper_cell.outputs['done'] >> result
        self.assertTrue(result[-1])

    def test_starter_cell(self):
        result = self.starter_cell.process()
        self.assertEqual(result, QuReturnCode('OK').returncode)


@console_printer
def run_test():
    # unittest.main(exit=False)
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_UtilityCells)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == 'builtins':
    run_test()
