from PyCell.custom_cell import Custom
from sympy import diff
from sympy import integrate
from sympy import oo


class Differentiate(Custom):
    inputs = {'f(x)': None, 'dx': None}
    outputs = {'df/dx': None}
    required = ['f(x)', 'dx']

    def __init__(self):
        self.return_msg_ = "Everything looks good!"

    def process(self):
        self.outputs['df/dx'] = diff(self.inputs['f(x)'], self.inputs['dx'])
        return super().process()

    def return_msg(self):
        return self.return_msg_


class Integrate(Custom):
    inputs = {'f(x)': None, 'dx': None, 'lower limit':-oo,
              'upper limit': oo}
    outputs = {'F(x)': None}
    required = ['f(x)', 'dx']

    def __init__(self):
        self.return_msg_ = "Everything looks good!"

    def process(self):
        self.outputs['F(x)'] = integrate(self.inputs['f(x)'],
                                         (self.inputs['dx'],
                                          self.inputs['lower limit'],
                                          self.inputs['upper limit']))
        return super().process()

    def return_msg(self):
        return self.return_msg_
