
""" FLUX tkinter window dispatcher """


# MODULE IMPORTS
from flxr.tklib import *

# MODULE PACKAGE
__package__ = tkpkg_n()


# MODULE CLASSES
class TkinterWindow(tk.Tk):
    def __init__(self, fw: any, svc: any, root: any, identifier: str, **kwargs):
        """
        FLUX tkinter window instance

        :param fw: Hosting framework
        :param svc: Framework service call
        :param root: Root application window
        :param identifier: Window unique identifier
        :param kwargs: Additional window configuration args
        """

        self.__FW = fw_obj(fw)
        self.__S = svc
        self.__root = root
        self._identifier: str = identifier

        tk.Tk.__init__(self)
        self.__S(TkinterWindow)['console'](text=f"Dispatching '{identifier}' window...")
        self._window_width: int = kwargs.get('width')
        self._window_height: int = kwargs.get('height')
        self._window_x_pos: int = kwargs.get('xpos', self._center_x())
        self._window_y_pos: int = kwargs.get('ypos', self._center_y())
        self._user_in_bounds: bool = False
        self.title(kwargs.get('title'))
        self.overrideredirect(kwargs.get('borderless'))
        self.geometry(f"{self._window_width}x{self._window_height}"
                      f"+{self._window_x_pos}+{self._window_y_pos}")
        self.config(bg=kwargs.get('bg'))

        self._container: tk.Frame = tk.Frame(
            master=self,
            bg=kwargs.get('bg')
        )
        self._container.pack_propagate(False)
        self._container.grid_propagate(False)
        self._container.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True
        )
        self._container.bind('<Enter>', self._master_hover_event)
        self._container.bind('<Leave>', self._master_hover_event)
        self.bind('<Configure>', self._master_configure_event)

    def maxamize(self):
        """ Maxamize the application window """
        self.state('zoomed')

    def root_container(self) -> tk.Frame:
        """ Returns the window root container """
        return self._container

    def coordinates(self) -> tuple:
        """ Returns the coordinates of the window corners """
        x1 = self._window_x_pos
        y1 = self._window_y_pos
        y2 = y1+self._window_height
        x3 = x1+self._window_width
        return tuple(([x1, y1], [x1, y2], [x3, y2], [x3, y1]))

    def winbind(self, event: str, func: any):
        """ Bind an event to the window root container """
        self._container.bind(event, func, add='+')

    def _master_hover_event(self, event: tk.Event):
        """ Master window hover event """
        if str(event).__contains__('Enter'):
            self._user_in_bounds = True
        elif str(event).__contains__('Leave'):
            self._user_in_bounds = False

    def _master_configure_event(self, event: tk.Event):
        """ Master window configure event """
        if self.winfo_width() != self._window_width:
            self._window_width = self.winfo_width()
        if self.winfo_height() != self._window_height:
            self._window_height = self.winfo_height()
        if self.winfo_rootx() != self._window_x_pos:
            self._window_x_pos = self.winfo_rootx()
        if self.winfo_rooty() != self._window_y_pos:
            self._window_y_pos = self.winfo_rooty()

    def _center_x(self) -> int:
        """ Returns the center x coordinate """
        return int((self.__root.winfo_screenwidth()/2)-(self._window_width/2))

    def _center_y(self) -> int:
        """ Returns the center y coordinate """
        return int((self.__root.winfo_screenheight()/2)-(self._window_height/2))


class TkinterWindowDispatcher:
    def __init__(self, fw: any, svc: any):
        """
        FLUX tkinter library window dispatcher

        :param fw: Hosting framework
        :param svc: Framework service call
        """

        self.__FW = fw_obj(fw)
        self.__S = svc

        self.__window_host: dict = {}

    def set_main(self, main: tk.Tk):
        """ Set the window dispatchers main window """
        self.__window_host['main-win'] = main
        self.__S(self)['console'](text="Successfully set main application window")

    def launch_main(self):
        """ Launch main application window """
        self.__S(self)['console'](text="Launching main application window...")
        self.__window_host['main-win'].mainloop()

    def new_window(self, identifier: str, **kwargs) -> TkinterWindow:
        """ Dispatch a new tkinter window """
        window: TkinterWindow = TkinterWindow(
            fw=self.__FW,
            svc=self.__S,
            root=self.__window_host['main-win'],
            identifier=identifier,
            title=kwargs.get('title', identifier),
            borderless=kwargs.get('borderless'),
            width=kwargs.get('width'),
            height=kwargs.get('height'),
            bg=kwargs.get('bg', '#F2F7F9'),
        )
        self.__window_host[identifier] = window
        return window

    def destroy_dependencies(self):
        """ Destroy all tkinter window instances except main """
        delete: list = []
        self.__S(self)['console'](text=f"Closing all children tkinter window instances...")
        for _id, __window in self.__window_host.items():
            if _id != 'main-win':
                self.__S(self)['console'](text=f"Closing '{_id}' window...")
                delete.append(_id)
                __window.destroy()
        for deletion in delete:
            del self.__window_host[deletion]
            self.__S(self)['console'](text=f"Deleted '{deletion}' window")

    def destroy_all(self):
        """ Destroy all tkinter window instances """
        self.__S(self)['console'](text=f"Closing all tkinter window instances...")
        for _id, __window in self.__window_host.items():
            self.__S(self)['console'](text=f"Closing '{_id}' window...")
            __window.destroy()
        self.__window_host.clear()
