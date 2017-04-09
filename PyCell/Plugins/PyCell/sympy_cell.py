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
    },
    {
    'name': 'CDF',
    'module': 'PyCell.sympy_cell',
    'categories': ['Statistics', 'Symbolic']
    },
    {
    'name': 'Calculate',
    'module': 'PyCell.sympy_cell',
    'categories': ['Math', 'Symbolic']
    }
    ]

tf = {'True':'True', 'False':'False'}
OK = QuReturnCode('OK')
QUIT = QuReturnCode('QUIT')

def eval_sym(out_key=None, in_key=None, eval_key='eval', eval_out='result'):
    """
    A decorator for processes that allow calculation of a numeric result. The
    output socket located at ``out_key`` must be a :class:`QuSym`. Optionally,
    an ``in_key`` may be supplied if the formula is found in an input. The
    formula must be supplied in at least one of the two. If both are supplied,
    the output formula will have priority.
    
    :param out_key: The key to the output socket containing a QuSym that
                    includes all values neccessary for evaluation.
    :type out_key: str
    :param in_key: The key to the input socket containing a QuSym that
                   includes all values neccessary for evaluation.
    :type in_key: str
    :param eval_key: The input key containing a boolean which determines if
                     a numeric result should be calculated. Optionally, you can
                     supply a boolean directly.
    :type eval_key: str or bool
    :param eval_out: The output key where the numeric result is written
    :type eval_out: str
    """
    def magic(process):
        def wrapper(self, *args, **kwargs):
            try:
                _eval = self.inputs[eval_key]
            except KeyError:
                _eval = eval_key
            ret = process(self)
            if _eval == True:
                fml = None
                if out_key is not None:
#                    assert isinstance(self.outputs[out_key], QuSym)
                    fml = self.outputs[out_key]
                else:
#                    assert isinstance(self.inputs[in_key], QuSym)
                    fml = self.inputs[in_key]
                _kwargs = fml.to_dict()
                vals = _kwargs['values']
                try:
                    _result = fml.fn(*vals)
                    self.outputs[eval_out] = _result
                except TypeError as e:
                    self.return_msg_ = (
                        f'Unable to calculate result. '
                        f'Unacceptable parameter value in {vals}'
                        )
                    ret = QUIT
            return ret
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
 
    def _op(self, expr, other):
        _kwargs = self.to_dict()
        try:
            _kwargs = self._combine_params(other)
        except AttributeError:
            pass
        return QuSym(expr, **_kwargs)
    
    def __add__(self, other):
        val = None
        try:
            val = other.expression
        except AttributeError:
            val = other
        return self._op(self.expression + val, other)
    
    def __sub__(self, other):
        val = None
        try:
            val = other.expression
        except AttributeError:
            val = other
        return self._op(self.expression - val, other)
    
    def __mul__(self, other):
        val = None
        try:
            val = other.expression
        except AttributeError:
            val = other
        return self._op(self.expression * val, other)
    
    def __matmul__(self, other):
        val = None
        try:
            val = other.expression
        except AttributeError:
            val = other
        return self._op(self.expression @ val, other)
    
    def __truediv__(self, other):
        val = None
        try:
            val = other.expression
        except AttributeError:
            val = other
        return self._op(self.expression / val, other)
    
    def __floordiv__(self, other):
        val = None
        try:
            val = other.expression
        except AttributeError:
            val = other
        return self._op(self.expression // val, other)
    
    def __mod__(self, other):
        val = None
        try:
            val = other.expression
        except AttributeError:
            val = other
        return self._op(self.expression % val, other)
    
    def __pow__(self, other):
        val = None
        try:
            val = other.expression
        except AttributeError:
            val = other
        return self._op(self.expression ** val, other)

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
    
    def __str__(self):
        return str(self.expression)


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
        self.return_msg_ = "Ready to go!"
    
    @eval_sym(out_key='f(x)')        
    def process(self):
        ret = OK
        try:
            self.outputs['f(x)'] = self.inputs['f(x)'].subs(
                self.inputs['subexpr'], self.inputs['replacement']
                )
        except AttributeError:
            if not isinstance(self.inputs['f(x)'], QuSym):
                self.return_msg_ = "Input f(x) must be a QuSym object!"
            else:
                self.return_msg_ = "I don't know what went wrong!"
            ret = QUIT
        return super().process(code=ret)

class Differentiate(Custom):
    inputs = {'f(x)': None, 'x': None, 'eval': tf}
    outputs = {'df/dx': None, 'result': None}
    required = ['f(x)', 'x']
    threadsafe = True
    
    @eval_sym(out_key='df/dx')
    def process(self):
#        assert isinstance(self.inputs['f(x)'], QuSym)
#        assert isinstance(self.inputs['x'], QuSym)
        
        dfdx = diff(
            self.inputs['f(x)'].expression, self.inputs['x'].expression
            )
        _kwargs = self.inputs['f(x)']._combine_params(self.inputs['x'])
        self.outputs['df/dx'] = QuSym(dfdx, **_kwargs)
        return super().process()


class Integrate(Custom):
    inputs = {'f(x)': None, 'dx': None, 'lower limit':-oo,
              'upper limit': oo}
    outputs = {'F(x)': None}
    required = ['f(x)', 'dx']
    
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
    
    @eval_sym(out_key='CDF', eval_key='eval', eval_out='result')
    def process(self):
        assert isinstance(self.inputs['distribution'],
                          sp.stats.rv.RandomSymbol)
        assert isinstance(self.inputs['z'], QuSym)
        dist = stats.cdf(self.inputs['distribution'])
        expr = dist(self.inputs['z'].expression)
        _kwargs = self.inputs['z'].to_dict()
        self.outputs['CDF'] = QuSym(expr, **_kwargs)
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
        self.return_msg_ = "Nothing to report!"
        
    @eval_sym(out_key='f(x)', eval_key='eval', eval_out='result')
    def process(self):
        _kwargs = self.inputs['x'].to_dict()
        outSym = sp.exp(self.inputs['x'].expression)
        self.outputs['f(x)'] = QuSym(outSym, **_kwargs)
        return super().process()
    
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
    def process(self):
        _kwargs = self.inputs['x'].to_dict()
        outSym = sp.ln(self.inputs['x'].expression)
        self.outputs['f(x)'] = QuSym(outSym, **_kwargs)
        return super().process()
    
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
    def process(self):
        _kwargs = self.inputs['x'].to_dict()
        outSym = sp.sqrt(self.inputs['x'].expression)
        self.outputs['f(x)'] = QuSym(outSym, **_kwargs)
        return super().process()


class Calculate(Custom):
    """
    Converts a QuSym into a function and calculates the value given supplied
    input variables.
    """
    inputs = {'f(x)': None}
    outputs = {'result': None}
    required = ['f(x)']
    threadsafe = False
    
    @eval_sym(in_key='f(x)', eval_key=True)
    def process(self):
        return super().process()

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
