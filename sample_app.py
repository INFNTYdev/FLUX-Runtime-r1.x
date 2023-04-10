
import tkinter as tk
from flxr import *


class App1(tk.Tk):
    def __init__(self, hfw: any, svc: any):
        self.__FW = fw_obj(hfw)
        self.__S = svc

        tk.Tk.__init__(self)
        self.geometry("1200x500")
        self.title("Test Application 1")

        self.button = tk.Button(
            master=self,
            text='Click for new window',
            command=self.new_win
        )
        self.button.pack(
            expand=True
        )
        self.button2 = tk.Button(
            master=self,
            text='Click to destroy all windows',
            command=self.destroy_all
        )
        self.button2.pack(
            expand=True
        )
        return

    def new_win(self):
        self.__S(App1)['TkWindow'](
            identifier=self.__S(App1)['time'](),
            title=self.__S(App1)['time'](),
            width=700
        )

    def destroy_all(self):
        self.__S(App1)['breakTk']()


if __name__ == '__main__':
    fw = Flxr(
        dev=True,
        main=App1
    )
