import unittest
import projection_cell
import Quantum
from Quantum import QuCell, QuCircuit
from ctrl_console import console_printer


class Test_AstColumnCells(unittest.TestCase):

    def setUp(self):
        self.col = projection_cell.AstColumn()
        self.col_cell = QuCell("Quantum::PyCell::Custom::AstColumn")
        self.starter_cell = QuCell("Quantum::PyCell::Custom::Start")
        self.starter_cell.process()
        self.tester = QuCircuit()
        self.tester.insert(self.col_cell)
        self.tester.insert(self.starter_cell)
        self.tester.connect(self.starter_cell, '>>', self.col_cell, '>>')

    def test_astcolumn(self):
        self.col.inputs['f(t)'] = '2*t'
        self.col.inputs['t'] = [1, 2]
        self.col.process()
        self.assertTrue(self.col.outputs['ans'] == [2, 4])

    def test_astcolumn_cell(self):
        self.col_cell.inputs['f(t)'] << '2**t'
        self.col_cell.inputs['t'] << [1, 2, 3]
        self.col_cell.process()
        result = []
        self.col_cell.outputs['ans'] >> result
        self.assertTrue(result[-1], [2, 4, 16])


@console_printer
def run_test():
    # unittest.main(exit=False)
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_AstColumnCells)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == 'builtins':
    run_test()