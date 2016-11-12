"""
Registry
========

.. important:: New cells must be added to the PyCell registry in order to be
               made available in Quantum runtime.

The registry is part of the PyCell plugin. It is responsible for making all
cells defined in Python available to the runtime system.

This is accomplished by first importing each object into the registry
namespace. The registry then defines a list of dictionaries. Each dictionary
represents a cell. PyCell will iterate through this list to intialize cells.

PyCell expects each cell dictionary to contain the following keys:

:name: The name of the class. This string should match the name exactly.
:module: The module where this class can be found.
:categories: A list of strings representing the category structure to which a
             cell belongs.
"""
from PyCell.sympy_cell import Differentiate, \
    Integrate
from PyCell.symengine_cell import Sympify, \
    Exponentiate, \
    Exp, \
    Expand
from PyCell.utility_cell import Sleep, \
    Print, \
    Start
from PyCell.projection_cell import AstColumn
from PyCell.logic_cell import If, \
    Eq, \
    Gt, \
    Gte, \
    Lt, \
    Lte, \
    Bitwise_Or, \
    Bitwise_And
from PyCell.pylang_cell import Variable, \
    Len, \
    To_List, \
    Add, \
    Subtract, \
    Mul, \
    Div, \
    Int_Div
from PyCell.dataframe_cell import Read_CSV, \
    Head, \
    Tail, \
    Sort_Values, \
    Column, \
    IsNull, \
    NotNull, \
    Select, \
    Sort_Index, \
    Value_Counts, \
    Str_Len, \
    Str_Contains, \
    Str_StartsWith, \
    GroupBy, \
    Set_Index, \
    Unstack, \
    Stack, \
    Year, \
    Month, \
    Day, \
    DayOfWeek, \
    Merge, \
    Pivot, \
    Update
from PyCell.df_cell import Read_CSV_df, \
    Head_df
from PyCell.pygal_cell import Make_Chart, \
    Add_To_Chart

# register paths
import sys
import os

# register cells
py_cells = [
    {
    'name': 'Differentiate',
    'module': 'PyCell.sympy_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'Integrate',
    'module': 'PyCell.sympy_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'Sympify',
    'module': 'PyCell.symengine_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'Exponentiate',
    'module': 'PyCell.symengine_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'Exp',
    'module': 'PyCell.symengine_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'Expand',
    'module': 'PyCell.symengine_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'Sleep',
    'module': 'PyCell.utility_cell',
    'categories': ['Flow Control']
    },
    {
    'name': 'AstColumn',
    'module': 'PyCell.projection_cell',
    'categories': ['Math', 'Numeric']
    },
    {
    'name': 'If',
    'module': 'PyCell.logic_cell',
    'categories': ['Flow Control']
    },
    {
    'name': 'Eq',
    'module': 'PyCell.logic_cell',
    'categories': ['Operators', 'Boolean']
    },
    {
    'name': 'Gt',
    'module': 'PyCell.logic_cell',
    'categories': ['Operators', 'Boolean']
    },
    {
    'name': 'Gte',
    'module': 'PyCell.logic_cell',
    'categories': ['Operators', 'Boolean']
    },
    {
    'name': 'Lt',
    'module': 'PyCell.logic_cell',
    'categories': ['Operators', 'Boolean']
    },
    {
    'name': 'Lte',
    'module': 'PyCell.logic_cell',
    'categories': ['Operators', 'Boolean']
    },
    {
    'name': 'Bitwise_Or',
    'module': 'PyCell.logic_cell',
    'categories': ['Operators', 'Boolean']
    },
    {
    'name': 'Bitwise_And',
    'module': 'PyCell.logic_cell',
    'categories': ['Operators', 'Boolean']
    },
    {
    'name': 'Print',
    'module': 'PyCell.utility_cell',
    'categories': ['Utility']
    },
    {
    'name': 'Start',
    'module': 'PyCell.utility_cell',
    'categories': ['Flow Control']
    },
    {
    'name': 'NumpyColumn',
    'module': 'PyCell.projection_cell',
    'categories': ['Math', 'Numeric']
    },
    {
    'name': 'Variable',
    'module': 'PyCell.pylang_cell',
    'categories': ['Memory']
    },
    {
    'name': 'Add',
    'module': 'PyCell.pylang_cell',
    'categories': ['Operators', 'Algebraic']
    },
    {
    'name': 'Subtract',
    'module': 'PyCell.pylang_cell',
    'categories': ['Operators', 'Algebraic']
    },
    {
    'name': 'Mul',
    'module': 'PyCell.pylang_cell',
    'categories': ['Operators', 'Algebraic']
    },
    {
    'name': 'Int_Div',
    'module': 'PyCell.pylang_cell',
    'categories': ['Operators', 'Algebraic']
    },
    {
    'name': 'Div',
    'module': 'PyCell.pylang_cell',
    'categories': ['Operators', 'Algebraic']
    },
    {
    'name': 'To_List',
    'module': 'PyCell.pylang_cell',
    'categories': ['Memory']
    },
    {
    'name': 'Len',
    'module': 'PyCell.pylang_cell',
    'categories': ['Utility']
    },
    {
    'name': 'Read_CSV',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Import']
    },
    {
    'name': 'Head',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Tail',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Sort_Values',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Column',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'IsNull',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'NotNull',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Select',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Sort_Index',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Value_Counts',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Str_Len',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify', 'String']
    },
    {
    'name': 'Str_Contains',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify', 'String']
    },
    {
    'name': 'Str_StartsWith',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify', 'String']
    },
    {
    'name': 'GroupBy',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Set_Index',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Unstack',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Stack',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Year',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify', 'DateTime']
    },
    {
    'name': 'Month',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify', 'DateTime']
    },
    {
    'name': 'Day',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify', 'DateTime']
    },
    {
    'name': 'DayOfWeek',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify', 'DateTime']
    },
    {
    'name': 'Merge',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Pivot',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Update',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Make_Chart',
    'module': 'PyCell.pygal_cell',
    'categories': ['Data', 'Output']
    },
    {
    'name': 'Add_To_Chart',
    'module': 'PyCell.pygal_cell',
    'categories': ['Data', 'Output']
    },
    {
    'name': 'Read_CSV_df',
    'module': 'PyCell.df_cell',
    'categories': ['Test', 'Import']
    },
    {
    'name': 'Head_df',
    'module': 'PyCell.df_cell',
    'categories': ['Test', 'Modify']
    },
#     {
#     'name': 'Plot',
#     'module': 'PyCell.pygal_cell',
#     'categories': ['Data', 'Output']
#     }
    ]
