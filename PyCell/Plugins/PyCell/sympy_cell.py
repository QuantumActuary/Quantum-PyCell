"""
Sympy 
=====

Provides symbolic math capabilities.
"""
from Quantum import QuReturnCode
from PyCell import registry
from PyCell.custom_cell import Custom
import sympy as sp
from sympy import (diff, integrate, oo, stats)

registry += [
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
    'name': 'Exponentiate',
    'module': 'PyCell.sympy_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'Exp',
    'module': 'PyCell.sympy_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'Ln',
    'module': 'PyCell.sympy_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'Subs',
    'module': 'PyCell.sympy_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'Sqrt',
    'module': 'PyCell.sympy_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'Expand',
    'module': 'PyCell.sympy_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'Symbol',
    'module': 'PyCell.sympy_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'SymFunction',
    'module': 'PyCell.sympy_cell',
    'categories': ['Math', 'Symbolic']
    },
    {
    'name': 'Normal',
    'module': 'PyCell.sympy_cell',
    'categories': ['Statistics', 'Symbolic']
    }
    ]

tf = {'True':'True', 'False':'False'}
OK = QuReturnCode('OK')
QUIT = QuReturnCode('QUIT')

def eval_sym(out_key=None, eval_key='eval', eval_out='result'):
    """
    A decorator for processes that allow calculation of a numeric result. The
    output socket located at ``out_key`` must be a :class:`QuSym`.
    
    :param out_key: The key to the output socket containing a QuSym that
                    includes all values neccessary for evaluation.
    :type out_key: str
    :param eval_key: The input key containing a boolean which determines if
                     a numeric result should be calculated
    :type eval_key: str
    :param eval_out: The output key where the numeric result is written
    :type eval_out: str
    """
    assert isinstance(out_key, str)
    assert isinstance(eval_key, str)
    def magic(process):
        def wrapper(self, *args, **kwargs):
            _eval = self.inputs[eval_key]
            process(self)
            if _eval == True:
                assert isinstance(self.outputs[out_key], QuSym)
                _kwargs = self.outputs[out_key].to_dict()
                vals = _kwargs['values']
                try:
                    _result = self.outputs[out_key].fn(*vals)
                    self.outputs[eval_out] = _result
                except TypeError as e:
                    self.return_msg_ = (
                        f'Unable to calculate result. '
                        f'Unacceptable parameter value in {vals}'
                        )
                    self.return_code = QUIT
        return wrapper
    return magic

class QuSym(object):
    """
    An object that combines symbolic representation with numeric evaluation.
    """
    def __init__(self, expression, variables=None, values=None):
        if isinstance(expression, str):
            assert not isinstance(values, tuple)
            self._expression = sp.Symbol(expression)
            self._variables = (self._expression,)
            self._values = (values,)
        else:
            assert isinstance(expression, sp.Basic)
            assert isinstance(variables, tuple)
            assert isinstance(values, tuple)
            self._expression = expression
            self._variables = variables
            self._values = values

        self._fn = None

    def to_dict(self):
        return {'variables': self._variables, 'values': self._values}
    
    def to_tuples(self):
        return tuple(zip(self._variables, self._values))
    
    def _combine_params(self, other):
        newtups = self.to_tuples()
        to_add = other.to_tuples()
        for tup in to_add:
            if tup not in newtups:
                newtups += (tup,)
        newvars = tuple([i[0] for i in newtups])
        newvals = tuple([i[1] for i in newtups])
        return {'variables': newvars, 'values': newvals}
    
    def __add__(self, other):
        assert isinstance(other, QuSym)
        newsym = self.expression + other.expression
        _kwargs = self._combine_params(other)
        return QuSym(newsym, **_kwargs)

    @property
    def fn(self):
        if self._fn is None:
            self._fn = sp.lambdify(self._variables, self._expression)
        return self._fn
    
    def subs(self, subexpr, replacement):
        assert isinstance(subexpr, QuSym)
        assert isinstance(replacement, QuSym)
        newsym = self.expression.subs(subexpr.expression,
                                      replacement.expression)
        newtups = tuple([x for x in self.to_tuples() if x not in 
                         subexpr.to_tuples()])
        newtups += replacement.to_tuples()
        vars = tuple([i[0] for i in newtups])
        vals = tuple([i[1] for i in newtups])
        return QuSym(newsym, variables=vars, values=vals)

    @property
    def expression(self):
        return self._expression


class Subs(Custom):
    """
    Searches for a subexpression in :math:`f(x)` and substitutes it with the
    expression in ``replacement``.
    
    :param f(x): The expression to search
    :type f(x): QuSym
    :param subexpr: The subexpression to match
    :type subexpr: QuSym
    :param replacement: The expression to use as substitute
    :type replacement: QuSym
    """
    inputs = {'f(x)': None, 'subexpr': None, 'replacement': None, 'eval':tf}
    outputs = {'f(x)': None, 'result': None}
    required = ['f(x)', 'subexpr', 'replacement', 'eval']
    threadsafe = True
    
    def __init__(self):
        self.return_code = OK
        self.return_msg_ = "Ready to go!"
    
    def start(self):
        self.return_code = OK
    
    @eval_sym(out_key='f(x)')
    def _process(self):
        pass
            
    def process(self):
        try:
            self.outputs['f(x)'] = self.inputs['f(x)'].subs(
                self.inputs['subexpr'], self.inputs['replacement']
                )
        except AttributeError:
            if not isinstance(self.inputs['f(x)'], QuSym):
                self.return_msg_ = "Input f(x) must be a QuSym object!"
            else:
                self.return_msg_ = "I don't know what went wrong!"
            self.return_code = QUIT
        self._process()
        return super().process(self.return_code)

class Differentiate(Custom):
    inputs = {'f(x)': None, 'dx': None, 'eval': tf}
    outputs = {'df/dx': None}
    required = ['f(x)', 'dx']

    def process(self):
        self.outputs['df/dx'] = diff(self.inputs['f(x)'], self.inputs['dx'])
        return super().process()


class Integrate(Custom):
    inputs = {'f(x)': None, 'dx': None, 'lower limit':-oo,
              'upper limit': oo}
    outputs = {'F(x)': None}
    required = ['f(x)', 'dx']

    def start(self):
        self.return_code = OK
    
    def process(self):
        self.outputs['F(x)'] = integrate(self.inputs['f(x)'],
                                         (self.inputs['dx'],
                                          self.inputs['lower limit'],
                                          self.inputs['upper limit']))
        return super().process()
    

class Symbol(Custom):
    """
    Creates a symbol.

    :param name: The symbol's name. This is what gets printed in latex output.
    :type name: String
    :param value: The input value that will be used for computation.
    :type value: numeric
    """
    inputs = {'name': None, 'value': None}
    outputs = {'symbol': None}
    required = ['name']
    threadsafe = True

    def start(self):
        self.return_code = OK
    
    def process(self):
        self.outputs['symbol'] = QuSym(self.inputs['name'],
                                       values=self.inputs['value'])

        return super().process()

class SymFunction(Custom):
    """
    Creates an abstract function.

    :param name: The symbol's name. This is what gets printed in latex output.
    :type name: str
    """
    inputs = {'name': None}
    outputs = {'symbol': None}
    required = ['name']
    threadsafe = True

    def __init__(self):
        self.return_code = OK
    
    def process(self):
        self.outputs['symbol'] = sp.Function(self.inputs['name'])
        return super().process()

class Normal(Custom):
    """
    Creates a symbolic normal distribution.

    :param name: Symbolic name of the distribution.
    :type name: String
    :param mean: Mean of the normal distribution
    :type mean: numeric
    :param variance: Variance of the normal distribution
    :type variance: numeric
    """
    inputs = {'name': None, 'mean': None, 'variance': None}
    outputs = {'normal': None}
    required = ['name', 'mean', 'variance']
    threadsafe = True
    # TODO: Allow default values

    def start(self):
        self.return_code = OK
    
    def process(self):
        self.outputs['normal'] = stats.Normal(
            self.inputs['name'], self.inputs['mean'], self.inputs['variance']
            )
        return super().process()
    
class CDF(Custom):
    """
    Converts a symbolic distribution into a callable cumulative distribution.
    """
    inputs = {'distribution': None, 'z': None, 'eval': tf}
    outputs = {'CDF': None, 'result': None}
    required = ['distribution']
    threadsafe = True
    
    def start(self):
        self.return_code = OK
    
    def _process(self):
        pass
    
    def process(self):
        pass

class Exponentiate(Custom):
    """
    Exponentiate base by exp. i.e. :math:`x^y` where :math:`x` is the base and
    :math:`y` is the exponent.
    """
    inputs = {'base': None, 'exp': None, 'eval': tf}
    outputs = {'f(x)': None, 'result': None}
    required = ['base', 'exp', 'eval']
    threadsafe = True
        
    def start(self):
        self.return_msg_ = "Nothing to report!"
        self.return_code = OK

    @eval_sym(out_key='f(x)', eval_key='eval', eval_out='result')
    def _process(self):
        base = self.inputs['base'].expression
        exp = self.inputs['exp'].expression
        try:
            _kwargs = self.inputs['base']._combine_params(self.inputs['exp'])
            outSym = base ** exp
            self.outputs['f(x)'] = QuSym(outSym, **_kwargs)
        except TypeError:
            self.return_msg_ = f'Could not exponentiate {base} by {exp}.'
            self.return_code = QUIT
        
    def process(self):
        self._process()
        return super().process()


class Exp(Custom):
    """Exponentiate :math:`e^x`

    :param x: The exponent.
    :type x: QuSym
    :returns: The symbolic result of exponentiating with base e.
    :rtype: QuSym
    """
    inputs = {'x': None, 'eval': tf}
    outputs = {'f(x)': None, 'result':None}
    required = ['x']
    threadsafe = True
    
    def start(self):
        self.return_code = OK
        self.return_msg_ = "Nothing to report!"
        
    @eval_sym(out_key='f(x)', eval_key='eval', eval_out='result')
    def _process(self):
        _kwargs = self.inputs['x'].to_dict()
        outSym = sp.exp(self.inputs['x'].expression)
        self.outputs['f(x)'] = QuSym(outSym, **_kwargs)
    
    def process(self):
        self._process()
        return super().process(self.return_code)
        
    def return_msg(self):
        return self.return_msg_
    
class Ln(Custom):
    """Natural log :math:`ln(x)`

    :param x: The number to log
    :type x: QuSym
    :returns: The symbolic result of ln(x).
    :rtype: QuSym
    """
    inputs = {'x': None, 'eval': tf}
    outputs = {'f(x)': None, 'result':None}
    required = ['x']
    threadsafe = True
    
    def start(self):
        self.return_code = OK
        self.return_msg_ = "Nothing to report!"
        
    @eval_sym(out_key='f(x)', eval_key='eval', eval_out='result')
    def _process(self):
        _kwargs = self.inputs['x'].to_dict()
        outSym = sp.ln(self.inputs['x'].expression)
        self.outputs['f(x)'] = QuSym(outSym, **_kwargs)
    
    def process(self):
        self._process()
        return super().process(self.return_code)
    
class Sqrt(Custom):
    """Square root :math:`\sqrt{x}`

    :param x: The square root radicand
    :type x: QuSym
    :returns: The symbolic result of :math:`\sqrt{x}`.
    :rtype: QuSym
    """
    inputs = {'x': None, 'eval': tf}
    outputs = {'f(x)': None, 'result':None}
    required = ['x']
    threadsafe = True
    
    def start(self):
        self.return_code = OK
        self.return_msg_ = "Nothing to report!"
        
    @eval_sym(out_key='f(x)', eval_key='eval', eval_out='result')
    def _process(self):
        _kwargs = self.inputs['x'].to_dict()
        outSym = sp.sqrt(self.inputs['x'].expression)
        self.outputs['f(x)'] = QuSym(outSym, **_kwargs)
    
    def process(self):
        self._process()
        return super().process(self.return_code)


class Expand(Custom):
    """Expands the input formula
    """
    inputs = {'f(x)': None, 'eval': tf}
    outputs = {'f(x)': None}
    required = ['f(x)']
    threadsafe = True
    
    def start(self):
        self.return_code = OK

    def process(self):
        for k in self.inputs.keys():
            if isinstance(self.inputs[k], str):
                self.inputs[k] = sp.var(self.inputs[k])
        if self.return_code.status == 'OK':
            self.outputs['f(x)'] = self.inputs['f(x)'].expand()
        return super().process()
