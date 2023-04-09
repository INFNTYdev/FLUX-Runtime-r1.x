
import tkinter as tk
from fluxr import *


class App1(tk.Tk):
    def __init__(self, fw_p):
        tk.Tk.__init__(self)
        self.geometry("1200x500")
        self.title("Test Application 1")
        return


class App2(TkWindow):
    def __init__(self, fw_p):
        TkWindow.__init__(
            self=self,
            identifier='test',
            fw=fw_p,
            svc_c=fw_p.service_call
        )
        self.geometry("1200x500")
        self.title("Test Application 2")
        self.t = tk.Button(self, text='Hello world!')
        self.t.pack(expand=True)
        return


if __name__ == '__main__':
    fw = RuntimeFramework(dev=True)
    fw.inject_app(App2(fw))
    fw.invoke_application()
