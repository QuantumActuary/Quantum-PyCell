import pandas as pd
from PyCell import registry
from PyCell.custom_cell import Custom
from PyCell.custom_cell import exception_raiser
from kivy.clock import mainthread

registry += [
    {
    'name': 'Read_CSV_df',
    'module': 'PyCell.df_cell',
    'categories': ['Test', 'Import']
    },
    {
    'name': 'Head_df',
    'module': 'PyCell.df_cell',
    'categories': ['Test', 'Modify']
    }
    ]


class Read_CSV_df(Custom):
    required = ['csv']

    def __init__(self):
        super().__init__()
        self.inputs = {'csv': None}
        self.outputs = {'dataframe': None}

#     @exception_raiser
    def read_csv(self):
        return pd.read_csv(self.inputs['csv'])

    def process(self):
        self.outputs['dataframe'] = self.read_csv()
        return super().process()


class Head_df(Custom):
    required = ['data']

    def __init__(self):
        super().__init__()
        self.inputs = {'n': 5, 'data': None}
        self.outputs = {'dataframe': None}

    def process(self):
        self.outputs['dataframe'] = self.inputs['data'].head(self.inputs['n'])
        return super().process()