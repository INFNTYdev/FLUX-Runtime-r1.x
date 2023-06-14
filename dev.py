
from flxr import *


class DeveloperWindow(tk.Tk):
    def __init__(self, hfw: any, svc: any) -> None:
        super().__init__()
        self.title("FLUX: Developer Window")
        self.minsize(
            width=800,
            height=400
        )

        self.TEST_FUNC: dict = {
            'New window': svc(DeveloperWindow)['newWindow'],
        }
        self.buttons: list = []

        for title, function in self.TEST_FUNC.items():
            self.buttons.append(
                tk.Button(master=self, text=title, command=function)
            )
            self.buttons[-1].pack(side=tk.TOP, pady=(10, 0))

        pass


class FrameworkWindow(FTkWindow):
    def __init__(self, hfw: any, svc: any) -> None:
        super().__init__(
            fw=hfw,
            svc=svc,
            root=self,
            identifier='main',
            title='FLUX: FTkWindow',
            minsize=(400, 200)
        )

        self.TEST_FUNC: dict = {
            'New window': svc(FrameworkWindow)['newWindow'],
        }
        self.buttons: list = []

        for title, function in self.TEST_FUNC.items():
            self.buttons.append(
                tk.Button(master=self, text=title, command=function)
            )
            self.buttons[-1].pack(side=tk.TOP, pady=(10, 0))


t: Flxr = Flxr(main=None, dev=True)
t.set_main(FrameworkWindow)
