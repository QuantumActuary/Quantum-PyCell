"""
Dataframe
=========

Provides Pandas DataFrame functions.
"""
import Quantum
from Quantum import QuReturnCode, QuCellSocket
import os
import sys
import pandas as pd
from PyCell import registry
from PyCell.custom_cell import Custom, ValidInputs, exception_raiser
# import matplotlib.pyplot as plt
from kivy.clock import mainthread
from multiprocessing import Process, Pipe

registry += [
    {
    'name': 'Read_CSV',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Query']
    },
    {
    'name': 'Head',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Query']
    },
    {
    'name': 'Tail',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Query']
    },
    {
    'name': 'Sort_Values',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Modify']
    },
    {
    'name': 'Column',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Query']
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
    'categories': ['Data', 'Query']
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
    'categories': ['Data', 'Query']
    },
    {
    'name': 'Iloc',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Query']
    },
    {
    'name': 'Loc',
    'module': 'PyCell.dataframe_cell',
    'categories': ['Data', 'Query']
    }
    ]

plugin_cache = os.path.join(os.environ['HOME'], '.kivy', '__cache__')
os.makedirs(plugin_cache, exist_ok=True)


def data_process(func):
    """
    Decorator for cell processes that execute a dataframe operation. It creates
    a new node in the data store that holds the return value for the wrapped
    generator. This result is then wrapped back up into an H5 and returned,
    where it is expected to be put into an output socket for the next cell to
    use.

    .. note::
       This decorator runs the decorated function in a separate processor and
       therefore, will not emit any print statements.
    """
    def process_func(*args, **kwargs):
#        assert isinstance(args[0], Custom), 'args[0] must be self'
        file = '{}.h5'.format(args[0].py_id)
        node = 'c{}'.format(args[0].py_id)
        if not isinstance(args[1], H5):
            raise TypeError('args[1] must be an H5')

        @exception_raiser
        def multi_process(conn, file, node, func, *new_args, **kwargs):
            try:
                df = func(*args, **kwargs)
                data_cols = args[1].data_columns
                H5(file, node, df, data_columns=data_cols)
                conn.send(True)
            except:
                print("Error creating {}".format(file))
                conn.send(False)
                raise

        parent_conn, child_conn = Pipe()
        largs = (child_conn, file, node, func, *args)
        p = Process(target=multi_process, args=largs, kwargs=kwargs)
        p.start()
        p.join(10)
        if parent_conn.recv():
            new_h5 = H5(file, node)
        else:
            print("Error creating {}".format(file))
            new_h5 = None
        return new_h5
    return process_func


def operator_process(op):
    """
    Documentation coming soon.
    """
    def do_func(func):
        def process_operator(*args, **kwargs):
            new_args = list(args)
            try:
                # convert the second argument to a df if it's an H5
                new_args[1] = args[1].df
            except:
                pass
            finally:
                node2 = '{}_{}_{}'.format(op, id(args[0]), id(args[1]))

            @exception_raiser
            def multi_operate(conn, node, func, *args, **kwargs):
                try:
                    df = func(*args, **kwargs)
                    H5('{}.h5'.format(node), node, df)
                    conn.send(True)
                except:
                    print("Error creating {}.h5".format(node))
                    conn.send(False)
                    raise

            parent_conn, child_conn = Pipe()
            largs = (child_conn, node2, func, *new_args)
            p = Process(target=multi_operate, args=largs, kwargs=kwargs)
            p.start()
            p.join()
            if parent_conn.recv():
                new_h5 = H5('{}.h5'.format(node2), node2)
            else:
                print("Error creating {}.h5".format(node2))
                new_h5 = None
            return new_h5

        return process_operator
    return do_func


class H5(object):
    """
    Proxy object for hdf5 storage. Used as a lightweight communication object
    between dataframe cell sockets.

    :param node: A group label.
    :type node: string
    """
#     write_lock = Lock()

    @classmethod
    def write_store(cls, df, file, node, **kwargs):
        store = pd.HDFStore(os.path.join(plugin_cache, file), complevel=9,
                            complib='blosc')
        store.put(node, df, format='table', **kwargs)
        store.close()

    def __init__(self, file, node='/', df=None, **kwargs):
        if df is not None:
            H5.write_store(df, file, node, **kwargs)
        self.node = node
        """The node that this H5 object represents."""
        self.file = file

    @property
    def store(self):
        """
        .. warning:: This is not thread-safe. Do not attempt to access from
                     multiple threads without a locking mechanism.
        """
        return pd.get_store(os.path.join(plugin_cache, self.file), mode='r')

    @property
    def df(self):
        """
        The dataframe.
        """
        df = pd.read_hdf(os.path.join(plugin_cache, self.file),
                         key=self.node)
        return df

    @property
    def columns(self):
        """
        Provides a column index iterable.
        """
        cols = pd.read_hdf(os.path.join(plugin_cache, self.file),
                           start=0, stop=1).columns
        return cols

    @property
    def data_columns(self):
        """
        Provides an iterable of columns that are indexed as data.
        """
        with self.store as store:
            storer = store.get_storer(self.node)
            dc = storer.data_columns
        return dc

    def select(self, *args, **kwargs):
        """
        Executes a select operation on the hdf5 object.
        """
        sel = pd.read_hdf(os.path.join(plugin_cache, self.file),
                          *args, key=self.node, **kwargs)
        return sel

    def select_column(self, *args, **kwargs):
        """
        Grabs a series from the store.
        """
        with self.store as store:
            col = store.select_column(self.node, *args, **kwargs)
        return col

    def __str__(self):
        return str(self.df)

    # Comparison Operators
    @operator_process('eq')
    def __eq__(self, other):
        return self.df == other

    @operator_process('lt')
    def __lt__(self, other):
        return self.df < other

    @operator_process('le')
    def __le__(self, other):
        return self.df <= other

    @operator_process('gt')
    def __gt__(self, other):
        return self.df > other

    @operator_process('ge')
    def __ge__(self, other):
        return self.df >= other

    @operator_process('ne')
    def __ne__(self, other):
        return self.df != other

    # Binary Operators
    @operator_process('add')
    def __add__(self, other):
        return self.df + other

    @operator_process('sub')
    def __sub__(self, other):
        return self.df - other

    @operator_process('mul')
    def __mul__(self, other):
        return self.df * other

    @operator_process('floordiv')
    def __floordiv__(self, other):
        return self.df // other

    @operator_process('truediv')
    def __truediv__(self, other):
        return self.df / other

    @operator_process('mod')
    def __mod__(self, other):
        return self.df % other

    @operator_process('pow')
    def __pow__(self, other):
        return self.df ** other

    @operator_process('and')
    def __and__(self, other):
        return self.df & other

    @operator_process('xor')
    def __xor__(self, other):
        return self.df ^ other

    @operator_process('or')
    def __or__(self, other):
        return self.df | other


class Read_CSV(Custom):
    """
    Converts a csv file to a DataFrame.

    :param csv: *Required*. The string could be a URL. Valid URL schemes
                include http, ftp, s3, and file. For file URLs, a host is
                expected. For instance, a local file could be file
                ``://localhost/path/to/table.csv``
    :type csv: str, pathlib.Path, py._path.local.LocalPath or any object with
               a read() method (such as a file handle or StringIO)
    :param index_col: Column to use as the row labels of the DataFrame. If a
                      sequence is given, a MultiIndex is used. If you have a
                      malformed file with delimiters at the end of each line,
                      you might consider index_col=False to force pandas to
                      _not_ use the first column as the index (row names)
    :type index_col: int or sequence or False, default None
    :param parse_dates: Determines if dates should be auto-parsed.

                        - boolean. If True -> try parsing the index.
                        - list of ints or names. e.g. If ``[1, 2, 3]`` -> try
                          parsing columns 1, 2, 3 each as a separate date
                          column.
                        - list of lists. e.g. If ``[[1, 3]]`` -> combine
                          columns 1 and 3 and parse as a single date column.
                        - dict, e.g. ``{‘foo’ : [1, 3]}`` -> parse columns 1, 3
                          as date and call result ``‘foo’``
    :type parse_dates: boolean or list of ints or names or list of lists or
                       dict, default False
    :param infer_datetime_format: If ``True`` and parse_dates is enabled for a
                                  column, attempt to infer the datetime format
                                  to speed up the processing.
    :type infer_datetime_format: boolean, default False
    :param data_columns: Columns to index
    :type data_columns: list
    :param min_itemsize: Specification of minimum field sizes. The parameter
                         should be a dict of fieldnames for keys and integers
                         for their respective sizes. ex: {'A':10, 'B':100}
    :type min_itemsize: dict
    :returns: The parsed csv file.
    :rtype: H5
    """
    infer_datetime_format = {'True': 'True', 'False': 'False'}
    inputs = {'csv': None, 'index_col': None, 'parse_dates': None,
              'infer_datetime_format': {}, 'data_columns': []}
    outputs = {'dataframe': None}
    required = ['csv']

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Give me a csv file!'
        self.inputs['infer_datetime_format'] = Read_CSV.infer_datetime_format

    def read_csv(self):
        kwargs = {}
        if not self.inputs['index_col'] == '':
            kwargs['index_col'] = self.inputs['index_col']
        if not self.inputs['parse_dates'] == '':
            kwargs['parse_dates'] = self.inputs['parse_dates']
        if not self.inputs['infer_datetime_format'] == '':
            kwargs['infer_datetime_format'] = (
                                self.inputs['infer_datetime_format'])

        dfkwargs = {}
        if self.inputs['data_columns'] is not None:
            dfkwargs['data_columns'] = self.inputs['data_columns']

        node = os.path.splitext(os.path.basename(self.inputs['csv']))[0]
        file = '{}.h5'.format(node)

        def read_file(file, node, dfkwargs, **kwargs):
            df = pd.read_csv(self.inputs['csv'], **kwargs)
            if 'data_columns' in dfkwargs.keys():
                if not isinstance(dfkwargs['data_columns'], bool):
                    df.set_index(dfkwargs['data_columns'])
            H5(file, node, df, **dfkwargs)

        largs = (file, node, dfkwargs)
        p = Process(target=read_file, args=largs, kwargs=kwargs)
        p.start()
        p.join()
        h5 = H5(file, node)
        return h5

    def process(self):
        self.outputs['dataframe'] = self.read_csv()
        return super().process()


class Iloc(Custom):
    """
    Create a dataframe subset using the `iloc` function.

    :param axis0: Rows to return by position
    :type axis0: int, list of int, slice
    :param axis1: Columns to return by position
    :type axis1: int, list of int, slice
    :param data: *Required*. The source data.
    :type data: H5
    :returns: The requested rows and columns.
    :rtype: H5
    """
    inputs = {'axis0': None, 'axis1': None, 'data': None}
    outputs = {'dataframe': None}
    required = ['data']

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'I\'m ready!'

    @data_process
    def iloc(self, h5):
        df = None
        if self.inputs['axis1'] is None:
            df = h5.df.iloc[self.inputs['axis0']]
        else:
            df = h5.df.iloc[self.inputs['axis0'], self.inputs['axis1']]
        return df

    def process(self):
        self.outputs['dataframe'] = self.iloc(self.inputs['data'])
        return super().process()


class Loc(Custom):
    """
    Create a dataframe subset using the `loc` function.

    :param axis0: Rows to return by label
    :type axis0: label, list of labels
    :param axis1: Columns to return by label
    :type axis1: label, list of labels
    :param data: *Required*. The source data.
    :type data: H5
    :returns: The requested rows and columns.
    :rtype: H5
    """
    inputs = {'axis0': None, 'axis1': None, 'data': None}
    outputs = {'dataframe': None}
    required = ['data']

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'I\'m ready!'

    @data_process
    def loc(self, h5):
        df = None
        if self.inputs['axis1'] is None:
            df = h5.df.loc[self.inputs['axis0']]
        else:
            df = h5.df.loc[self.inputs['axis0'], self.inputs['axis1']]
        return df

    def process(self):
        self.outputs['dataframe'] = self.loc(self.inputs['data'])
        return super().process()


class Head(Custom):
    """
    Creates a new dataframe from the first few rows of the input DataFrame.

    :param rows: Number of rows to return.
    :type rows: int
    :param data: *Required*. The source data.
    :type data: H5
    :returns: The requested number rows.
    :rtype: H5
    """
    required = ['data']
    inputs = ValidInputs(n=5, data=None)
    outputs = {'dataframe': None}


    def __init__(self):
        super().__init__()
        self.return_msg_ = 'I\'m ready!'
        self.inputs['n'].set_validator(self.validate_n)
        self.inputs['data'] = None

    @data_process
    def head(self, h5):
        return h5.df.head(self.inputs['n'].value)

    def validate_n(self, val):
        if not isinstance(val, int):
            self.inputs['n'] << Head.inputs['n'].value
            return False
        return True

    def process(self):
        self.outputs['dataframe'] = self.head(self.inputs['data'].value)
        return super().process()


class Tail(Custom):
    """
    Creates a new dataframe from the last few rows of the input DataFrame.

    :param rows: Number of rows to return.
    :type rows: int
    :param data: *Required*. The source data.
    :type data: DataFrame
    :returns: The requested number rows.
    :rtype: H5
    """
    inputs = ValidInputs({'n': 5, 'data': None})
    outputs = {'dataframe': None}
    required = ['data']

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'I\'m ready!'
        self.inputs['n'].set_validator(self.validate_n)
        self.inputs['data'] = None

    @data_process
    def tail(self, h5):
        return h5.df.tail(self.inputs['n'].value)

    def validate_n(self, val):
        if not isinstance(val, int):
            self.inputs['n'] << Tail.inputs['n'].value
            return False
        return True

    def process(self):
        self.outputs['dataframe'] = self.tail(self.inputs['data'].value)
        return super().process()


class Sort_Values(Custom):
    """
    Sorts a dataframe using a list of columns, or sorts a series using its
    values column.

    :param data: *Required*. Data to sort.
    :type data: DataFrame or Series
    :param column_list: Order by these columns. If the data is a Series, then
                        this parameter should be None.
    :type column_list: list or None
    :returns: The sorted data
    :rtype: H5
    """
    required = ['data']
    inputs = {'data': None, 'column_list': []}
    outputs = {'data': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to sort.'

    @data_process
    def sort_values(self, h5):
        if not isinstance(h5.df, pd.Series):
            df = h5.df.sort_values(self.inputs['column_list'])
        else:
            df = h5.df.sort_values()
        return df

    def process(self):
        self.outputs['data'] = self.sort_values()
        self.return_msg_ = 'Sorted'
        return super().process()


class Column(Custom):
    """
    Create a new DataFrame or Series by specifying a subset of column names.

    :param columns: *Required*. A single column name or a list of column names.
                    If a single column is specified, the result will be a
                    Pandas Series. Otherwise, the result will be another
                    DataFrame.
    :type columns: string or list
    :param data: *Required*. The original DataFrame.
    :type data: DataFrame
    :returns: A subset of columns from the original data.
    :rtype: H5

    .. tip:: If ``columns`` is a list, the result will be a dataframe. If it
              is a single string, the result will be a series.
    """
    required = ['data', 'columns']
    inputs = {'data': None, 'columns': []}
    outputs = {'data': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to select columns!'

    @data_process
    def column(self, h5):
        cols = self.inputs['columns']
        try:
            if not isinstance(cols, list):
                df = h5.select_column(column=cols)
            else:
                df = h5.select(columns=cols)
        except:
            df = h5.df.loc[:, cols]
        return df

    def process(self):
        self.return_msg_ = 'Selecting column...'
        self.outputs['data'] = self.column(self.inputs['data'])
        self.return_msg_ = 'Selected'
        return super().process(QuReturnCode('OK'))


class IsNull(Custom):
    """
    Checks for NaN elements in a Series

    :param series: *Required*. The data to check.
    :type series: Series
    :returns: A Series indicating where elements of the input are NaN.
    :rtype: H5
    """
    required = ['series']
    inputs = {'series': None}
    outputs = {'series': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to filter for nulls!'

    @data_process
    def isnull(self, h5):
        return h5.df.isnull()

    def process(self):
        self.outputs['series'] = self.isnull(self.inputs['series'])
        self.return_msg_ = 'Checked for nulls.'
        return super().process()


class NotNull(Custom):
    """
    Checks for non-NaN elements in a Series

    :param series: *Required*. The data to check.
    :type series: Series
    :returns: A Series indicating where elements of the input are not NaN.
    :rtype: H5
    """
    required = ['series']
    inputs = {'series': None}
    outputs = {'series': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to filter for nulls!'

    @data_process
    def notnull(self, h5):
        return h5.df.notnull()

    def process(self):
        self.outputs['series'] = self.notnull(self.inputs['series'])
        self.return_msg_ = 'Checked for nulls.'
        return super().process()


class Select(Custom):
    """
    Create a new DataFrame from an existing one based on a boolean Series.

    :param data: *Required*. The source data.
    :type data: DataFrame
    :param sieve: *Required*. A boolean Series used as a filter.
    :type sieve: Series
    :param expression: Conditions used for the where clause of a query.
    :type expression: string
    :returns: A subset of data.
    :rtype: H5
    """
    required = ['data']
    inputs = {'data': None, 'sieve': None, 'expression': ''}
    outputs = {'dataframe': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to select.'


    @data_process
    def select(self, h5):
        if self.is_valid_input(self.inputs['sieve']):
            s = self.inputs['sieve'].df
            return h5.df[s]
        elif self.is_valid_input(self.inputs['expression']):
            return h5.select(where=self.inputs['expression'])
        else:
            return h5.df

    def process(self):
        self.outputs['dataframe'] = self.select(self.inputs['data'])
        self.return_msg_ = 'Data is filtered.'
        return super().process()


class Sort_Index(Custom):
    """
    Sorts a Series by its index.

    :param series: *Required*. The data to sort.
    :type series: Series
    :returns: The sorted data.
    :rtype: H5
    """
    required = ['series']
    inputs = {'series': None}
    outputs = {'series': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to sort.'

    @data_process
    def sort_index(self, h5):
        return h5.df.sort_index()

    def process(self):
        self.outputs['series'] = self.sort_index(self.inputs['series'])
        self.return_msg_ = 'Series is sorted.'
        return super().process()


class Value_Counts(Custom):
    """
    Count by index of a Series.

    :param series: *Required*. The data to tally.
    :type series: Series
    :returns: The tallied data.
    :rtype: H5
    """
    required = ['series']
    inputs = {'series': None}
    outputs = {'series': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to tally.'

    @data_process
    def value_counts(self, h5):
        return h5.df.value_counts()

    def process(self):
        self.outputs['series'] = self.value_counts(self.inputs['series'])
        self.return_msg_ = 'Series is tallied.'
        return super().process()


class Str_Len(Custom):
    """
    Determines the length of each string in a Series.

    :param series: *Required*. The series of string data.
    :type series: Series
    :returns: A new Series with calculated lengths of strings.
    :rtype: H5
    """
    required = ['series']
    inputs = {'series': None}
    outputs = {'series': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to len.'

    @data_process
    def str_len(self, h5):
        return h5.df.str.len()

    def process(self):
        self.outputs['series'] = self.str_len(self.inputs['series'])
        self.return_msg_ = 'Series is calculated.'
        return super().process()


class Str_Contains(Custom):
    """
    Determines if a substring can be matched to each string of a Series.

    :param series: *Required*. The series of string data.
    :type series: Series
    :param substring: The string to match.
    :type substring: string
    :returns: A new Series indicating if a match was successful.
    :rtype: H5
    """
    required = ['series']
    inputs = {'series': None, 'substring': None}
    outputs = {'series': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to match substring.'

    @data_process
    def str_contains(self, h5):
        string = self.inputs['substring']
        return h5.df.str.contains(string)

    def process(self):
        self.outputs['series'] = self.str_contains(self.inputs['series'])
        self.return_msg_ = 'Strings have been searched.'
        return super().process()


class Str_StartsWith(Custom):
    """
    Determines if a substring can be matched to the beginning of each string of
    a Series.

    :param series: *Required*. The series of string data.
    :type series: Series
    :param substring: The string to match.
    :type substring: string
    :returns: A new Series indicating if a match was successful.
    :rtype: H5
    """
    required = ['series']
    inputs = {'series': None, 'substring': None}
    outputs = {'series': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to match substring.'

    @data_process
    def str_startswith(self, h5):
        string = self.inputs['substring']
        return h5.df.str.startswith(string)

    def process(self):
        self.outputs['series'] = self.str_startswith(self.inputs['series'])
        self.return_msg_ = 'Strings have been searched.'
        return super().process()


class GroupBy(Custom):
    """
    Group a dataframe by specific columns. Columns can be calculated on the fly
    and supplied to groupby as a list element.

    :param dataframe: *Required*. The dataframe used for the grouping
                      operation.
    :type dataframe: DataFrame
    :param columns: *Required*. The name(s) of columns to group by. This can
                    also be an expression operating on a Series. For multiple
                    columns a list is required.
    :type columns: string
    :param aggregation: The method used to summarize groups.
    :type aggregation: string
    :returns: Grouped data.
    :rtype: H5
    """
    aggregation = {'size': 'size', 'min': 'min', 'mean': 'mean', 'max': 'max'}
    required = ['dataframe', 'columns']
    inputs = {'dataframe': None, 'columns': None, 'aggregation': {}}
    outputs = {'data': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to group data.'
        self.inputs['aggregation'] = GroupBy.aggregation

    def start(self):
        self.return_msg_ = 'Starting to process.'

    def stop(self):
        self.return_msg_ = 'Finished process.'

    @data_process
    def groupby(self, h5):
        method = 'size'  # set the default
        if self.inputs['aggregation'] != GroupBy.aggregation:
            method = self.inputs['aggregation']

        if method == 'min':
            return h5.df.groupby(self.inputs['columns']).min()
        elif method == 'mean':
            return h5.df.groupby(self.inputs['columns']).mean()
        elif method == 'max':
            return h5.df.groupby(self.inputs['columns']).max()
        else:
            return h5.df.groupby(self.inputs['columns']).size()

    def process(self):
        self.outputs['data'] = self.groupby(self.inputs['dataframe'])
        self.return_msg_ = 'Data is grouped.'
        return super().process()


class Set_Index(Custom):
    """
    Assign indexes to a dataframe to speed up data retrievals.

    :param dataframe: *Required*. The data to re-index.
    :type dataframe: DataFrame
    :param columns: *Required*. A single column name or a list of column names.
    :type columns: String
    :returns: Re-indexed data.
    :rtype: H5
    """
    required = ['dataframe', 'columns']
    inputs = {'dataframe': None, 'columns': None}
    outputs = {'dataframe': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to re-index data.'

    @data_process
    def set_index(self, h5):
        return h5.df.set_index(self.inputs['columns'])

    def process(self):
        self.outputs['dataframe'] = self.set_index(self.inputs['dataframe'])
        self.return_msg_ = 'Data is reindexed.'
        return super().process()


class Unstack(Custom):
    """
    Pivot a level of the (necessarily hierarchical) index labels, returning a
    DataFrame having a new level of column labels whose inner-most level
    consists of the pivoted index labels. If the index is not a MultiIndex, the
    output will be a Series (the analogue of stack when the columns are not a
    MultiIndex). The level involved will automatically get sorted.

    :param data: *Required*. The data to unstack.
    :type data: DataFrame or Series
    :param level: Level(s) of index to unstack, can pass level name
    :type level: int, string, or list of these, default -1 (last level)
    :param fill_value: replace NaN with this value if the unstack produces
                       missing values.
    :type fill_value: any
    :returns: Unstacked data.
    :rtype: H5
    """
    required = ['data']
    inputs = {'data': None, 'level':-1, 'fill_value': None}
    outputs = {'data': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to unstack data.'

    @data_process
    def unstack(self, h5):
        if self.is_valid_input(self.inputs['level']):
            # overwrite default
            level = self.inputs['level']

        if self.is_valid_input(self.inputs['fill_value']):
            # overwrite default
            fill = self.inputs['fill_value']

        return h5.df.unstack(level, fill)

    def process(self):
        self.outputs['data'] = self.unstack(self.inputs['data'])
        self.return_msg_ = 'Data is unstacked.'
        return super().process()


class Stack(Custom):
    """
    Pivot a level of the (possibly hierarchical) column labels, returning a
    DataFrame (or Series in the case of an object with a single level of column
    labels) having a hierarchical index with a new inner-most level of row
    labels. The level involved will automatically get sorted.

    :param data: *Required*. The data to unstack.
    :type data: DataFrame or Series
    :param level: Level(s) of index to stack, can pass level name
    :type level: int, string, or list of these, default -1 (last level)
    :param dropna: Whether to drop rows in the resulting Frame/Series with no
                   valid values
    :type dropna: boolean, default True
    :returns: Unstacked data.
    :rtype: H5
    """
    required = ['data']
    inputs = {'data': None, 'level':-1, 'dropna': True}
    outputs = {'data': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to stack data.'

    @data_process
    def stack(self, h5):
        if self.is_valid_input(self.inputs['level']):
            level = self.inputs['level']

        if self.is_valid_input(self.inputs['dropna']):
            dropna = self.inputs['dropna']

        return h5.df.stack(level, dropna)

    def process(self):
        self.outputs['data'] = self.stack(self.inputs['data'])
        self.return_msg_ = 'Data stacked.'
        return super().process()


class Year(Custom):
    """
    Extract the year from a datetime Series.

    :param series: *Required*. A Series containing dates.
    :type series: Series
    :returns: A Series containing only the years from the input dates.
    :rtype: H5
    """
    required = ['series']
    inputs = {'series': None}
    outputs = {'series': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to extract year.'

    @data_process
    def year(self, h5):
        return h5.df.dt.year

    def process(self):
        self.outputs['series'] = self.year(self.inputs['series'])
        self.return_msg_ = 'Year extracted to new series!'
        return super().process()


class Month(Custom):
    """
    Extract the month from a datetime Series.

    :param series: *Required*. A Series containing dates.
    :type series: Series
    :returns: A Series containing only the months from the input dates.
    :rtype: H5
    """
    required = ['series']
    inputs = {'series': None}
    outputs = {'series': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to extract month.'

    @data_process
    def month(self, h5):
        return h5.df.dt.month

    def process(self):
        self.outputs['series'] = self.month(self.inputs['series'])
        self.return_msg_ = 'Month extracted to new series!'
        return super().process()


class Day(Custom):
    """
    Extract the day from a datetime Series.

    :param series: *Required*. A Series containing dates.
    :type series: Series
    :returns: A Series containing only the days from the input dates.
    :rtype: H5
    """
    required = ['series']
    inputs = {'series': None}
    outputs = {'series': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to extract day.'

    @data_process
    def day(self, h5):
        return h5.df.dt.day

    def process(self):
        self.outputs['series'] = self.day(self.inputs['series'])
        self.return_msg_ = 'Day extracted to new series!'
        return super().process()


class DayOfWeek(Custom):
    """
    Extract the day of week from a datetime Series.

    :param series: *Required*. A Series containing dates.
    :type series: Series
    :returns: A Series containing only the days of week from the input dates.
    :rtype: H5
    """
    required = ['series']
    inputs = {'series': None}
    outputs = {'series': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to extract day of week.'

    @data_process
    def dayofweek(self, h5):
        return h5.df.dt.dayofweek

    def process(self):
        self.outputs['series'] = self.dayofweek(self.inputs['series'])
        self.return_msg_ = 'Day of week extracted to new series!'
        return super().process()


class Merge(Custom):
    """
    Merge DataFrame objects by performing a database-style join operation by
    columns or indexes.

    If joining columns on columns, the DataFrame indexes will be ignored.
    Otherwise if joining indexes on indexes or indexes on a column or columns,
    the index will be passed on.

    :param A: The left operand of a merge.
    :type A: DataFrame
    :param B: The right operand of a merge.
    :type B: DataFrame
    :param how: The method to use for merging.

                - left: use only keys from left frame (SQL: left outer join)
                - right: use only keys from right frame (SQL: right outer join)
                - outer: use union of keys from both frames (SQL: full outer
                  join)
                - inner: use intersection of keys from both frames (SQL: inner
                  join)
    :type how: 'left', 'right', 'outer', 'inner', default 'inner'
    :param on: Field names to join on. Must be found in both DataFrames. If on
               is None and not merging on indexes, then it merges on the
               intersection of the columns by default.
    :type on: label or list
    :param left_on: Field names to join on in left DataFrame. Can be a vector
                    or list of vectors of the length of the DataFrame to use a
                    particular vector as the join key instead of columns.
    :type left_on: label or list, or array-like
    :param right_on: Field names to join on in right DataFrame or vector/list
                     of vectors per left_on docs.
    :type right_on: label or list, or array-like
    :param left_index: Use the index from the left DataFrame as the join
                       key(s). If it is a MultiIndex, the number of keys in the
                       other DataFrame (either the index or a number of
                       columns) must match the number of levels.
    :type left_index: boolean, default False
    :param right_index: Use the index from the right DataFrame as the join key.
                        Same caveats as left_index.
    :type right_index: boolean, default False
    :param sort: Sort the join keys lexicographically in the result DataFrame.
    :type sort: boolean, default False
    :param suffixes: Suffix to apply to overlapping column names in the left
                     and right side, respectively.
    :type suffixes: 2-length sequence (tuple, list, ...)
    :param copy: If False, do not copy data unnecessarily
    :type copy: boolean, default True

    :returns: The merged result.
    :rtype: H5
    """
    how = {'left': 'left', 'right': 'right', 'outer': 'outer',
           'inner': 'inner'}
    required = ['A', 'B']
    inputs = {'A': None, 'B': None, 'how': {}, 'on': None,
              'left_on': None, 'right_on': None, 'left_index': False,
              'right_index': False, 'sort': False, 'suffixes': None,
              'copy': True}
    outputs = {'dataframe': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to merge.'
        self.inputs['how'] = Merge.how

    @data_process
    def merge(self, h5):
        kwargs = {}
        if self.is_valid_input(self.inputs['how']):
            kwargs['how'] = self.inputs['how']

        if self.is_valid_input(self.inputs['on']):
            kwargs['on'] = self.inputs['on']

        if self.is_valid_input(self.inputs['left_on']):
            kwargs['left_on'] = self.inputs['left_on']

        if self.is_valid_input(self.inputs['right_on']):
            kwargs['right_on'] = self.inputs['right_on']

        if self.is_valid_input(self.inputs['left_index']):
            kwargs['left_index'] = self.inputs['left_index']

        if self.is_valid_input(self.inputs['right_index']):
            kwargs['right_index'] = self.inputs['right_index']

        if self.is_valid_input(self.inputs['sort']):
            kwargs['sort'] = self.inputs['sort']

        if self.is_valid_input(self.inputs['suffixes']):
            kwargs['suffixes'] = self.inputs['suffixes']

        if self.is_valid_input(self.inputs['copy']):
            kwargs['copy'] = self.inputs['copy']

        h5b = self.inputs['B']
        assert isinstance(h5b, H5), 'Socket B must be an H5 type.'

        if kwargs:
            df = h5.df.merge(h5b.df, **kwargs)
        else:
            df = h5.df.merge(h5b.df)

        # merge indices
        first = set(h5.data_columns)
        second = set(h5b.data_columns)
        data_cols = list(first | second)
        # use the merged index
        df.set_index(data_cols, inplace=True)
        return df

    def process(self):
        self.outputs['dataframe'] = self.merge(self.inputs['A'])
        self.return_msg_ = 'I have merged!'
        return super().process()


class Pivot(Custom):
    """
    Reshape data (produce a “pivot” table) based on column values. Uses unique
    values from index / columns to form axes and return either DataFrame or
    Panel, depending on whether you request a single value column (DataFrame)
    or all columns (Panel).

    :param dataframe: *Required*. The data to pivot.
    :type dataframe: DataFrame
    :param index: Column name to use to make new frame’s index. If None, uses
                  existing index.
    :type index: string or object
    :param columns: *Required*. Column name to use to make new frame’s columns.
    :type columns: string or object
    :param values: Column name to use for populating new frame’s values.
    :type values: string or object

    .. tip:: The pivot operation is a special case of a sequence of more
              primitive operations-- set_index, sort_index, unstack in that
              order. Finer control can be achieved by using the generalized
              operations.
    """
    required = ['dataframe', 'columns']
    inputs = {'dataframe': None, 'index': None, 'columns': None,
              'values': None}
    outputs = {'dataframe': None}

    def __init__(self):
        super().__init__()
        self.return_msg_ = 'Ready to pivot.'

    @data_process
    def pivot(self, h5):
        kwargs = {}
        if super().is_valid_input(self.inputs['index'], allow_none=True):
            kwargs['index'] = self.inputs['index']
        if super().is_valid_input(self.inputs['values']):
            kwargs['values'] = self.inputs['values']

        kwargs['columns'] = self.inputs['columns']
        return h5.df.pivot(**kwargs)

    def process(self):
        self.outputs['dataframe'] = self.pivot(self.inputs['dataframe'])
        self.return_msg_ = 'Data is pivoted!'
        return super().process()


class Update(Custom):
    """
    Updates values of a specific column inside of a DataFrame. If a column
    doesn't exist, it will be automatically created.

    :param dataframe: *Required*. The dataframe that recieves the updates.
    :type dataframe: DataFrame
    :param column: *Required*. The dataframe column that recieves the updates.
    :type column: string
    :param rows: A series of True and False that determines which rows get
                 updates.
    :type rows: Series
    :param values: *Required*. The values to write into the dataframe. The
                   row index should correspond to the row index of the
                   dataframe.
    :type values: Series
    :returns: The updated data.
    :rtype: H5
    """
    inputs = {'data': None, 'rows': None, 'column': None, 'values': None}
    outputs = {'data': None}
    required = ['data', 'column', 'values']

    def __init__(self):
        super().__init__()
        self.return_msg_ = "Ready to update data."

    @data_process
    def update(self, h5):
        assert isinstance(self.inputs['data'], H5), \
            "dataframe must be an H5."
        df = h5.df
        if self.inputs['rows'] == '':
            df.loc[:, self.inputs['column']] = self.inputs['values'].df
        else:
            assert isinstance(self.inputs['rows'].df, pd.Series), \
                "rows must be a Series."
            df.loc[self.inputs['rows'].df, self.inputs['column']] = \
                self.inputs['values'].df
        return df

    def process(self):
        self.outputs['data'] = self.update(self.inputs['data'])
        self.return_msg_ = 'Data updated!'
        if isinstance(self.outputs['data'], H5):
            return super().process(QuReturnCode('OK'))
        else:
            return super().process(QuReturnCode('UNKNOWN'))
