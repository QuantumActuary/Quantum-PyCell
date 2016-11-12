import Quantum
from PyCell.custom_cell import Custom
# from symengine import sympify
# from symengine import var
# from symengine import exp
# from symengine import Symbol
from sympy import sympify
from sympy import var
from sympy import exp
from sympy import Symbol


class Sympify(Custom):
    """Converts back and forth ))<>(( between Symengine and Sympy
    """
    inputs = {'f(x)': None}
    outputs = {'f(x)': None}
    required = ['f(x)']

    def __init__(self):
        self.return_msg_ = "Nothing to report!"
        self.return_code = Quantum.OK

    def process(self):
        self.outputs['f(x)'] = sympify(self.inputs['f(x)'])
        return super().process()

    def return_msg(self):
        return self.return_msg_


class Exponentiate(Custom):
    """Exponentiate base by exp
    """
    inputs = {'base': None, 'exp': None}
    outputs = {'f(x)': None}
    required = ['base', 'exp']

    def __init__(self):
        self.return_msg_ = "Nothing to report!"
        self.return_code = Quantum.OK

    def process(self):
        for k in self.inputs.keys():
            if isinstance(self.inputs[k], str):
                self.inputs[k] = var(self.inputs[k])
        if self.return_code == Quantum.OK:
            self.outputs['f(x)'] = (self.inputs['base'] ** self.inputs['exp'])
        return super().process()

    def return_msg(self):
        return self.return_msg_


class Exp(Custom):
    """The constant e
    """
    inputs = {'exp': None}
    outputs = {'f(x)': None}
    required = ['exp']

    def __init__(self):
        self.return_msg_ = "Nothing to report!"
        self.return_code = Quantum.OK

    def process(self):
        for k in self.inputs.keys():
            if isinstance(self.inputs[k], str):
                self.inputs[k] = var(self.inputs[k])
        if self.return_code == Quantum.OK:
            self.outputs['f(x)'] = exp(self.inputs['exp'])
        return super().process()

    def return_msg(self):
        return self.return_msg_


class Expand(Custom):
    """Expands the input formula
    """
    inputs = {'f(x)': None}
    outputs = {'f(x)': None}
    required = ['f(x)']

    def __init__(self):
        self.return_msg_ = "Nothing to report!"
        self.return_code = Quantum.OK

    def process(self):
        for k in self.inputs.keys():
            if isinstance(self.inputs[k], str):
                self.inputs[k] = var(self.inputs[k])
        if self.return_code == Quantum.OK:
            self.outputs['f(x)'] = self.inputs['f(x)'].expand()
        return super().process()

    def return_msg(self):
        return self.return_msg_
