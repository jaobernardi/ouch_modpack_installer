from copy import copy
import os
import sys
import zipfile
from io import BytesIO
from queue import Queue
from threading import Thread
from tkinter import *
from tkinter import ttk

import requests
from PIL import Image, ImageTk
import psutil

from libs.structures import AppStateType, Modpack


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # running as a script (e.g., in development or debugging)
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


root = Tk()
root.resizable(False, False)
root.title("Ouch Installer")
try:
    root.iconbitmap("./tcc_is_back.ico")
except:
    pass

image = Image.open("tcc_is_back.ico")
image = ImageTk.PhotoImage(image)
BG_COLOR = "#1e1f2e"
root.configure(bg=BG_COLOR)
root.minsize(256, 200)
root.geometry("256x200")
style = ttk.Style()
style.configure("BW.TLabel", foreground="white", background="#75768f", padding=3)

global MEMORY_TO_ALLOCATE
MEMORY_TO_ALLOCATE = 8
MAX_MEMORY = round(psutil.virtual_memory().total/1024/1024/1024)

def set_memory(memory: int):
    global MEMORY_TO_ALLOCATE
    MEMORY_TO_ALLOCATE = memory
    print(MEMORY_TO_ALLOCATE)

def clear(hide_menu: bool = None):
    # root.grid()
    for i in [i for i in root.children.values()]:
        i.destroy()
    ttk.Label(root, image=image, background=BG_COLOR).pack()
    menubar = Menu(root,  bg="black", fg="white", activebackground="gray")

    utilsmenu = Menu(menubar, tearoff=0)

    utils_memory_allocation = Menu(utilsmenu, tearoff=0)

    for i in range(MAX_MEMORY-8):
        def super_wrapper(mem):
            def wrapped_callback():
                set_memory(mem)
            return wrapped_callback
        utils_memory_allocation.add_radiobutton(label=f"{i+8}GB", command=super_wrapper(i+8))
    utilsmenu.add_cascade(label="Alocação de Memória", menu=utils_memory_allocation)

    menubar.add_cascade(label="Config", menu=utilsmenu)
    if not hide_menu:
        root.config(menu=menubar)

def install():
    clear(hide_menu=True)
    ttk.Label(root, text="Instalando modpack", style="BW.TLabel").pack()

    def async_install():
        lbl = ttk.Label(
            root,
            text="Baixando índice de mods",
            background="#1e1f2e",
            foreground="white",
            justify="center",
            wraplength=256,
        )
        lbl.pack()
        req = requests.get("https://aiquedificil.com.br/modpack/pack.mrpack")
        try:
            file = zipfile.PyZipFile(BytesIO(req.content))
            modpack = Modpack.from_zip(file)
            for i in modpack.install_client(memory_gb=MEMORY_TO_ALLOCATE):
                lbl["text"] = i.msg
        except Exception as e:
            gui()
            lbl = ttk.Label(
                root,
                text="Gag, falhei ao instalar modpack :'(",
                background="#1e1f2e",
                foreground="#991F1F",
                justify="center",
                wraplength=256,
            )
            lbl.pack()
            raise e
        clear()
        ttk.Label(root, text="Modpack Instalado \\o/", style="BW.TLabel").pack()

    thread = Thread(target=async_install, daemon=True).start()


def gui():
    clear()
    ttk.Button(root, style="BW.TLabel", text="Instalar Modpack", command=install).pack()


def main():
    gui()
    root.mainloop()


if __name__ == "__main__":
    main()
