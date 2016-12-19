"""
Logic
=====

Logic cells are graph nodes that determine the branching structure of process
execution.
"""
from Quantum import QuReturnCode
from PyCell.custom_cell import Custom


class If(Custom):
    """
    A switch element that determines which cell will be executed next.

    **Inputs**

    :\>\>: Execution pin. Receives an execution token from upstream connection.
    :condition: A boolean value that determines which output pin recieves the
                next execution token.

    **Outputs**

    :true \>\>: Connects to the cell to execute if true.
    :false \>\>: Connects to the cell to execute if false.
    """
    required = ['condition', '>>']
    internal_use = ['>>']

    def __init__(self):
        self.return_msg_ = "All is quiet..."
        self.inputs = {'condition': True}
        self.inflows = ['>>']
        self.outflows = {'true >>': QuReturnCode.str2int['UNKNOWN'],
                         'false >>': QuReturnCode.str2int['UNKNOWN']}

    def return_msg(self):
        return self.return_msg_

    def process(self):
        if self.inputs['condition']:
            self.outflows['true >>'] = QuReturnCode.str2int['OK']
            self.outflows['false >>'] = QuReturnCode.str2int['UNKNOWN']
        else:
            self.outflows['false >>'] = QuReturnCode.str2int['OK']
            self.outflows['true >>'] = QuReturnCode.str2int['UNKNOWN']

        return super().process()


class Eq(Custom):
    """
    Tests for equality.

    :param a: Left operand.
    :param b: Right operand.
    :returns: Whether or not ``a==b``.
    """
    required = ['a', 'b']

    def __init__(self):
        self.return_msg_ = 'Ready to test equality.'
        self.inputs = {'a': None, 'b': None}
        self.outputs = {'result': None}

    def process(self):
        self.outputs['result'] = (self.inputs['a'] == self.inputs['b'])
        self.return_msg_ = 'Testing done.'
        return super().process()


class Gt(Custom):
    """
    Greater than.

    :param a: Left operand.
    :param b: Right operand.
    :returns: Whether or not ``a>b``.
    """
    required = ['a', 'b']

    def __init__(self):
        self.return_msg_ = 'Ready to test greater than.'
        self.inputs = {'a': None, 'b': None}
        self.outputs = {'result': None}

    def process(self):
        self.outputs['result'] = (self.inputs['a'] > self.inputs['b'])
        self.return_msg_ = 'Testing done.'
        return super().process()


class Gte(Custom):
    """
    Greater than or equal.

    :param a: Left operand.
    :param b: Right operand.
    :returns: Whether or not ``a>=b``.
    """
    required = ['a', 'b']

    def __init__(self):
        self.return_msg_ = 'Ready to test greater than or equal.'
        self.inputs = {'a': None, 'b': None}
        self.outputs = {'result': None}

    def process(self):
        self.outputs['result'] = (self.inputs['a'] >= self.inputs['b'])
        self.return_msg_ = 'Testing done.'
        return super().process()


class Lt(Custom):
    """
    Less than.

    :param a: Left operand.
    :param b: Right operand.
    :returns: Whether or not ``a<b``.
    """
    required = ['a', 'b']

    def __init__(self):
        self.return_msg_ = 'Ready to test less than.'
        self.inputs = {'a': None, 'b': None}
        self.outputs = {'result': None}

    def process(self):
        self.outputs['result'] = (self.inputs['a'] < self.inputs['b'])
        self.return_msg_ = 'Testing done.'
        return super().process()


class Lte(Custom):
    """
    Less than or equal.

    :param a: Left operand.
    :param b: Right operand.
    :returns: Whether or not ``a<=b``.
    """
    required = ['a', 'b']

    def __init__(self):
        self.return_msg_ = 'Ready to test less than or equal.'
        self.inputs = {'a': None, 'b': None}
        self.outputs = {'result': None}

    def process(self):
        self.outputs['result'] = (self.inputs['a'] <= self.inputs['b'])
        self.return_msg_ = 'Testing done.'
        return super().process()


class Bitwise_Or(Custom):
    """
    Bitwise or operator.

    :param a: Left operand.
    :param b: Right operand.
    :returns: Whether or not ``a|b``.
    """
    required = ['a', 'b']

    def __init__(self):
        self.return_msg_ = 'Ready to |.'
        self.inputs = {'a': None, 'b': None}
        self.outputs = {'result': None}

    def process(self):
        self.outputs['result'] = (self.inputs['a'] | self.inputs['b'])
        self.return_msg_ = 'Bitwise | done.'
        return super().process()


class Bitwise_And(Custom):
    """
    Bitwise and operator.

    :param a: Left operand.
    :param b: Right operand.
    :returns: Whether or not ``a&b``.
    """
    required = ['a', 'b']

    def __init__(self):
        self.return_msg_ = 'Ready to &.'
        self.inputs = {'a': None, 'b': None}
        self.outputs = {'result': None}

    def process(self):
        self.outputs['result'] = (self.inputs['a'] & self.inputs['b'])
        self.return_msg_ = 'Bitwise & done.'
        return super().process()
