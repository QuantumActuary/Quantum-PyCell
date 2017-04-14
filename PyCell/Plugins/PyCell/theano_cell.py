"""
Theano Plugin
=============

This plugin provides cells to work with theano.
"""
import numpy
#from theano import (function, tensor as T)
from PyCell import registry
from PyCell.custom_cell import Custom

registry += [
    {
        'name': 'Scalar',
        'module': 'PyCell.theano_cell',
        'categories': ['Memory']
    },
    {
        'name': 'Function',
        'module': 'PyCell.theano_cell',
        'categories': ['Theano']
    }
             ]

class Scalar(Custom):
    """
    Creates a theano scalar

    :param name: The name of your variable.
    :type name: String
    :returns: A theano scalar.
    :rtype: dscalar
    """

    inputs = {'name': None}
    outputs = {'scalar': None}
    required = ['name']

    def process(self):
        self.outputs['scalar'] = T.dscalar(self.inputs['name'])
        return super().process()

class Function(Custom):
    """
    Compiles a theano expression into a callable function.

    :param inputs: A list of theano input variables.
    :type inputs: List
    :param expr: The expression to be compiled, composed of theano objects.
    :type expr: Variable
    :returns: A compiled, python-callable function.
    :rtype: callable
    """
    inputs = {'inputs':None, 'expr':None}
    outputs = {'func':None}
    required = ['inputs', 'expr']

    def process(self):
        self.outputs['func'] = function(self.inputs['inputs'],
                                        self.inputs['expr'])
        return super().process()
