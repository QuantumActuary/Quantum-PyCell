import dataframe_cell
from dataframe_cell import H5
import unittest
import Quantum
from Quantum import QuCell, QuCircuit, QuScheduler
import pandas as pd
from ctrl_console import console_printer


class Test_DataFrameCells(unittest.TestCase):
    def setUp(self):
        self.csv = 'titles.csv'
        self.csv_cell = QuCell('Quantum::PyCell::Custom::Read_CSV')
        self.csv_cell.inputs['csv'] << self.csv

    def test_read_csv_cell(self):
        self.csv_cell.process(0)
        self.assertTrue(isinstance(self.csv_cell.outputs['dataframe'].value.df,
                                   pd.DataFrame))

    def test_circuit_editing(self):
        self.csv_cell.inputs['index_col'] << None
        c1 = QuCell('Quantum::PyCell::Custom::Column')
        c1.inputs['columns'] << 'year'
        c2 = QuCell('Quantum::PyCell::Custom::Eq')
        c2.inputs['b'] << 2
        c = QuCircuit()
        c.insert(self.csv_cell)
        c.insert(c1)
        c.insert(c2)
        c.connect(self.csv_cell, 'dataframe', c1, 'data')
        c.connect(c1, 'data', c2, 'a')
        s = QuScheduler(c)
        s.execute(1)
        out = c2.outputs['result'].value
        self.assertTrue(isinstance(out.df, pd.Series))
        c.remove(c2)
        c3 = QuCell('Quantum::PyCell::Custom::Eq')
        c3.inputs['b'] << 1
        c.insert(c3)
        c.connect(c1, 'data', c3, 'a')
        s2 = QuScheduler(c)
        s2.execute(1)
        out = c3.outputs['result'].value
        self.assertTrue(isinstance(out.df, pd.Series))

    def test_head_cell(self):
        head = QuCell('Quantum::PyCell::Custom::Head')
        c = QuCircuit()
        c.insert(head)
        c.insert(self.csv_cell)
        c.connect(self.csv_cell, 'dataframe', head, 'data')
        s = QuScheduler(c)
        s.execute(1)
        # test default value
        self.assertEqual(len(head.outputs['dataframe'].value.df), 5)

        # test using a value other than default
        head.inputs['n'] << 10
        s.execute(1)
        self.assertEqual(len(head.outputs['dataframe'].value.df), 10)

        # test using non-number input
        head.inputs['n'] << 'a'
        s.execute(1)
        self.assertEqual(len(head.outputs['dataframe'].value.df), 5)

    def test_tail_cell(self):
        tail = QuCell('Quantum::PyCell::Custom::Tail')
        c = QuCircuit()
        c.insert(tail)
        c.insert(self.csv_cell)
        c.connect(self.csv_cell, 'dataframe', tail, 'data')
        s = QuScheduler(c)
        s.execute(1)
        # test default value
        self.assertEqual(len(tail.outputs['dataframe'].value.df), 5)

        # test using a value other than default
        tail.inputs['n'] << 10
        s.execute(1)
        self.assertEqual(len(tail.outputs['dataframe'].value.df), 10)

        # test using non-number input
        tail.inputs['n'] << 'a'
        s.execute(1)
        self.assertEqual(len(tail.outputs['dataframe'].value.df), 5)


@console_printer
def run_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_DataFrameCells)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == 'builtins':
    run_test()
