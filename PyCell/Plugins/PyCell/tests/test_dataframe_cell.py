import dataframe_cell
import unittest
import Quantum
from Quantum import QuCell, QuCircuit, QuScheduler
import pandas as pd
from ctrl_command import console_printer
from mogwai.constants import OUT
import csv


class Test_DataFrameCells(unittest.TestCase):
    def setUp(self):
        pass

    def test_circuit_editing(self):
        csv = '/Users/Thomas/pycon-pandas-tutorial-master/data/titles.csv'
#         d = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'c']),
#              'two': pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
#         df = pd.DataFrame(d)
        c0 = QuCell('Quantum::PyCell::Custom::From_CSV')
        c0.inputs['csv'] << csv
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
        out = []
        c2.outputs['result'] >> out
        self.assertTrue(isinstance(out[0], pd.Series))
#         print(out[-1])
        c.remove(c2)
        c3 = QuCell('Quantum::PyCell::Custom::Eq')
        c3.inputs['b'] << 1
        c.insert(c3)
        c.connect(c1, 'data', c3, 'a')
        s2 = QuScheduler(c)
        s2.execute(1)
        c3.outputs['result'] >> out
        self.assertTrue(isinstance(out[-1], pd.Series))
#         print(out[-1])


@console_printer
def run_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_DataFrameCells)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == 'builtins':
    run_test()
