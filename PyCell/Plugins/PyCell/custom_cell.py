"""
Custom Cell
===========

Provides prototype cell from which all other cells should derive.

.. tip::
   For writing your own cells, those that are run in a separate process will
   not emit any print statements. Cells that are threadsafe and set to always
   reprocess will run in the main process and will thus print to your console.
   Running a circuit with debug turned on will force all cells to run in a
   single thread and therefore all cells will be able to print to the console
   in this mode.

   To run your circuit in debug, you can type the following in your console::

       >>> run(debug=True, step=1)

   You can increase the step size to run multiple cells.
"""
from Quantum import QuReturnCode, QuCellSocket
from traceback_formatter import pprint_tb
import sys
import copy


def exception_raiser(func):
    """
    Use this decorator on functions that need to raise exceptions and display
    them in Quantum's console.
    """
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
    :param threadsafe: Determines if a cell will run in a separate thread or
                       separate process. If threadsafe, PyCell will attempt to
                       run the cell in a thread, otherwise, it will spawn a
                       separate process just to run the cell.
    :type threadsafe: boolean
    :param always_reprocess: Determines if a cell should always re-process
                             on a subsequent call even if none of the inputs
                             have changed. Default, False.
    :type always_reprocess: boolean
    """
    inputs = {}
    outputs = {}
    inflows = []
    outflows = {}
    required = []
    internal_use = []
    always_reprocess = False
    threadsafe = False

    def __init__(self):
        self.py_id = 0  # value generated in c++
        self.inputs = {k:v for k, v in self.__class__.inputs.items()}
        if isinstance(self.__class__.inputs, ValidInputs):
            self.inputs = copy.deepcopy(self.__class__.inputs)
            self.inputs = ValidInputs(self.inputs)
        self.outputs = {k:v for k, v in self.__class__.outputs.items()}
        self.inflows = [v for v in self.__class__.inflows]
        self.outflows = {k:v for k, v in self.__class__.outflows.items()}

    def start(self):
        pass

    def stop(self):
        pass

    def process(self, code=None):
        """
        Manages the return value that gets passed back to the C++ scheduler.
        Always call this function at the end of your process implementation
        and return its value. Your process function should never need to
        return a value to the scheduler. This function will manage that for
        you.

        :param code: You can pass a return code here which will get passed on
                     to the scheduler.
        :type code: :class:`~Quantum.QuReturnCode`
        """
        try:
            return code.returncode
        except AttributeError:
            return QuReturnCode('OK').returncode


    def return_msg(self):
        try:
            return self.return_msg_
        except:
            return "No message available."

class ValidInputs(dict):
    """
    This is a special dict that assumes all values are
    :class:`~Quantum.QuCellSocket`. QuCellSockets can contain validation
    functions that determine what happens when a client tries to store a value
    in the socket. ValidInputs helps to manage a dict of these sockets and
    prevents the QuCellSocket from being overwritten by a primitive type. This
    preserves any validation functions that may have been registered with the
    sockets.

    Examples::

      inputs = ValidInputs(my_socket=QuCellSocket(1.234))
      inputs = ValidInputs(a=QuCellSocket('a_value'), b=QuCellSocket('b_value'))
      inputs = ValidInputs({'c':QuCellSocket(5)})
      inputs = ValidInputs(num=1, char='a')
    """
    def __init__(self, *args, **kwargs):
        for i in args:
            for k, v in i.items():
                if not isinstance(v, QuCellSocket):
                    self[k] << v
                else:
                    self[k] = v
        for k, v in kwargs.items():
            if not isinstance(v, QuCellSocket):
                self[k] << v
            else:
                self[k] = v

    def __setitem__(self, key, item):
        if not isinstance(item, QuCellSocket):
            self[key] << item
        else:
            self.__dict__[key] = item

    def __getitem__(self, key):
        ret = None
        try:
            ret = self.__dict__[key]
        except KeyError:
            self[key] = QuCellSocket(None)
            ret = self[key]
        return ret

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return self.__dict__.has_key(k)

    def pop(self, k, d=None):
        return self.__dict__.pop(k, d)

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        # return self.__dict__.keys()
        return list(self.__dict__)

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict):
        return cmp(self.__dict__, dict)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))



