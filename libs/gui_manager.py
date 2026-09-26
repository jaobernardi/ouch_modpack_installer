import logging
import os
import sys
from tkinter import Menu, StringVar, Tk, ttk

from PIL import Image, ImageTk
import psutil

from libs.structures.settings import GarbageCollectorEnum, InstallSettings

global MAX_MEMORY
MAX_MEMORY = round(psutil.virtual_memory().total/1024/1024/1024)


class GUIManager:
    def __init__(self) -> None:
        self.root = Tk()
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.style: dict[str, str] = {
            "BG_COLOR": "#1e1f2e"
        }
        self.installation_settings = InstallSettings.get_ideal_settings()
        self.logo: ImageTk.PhotoImage | None = None
        self.setup()
        pass

    @staticmethod
    def resource_path(relative_path: str) -> str:
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            base_path = sys._MEIPASS  # type: ignore
        except AttributeError:
            # running as a script (e.g., in development or debugging)
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)  # type: ignore

    def get_menu(self) -> Menu:
        menubar = Menu(
            self.root,
            bg=self.style["BG_COLOR"],
            fg="white",
            activebackground="gray"
        )

        utilsmenu = Menu(menubar, tearoff=0)

        utils_memory_allocation = Menu(utilsmenu, tearoff=0)
        # TODO: Adjust this to use tkinter's built-in methods.
        for i in range(MAX_MEMORY-8):
            def super_wrapper(mem: int):
                def wrapped_callback():
                    self.installation_settings.allocated_memory = mem*1024
                    print(self.installation_settings)
                return wrapped_callback

            utils_memory_allocation.add_radiobutton(
                label=f"{i+8}GB",
                command=super_wrapper(i+8)
            )

        utilsmenu.add_cascade(
            label="Alocação de Memória",
            menu=utils_memory_allocation
        )
        menubar.add_cascade(label="Config", menu=utilsmenu)

        current_gc = StringVar(
            value=self.installation_settings.garbage_collector.value
        )

        def update_gc_settings():
            self.installation_settings.garbage_collector = GarbageCollectorEnum(current_gc.get())  # noqa: 501
            print(self.installation_settings)

        utils_gc = Menu(utilsmenu, tearoff=0)
        for gc in GarbageCollectorEnum:
            utils_gc.add_radiobutton(
                label=gc.value,
                variable=current_gc,
                command=update_gc_settings
            )

        menubar.add_cascade(label="Garbage Collector", menu=utils_gc)
        return menubar

    def reset(self):
        # Destroy all children.
        for element in [i for i in self.root.children.values()]:
            element.destroy()

        assert self.logo
        self.logger.info("Reset screen")
        ttk.Label(
            self.root,
            image=self.logo,
            background=self.style["BG_COLOR"]
        ).pack()

        menubar = self.get_menu()
        self.root.config(menu=menubar)

    def setup(self):
        self.logger.info("Setting up tkinter")
        self.root.resizable(False, False)
        self.root.title("Ouch que Dificil: Instalador de Modpack")

        try:
            self.root.iconbitmap(self.resource_path("logo.ico"))  # type: ignore # noqa
        except:  # noqa
            self.logger.warning("Failed to set iconbitmap")
            pass

        self.root.configure(bg=self.style["BG_COLOR"])
        self.root.minsize(256, 200)
        self.root.geometry("256x200")

        image = Image.open(self.resource_path("logo.ico"))
        self.logo = ImageTk.PhotoImage(image)
        self.reset()

    def run(self) -> None:
        self.root.mainloop()
