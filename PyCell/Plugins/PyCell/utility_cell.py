from Quantum import QuReturnCode
from PyCell import registry
from PyCell.custom_cell import Custom
import time

registry += [
    {
    'name': 'Sleep',
    'module': 'PyCell.utility_cell',
    'categories': ['Flow Control']
    },
    {
    'name': 'Print',
    'module': 'PyCell.utility_cell',
    'categories': ['Utility']
    },
    {
    'name': 'Start',
    'module': 'PyCell.utility_cell',
    'categories': ['Flow Control']
    }
    ]

class Sleep(Custom):
    inputs = {'seconds': 0}
    inflows = ['>>']
    outputs = {'done': False}
    outflows = {'>>': QuReturnCode('UNKNOWN').returncode}
    required = ['>>', 'seconds']
    internal_use = ['>>']

    def __init__(self):
        self.return_msg_ = "Everything looks good!"

    def process(self):
        time.sleep(self.inputs['seconds'])
        print("I have awakened!")
        self.outputs['done'] = True
        self.outflows['>>'] = QuReturnCode('OK').returncode
        return super().process()

    def return_msg(self):
        return self.return_msg_


class Print(Custom):
    inputs = {'msg': 'Hello World!'}
    inflows = ['>>']
    outflows = {'>>': QuReturnCode('UNKNOWN').returncode}
    required = ['>>', 'msg']
    internal_use = ['>>']
    always_reprocess = True
    threadsafe = True

    def __init__(self):
        self.return_msg_ = "Ready... to print money!"

    def process(self):
        try:
            print(self.inputs['msg'])
            self.outflows['>>'] = QuReturnCode('OK').returncode
            self.return_msg_ = 'Print execution done.'
        except:
            self.outflows['>>'] = QuReturnCode('UNKNOWN').returncode
            self.return_msg_ = 'Problem printing!'
        return super().process()

    def return_msg(self):
        return self.return_msg_


class Start(Custom):
    outflows = {'>>': QuReturnCode('OK').returncode}

    def process(self):
        self.outflows['>>'] = QuReturnCode('OK').returncode
        return super().process()
