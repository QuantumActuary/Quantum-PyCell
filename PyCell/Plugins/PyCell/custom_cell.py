"""
Custom Cell
===========

Provides prototype cell from which all other cells should derive.
"""
import Quantum
from traceback_formatter import pprint_tb
import sys


def exception_raiser(func):
    def exec_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pprint_tb(*sys.exc_info())
            raise
    return exec_func


class Custom(object):
    """
    This is the abstract type that all PyCells should derive from. It provides
    the default class variables as well as some convenience functions that all
    cells will need. All derivative cells should return the process function
    defined here. The Custom class also provides a unique ``py_id`` to each
    cell that derives from it.

    :param inputs: A dictionary of input sockets. Derivative classes can
                   override this variable to supply thier own input sockets.
    :type inputs: dict
    :param outputs: A dictionary of output sockets. Derivative classes can
                    override to supply thier own output sockets.
    :type outputs: dict
    :param inflows: A list of input sockets that may only accept a Quantum
                    ``ReturnCode``. Return codes are an enum defined by
                    Quantum API.
    :type inflows: list
    :param outflows: A dictionary of output sockets that may only hold a
                     ``ReturnCode``.
    :type outflows: dict
    :param required: A list of required sockets by name.
    :type required: list
    :param always_preprocess: Determines if a cell should always re-process
                              on a subsequent call even if none of the inputs
                              have changed. Default, False.
    :type always_preprocess: boolean
    """
    inputs = {}
    outputs = {}
    inflows = []
    outflows = {}
    required = []
    internal_use = []
    always_reprocess = False

    def __init__(self):
        self.py_id = 0  # value generated in c++

    def is_valid_input(self, i, allow_none=False, allow_dict=False, **kwargs):
        """
        Checks whether or not an input has a value. This may be useful for
        determining if a key word argument should be appended prior to a
        function call.

        :param i: The input socket.
        :type i: object
        :param allow_none: Determines if ``None`` counts as a valid value.
                           Default, False
        :type allow_none: boolean
        """
        if allow_none or isinstance(i, str):
            return not i == ''
        elif allow_dict:
            return i is not None
        else:
            return i is not None and not isinstance(i, dict)

    def process(self):
        """
        Manages the return value that gets passed back to the C++ scheduler.
        Always call this function at the end of your process implementation
        and return its value. Your process function should never need to
        return a value to the scheduler. This function will manage that for
        you.
        """
        return Quantum.OK
