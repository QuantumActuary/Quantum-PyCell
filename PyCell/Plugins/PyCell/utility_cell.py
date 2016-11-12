import Quantum
from PyCell.custom_cell import Custom
import time


class Sleep(Custom):
    inputs = {'seconds': 0}
    inflows = ['>>']
    outputs = {'done': False}
    outflows = {'>>': Quantum.UNKNOWN}
    required = ['>>', 'seconds']
    internal_use = ['>>']

    def __init__(self):
        self.return_msg_ = "Everything looks good!"

    def process(self):
        time.sleep(self.inputs['seconds'])
        print("I have awakened!")
        self.outputs['done'] = True
        self.outflows['>>'] = Quantum.OK
        return super().process()

    def return_msg(self):
        return self.return_msg_


class Print(Custom):
    inputs = {'msg': 'Hello World!'}
    inflows = ['>>']
    outflows = {'>>': Quantum.UNKNOWN}
    required = ['>>', 'msg']
    internal_use = ['>>']
    always_reprocess = True

    def __init__(self):
        self.return_msg_ = "Ready... to print money!"

    def process(self):
        try:
            print(self.inputs['msg'])
            self.outflows['>>'] = Quantum.OK
            self.return_msg_ = 'Print execution done.'
        except:
            self.outflows['>>'] = Quantum.UNKNOWN
            self.return_msg_ = 'Problem printing!'
        return super().process()

    def return_msg(self):
        return self.return_msg_


class Start(Custom):
    outflows = {'>>': Quantum.OK}

    def process(self):
        self.outflows['>>'] = Quantum.OK
        return super().process()
