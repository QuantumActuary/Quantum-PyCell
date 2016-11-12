import unittest
import logic_cell
import Quantum
from Quantum import QuCell, QuCircuit
from ctrl_command import console_printer


class Test_LogicCells(unittest.TestCase):

    def setUp(self):
        self.iffer = logic_cell.If()
        self.iffer_cell = QuCell("Quantum::PyCell::Custom::If")
        self.starter_cell = QuCell("Quantum::PyCell::Custom::Start")
        self.starter_cell.process()
        self.tester = QuCircuit()
        self.tester.insert(self.iffer_cell)
        self.tester.insert(self.starter_cell)
        self.tester.connect(self.starter_cell, '>>', self.iffer_cell, '>>')

    def test_if(self):
        self.iffer.inputs['condition'] = True
        self.iffer.process()
        self.assertEqual(self.iffer.outflows['true >>'], Quantum.OK)
        self.assertEqual(self.iffer.outflows['false >>'], Quantum.UNKNOWN)

        self.iffer.inputs['condition'] = False
        self.iffer.process()
        self.assertEqual(self.iffer.outflows['false >>'], Quantum.OK)
        self.assertEqual(self.iffer.outflows['true >>'], Quantum.UNKNOWN)

    def test_if_cell(self):
        self.iffer_cell.inputs['condition'] << False
        self.iffer_cell.process()
        result = []
        self.iffer_cell.outputs['true >>'] >> result
        self.assertEqual(result[-1], Quantum.UNKNOWN)
        self.iffer_cell.outputs['false >>'] >> result
        self.assertEqual(result[-1], Quantum.OK)

        self.iffer_cell.inputs['condition'] << True
        self.iffer_cell.process()
        self.iffer_cell.outputs['true >>'] >> result
        self.assertEqual(result[-1], Quantum.OK)
        self.iffer_cell.outputs['false >>'] >> result
        self.assertEqual(result[-1], Quantum.UNKNOWN)

@console_printer
def run_test():
    # unittest.main(exit=False)
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_LogicCells)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == 'builtins':
    run_test()
