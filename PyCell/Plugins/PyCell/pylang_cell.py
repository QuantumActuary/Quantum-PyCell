"""
Pylang
======

The pylang plugin provides common python functions.
"""
from PyCell.custom_cell import Custom


class Variable(Custom):
    """
    Declares a Python variable.

    :param value: *Required*. The value held by the variable.
    :type value: any
    """
    inputs = {'value': None}
    outputs = {'value': None}
    required = ['value']

    def __init__(self):
        self.return_msg_ = 'Set my value!'

    def process(self):
        self.outputs['value'] = self.inputs['value']
        self.return_msg_ = 'My value has been set.'
        return super().process()


class To_List(Custom):
    """
    Wraps an object into a list with the object as the single element in the
    list.

    :param obj: *Required*. The object to be put into the empty list.
    :type obj: any
    :return: A list with a single element.
    :rtype: list
    """
    inputs = {'obj': None}
    outputs = {'list': []}
    required = ['obj']

    def __init__(self):
        self.return_msg_ = 'Ready to listify.'

    def process(self):
        try:
            # unwrap H5 objects
            item = self.inputs['obj'].df
        except:
            item = self.inputs['obj']
        self.outputs['list'] = [item]
        self.return_msg_ = 'I made a list!'
        return super().process()


class Len(Custom):
    """
    Calls ``len()`` on an iterable object.

    :param obj: *Required*. An iterable object.
    :type obj: any
    :return: The length of the object.
    :rtype: int
    """
    inputs = {'obj': []}
    outputs = {'len': 0}
    required = ['obj']

    def __init__(self):
        self.return_msg_ = 'Give me something to len!'

    def process(self):
        result = self.inputs['obj']
        result = len(result)
        self.outputs['len'] = result
        self.return_msg_ = 'I counted!'
        return super().process()


class Add(Custom):
    """
    Adds two objects.

    :param a: *Required*. Left operand.
    :param b: *Required*. Right operand.
    :param type: Indicates the type of operation, whether it should add using
                 default python behavior or add symbolically.
    :returns: The result of ``a+b``.
    """
    inputs = {'type': {'Symbolic': 'Symbolic', 'Default': 'Default'},
              'a': None, 'b': None}
    outputs = {'result': None}
    required = ['a', 'b']

    def __init__(self):
        self.return_msg_ = 'Ready to add stuff.'

    def configure(self):
        self.type = 'Default'
        if self.inputs['type'] is None or self.inputs['type'] == '':
            self.type = 'Default'
        else:
            self.type = self.inputs['type']

        if self.type == 'Symbolic':
#             from symengine import var
            from sympy import var
            for k in self.required:
                if isinstance(self.inputs[k], str):
                    self.inputs[k] = var(self.inputs[k])

    def process(self):
        self.outputs['result'] = self.inputs['a'] + self.inputs['b']
        self.return_msg_ = 'I added a and b.'
        return super().process()


class Subtract(Custom):
    """
    Adds two objects.

    :param a: *Required*. Left operand.
    :param b: *Required*. Right operand.
    :param type: Indicates the type of operation, whether it should add using
                 default python behavior or add symbolically.
    :returns: The result of ``a-b``.
    """
    inputs = {'type': {'Symbolic': 'Symbolic', 'Default': 'Default'},
              'a': None, 'b': None}
    outputs = {'result': None}
    required = ['a', 'b']

    def __init__(self):
        self.return_msg_ = 'Ready to subtract stuff.'

    def configure(self):
        self.type = 'Default'
        if self.inputs['type'] is None or self.inputs['type'] == '':
            self.type = 'Default'
        else:
            self.type = self.inputs['type']

        if self.type == 'Symbolic':
            from symengine import var
            for k in self.required:
                if isinstance(self.inputs[k], str):
                    self.inputs[k] = var(self.inputs[k])

    def process(self):
        self.outputs['result'] = self.inputs['a'] - self.inputs['b']
        self.return_msg_ = 'I subtracted b from a.'
        return super().process()


class Mul(Custom):
    """
    Multiplies two objects.

    :param a: *Required*. Left operand.
    :param b: *Required*. Right operand.
    :param type: Indicates the type of operation, whether it should multiply
                 using default python behavior or add symbolically.
    :returns: The result of ``a*b``.
    """
    inputs = {'type': {'Symbolic': 'Symbolic', 'Default': 'Default'},
              'a': None, 'b': None}
    outputs = {'result': None}
    required = ['a', 'b']

    def __init__(self):
        self.return_msg_ = 'Ready to multiply stuff.'

    def configure(self):
        self.type = 'Default'
        if self.inputs['type'] is None or self.inputs['type'] == '':
            self.type = 'Default'
        else:
            self.type = self.inputs['type']

        if self.type == 'Symbolic':
            from symengine import var
            for k in self.required:
                if isinstance(self.inputs[k], str):
                    self.inputs[k] = var(self.inputs[k])

    def process(self):
        self.outputs['result'] = self.inputs['a'] * self.inputs['b']
        self.return_msg_ = 'I mulitplied a and b.'
        return super().process()


class Div(Custom):
    """
    Divides two objects.

    :param a: *Required*. Left operand.
    :param b: *Required*. Right operand.
    :param type: Indicates the type of operation, whether it should divide
                 using default python behavior or add symbolically.
    :returns: The result of ``a/b``.
    """
    inputs = {'type': {'Symbolic': 'Symbolic', 'Default': 'Default'},
              'a': None, 'b': None}
    outputs = {'result': None}
    required = ['a', 'b']

    def __init__(self):
        self.return_msg_ = 'Ready to divide stuff.'

    def configure(self):
        self.type = 'Default'
        if self.inputs['type'] is None or self.inputs['type'] == '':
            self.type = 'Default'
        else:
            self.type = self.inputs['type']

        if self.type == 'Symbolic':
            from symengine import var
            for k in self.required:
                if isinstance(self.inputs[k], str):
                    self.inputs[k] = var(self.inputs[k])

    def process(self):
        self.outputs['result'] = self.inputs['a'] / self.inputs['b']
        self.return_msg_ = 'I divided a by b.'
        return super().process()


class Int_Div(Custom):
    """
    Integer divides two objects. Equivalent to the ``//`` operator.

    :param a: Left operand.
    :param b: Right operand.
    :returns: The result of ``a//b``.
    """
    inputs = {'a': None, 'b': None}
    outputs = {'result': None}
    required = ['a', 'b']

    def __init__(self):
        self.return_msg_ = 'Ready to integer divide stuff.'

    def process(self):
        self.outputs['result'] = self.inputs['a'] // self.inputs['b']
        self.return_msg_ = 'I integer divided a and b.'
        return super().process()
