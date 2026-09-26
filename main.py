import multiprocessing
import os

from libs.gui_manager import GUIManager
import logging

logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler("installer.log")])

manager = GUIManager()

if __name__ == "__main__":
    if os.name != "nt":
        multiprocessing.set_start_method('forkserver', force=True)
    multiprocessing.freeze_support()

    manager.run()
