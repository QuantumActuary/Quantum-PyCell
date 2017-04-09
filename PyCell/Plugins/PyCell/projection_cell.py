"""
Projection
==========
The projection module produces tensors that are intended to represent your
model's time series results.
"""

from PyCell.custom_cell import Custom
from PyCell import registry
import ast
import operator as op
import numpy as np

registry += [
    {
    'name': 'AstColumn',
    'module': 'PyCell.projection_cell',
    'categories': ['Math', 'Numeric']
    },
    {
    'name': 'NumpyColumn',
    'module': 'PyCell.projection_cell',
    'categories': ['Math', 'Numeric']
    },
    ]

# supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}


class AstColumn(Custom):
    """
    AstColumn produces a vector tranformation using t as the input vector and
    f(t) as the transformation function. The function f should be an expression
    in terms of t, and the t socket should contain a list.

    Example::

        >>> a = AstColumn()
        >>> a.inputs['f(t)'] = 't**2'
        >>> a.inputs['t'] = [1, 2, 3, 4]
        >>> a.process()
        0
        >>> a.outputs['ans']
        [1, 4, 9, 16]
    """
    inputs = {'f(t)': 't', 't': []}
    inflows = ['>>']
    outputs = {'ans': []}
    required = ['>>', 'f(t)', 't']
    internal_use = ['>>']

    def __init__(self):
        self.return_msg_ = "No problems boss!"

    def return_msg(self):
        return self.return_msg_

    def process(self):
        expr = str(self.inputs['f(t)'])
        self.outputs['ans'] = [self._eval_expr(expr.replace('t', str(t)))
                               for t in self.inputs['t']]
        return super().process()

    def _eval_expr(self, expr):
        """
        *Internal*. Evaluates a string math expression.

        Example::

            >>> _eval_expr('2^6')
            4
            >>> _eval_expr('2**6')
            64
            >>> _eval_expr('1 + 2*3**(4^5) / (6 + -7)')
            -5.0
        """
        return self._eval(ast.parse(expr, mode='eval').body)


    def _eval(self, node):
        """
        Recursively evaluates a binary syntax tree. Each node is composed of
        other nodes, operators, or numbers. When a node is encountered, a
        a recursion occurs.
        """
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            return operators[type(node.op)](self._eval(node.left),
                                            self._eval(node.right))
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            return operators[type(node.op)](self._eval(node.operand))
        else:
            raise TypeError(node)


class NumpyColumn(Custom):
    """
    NumpyColumn produces a vector tranformation using t as the input vector and
    f(t) as the transformation function. The function f should be an expression
    in terms of t, and the t socket should contain a list.

    Example::

        >>> a = NumpyColumn()
        >>> a.inputs['f(t)'] = 't**2'
        >>> a.inputs['t'] = [1, 2, 3, 4]
        >>> a.process()
        0
        >>> a.outputs['ans']
        array([1, 4, 9, 16])
    """
    inputs = {'f(t)': 't', 't': []}
    inflows = ['>>']
    outputs = {'ans': []}
    required = ['>>', 'f(t)', 't']
    internal_use = ['>>']

    def __init__(self):
        self.return_msg_ = "No problems boss!"

    def return_msg(self):
        return self.return_msg_

    def process(self):
        expr = str(self.inputs['f(t)'])
        t = np.array(self.inputs['t'])
        self.outputs['ans'] = eval(expr)
        return super().process()
