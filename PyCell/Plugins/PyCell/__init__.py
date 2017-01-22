from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__) + "/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]
try:
    __all__.remove('registry')
except:
    pass
registry = [
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
#     {
#     'name': 'Read_CSV_df',
#     'module': 'PyCell.df_cell',
#     'categories': ['Test', 'Import']
#     },
#     {
#     'name': 'Head_df',
#     'module': 'PyCell.df_cell',
#     'categories': ['Test', 'Modify']
#     },
#     {
#     'name': 'Plot',
#     'module': 'PyCell.pygal_cell',
#     'categories': ['Data', 'Output']
#     }
    ]
