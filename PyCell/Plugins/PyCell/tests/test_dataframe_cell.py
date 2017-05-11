import dataframe_cell
from dataframe_cell import H5
import unittest
import Quantum
from Quantum import QuCell, QuCircuit, QuScheduler
import pandas as pd
from ctrl_console import console_printer
from mogwai.constants import OUT
import csv


class Test_DataFrameCells(unittest.TestCase):
    def setUp(self):
        self.csv = 'titles.csv'

    def test_cell_creation(self):
        c0 = QuCell('Quantum::PyCell::Custom::Read_CSV')
        c0.inputs['csv'] << self.csv
        c0.process(0)
        self.assertTrue(isinstance(c0.outputs['dataframe'].value.df,
                                   pd.DataFrame))

    def test_circuit_editing(self):
        c0 = QuCell('Quantum::PyCell::Custom::Read_CSV')
        c0.inputs['csv'] << self.csv
        c0.inputs['index_col'] << None
        c1 = QuCell('Quantum::PyCell::Custom::Column')
        c1.inputs['columns'] << 'year'
        c2 = QuCell('Quantum::PyCell::Custom::Eq')
        c2.inputs['b'] << 2
        c = QuCircuit()
        c.insert(c0)
        c.insert(c1)
        c.insert(c2)
        c.connect(c0, 'dataframe', c1, 'data')
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


@console_printer
def run_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_DataFrameCells)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == 'builtins':
    run_test()
