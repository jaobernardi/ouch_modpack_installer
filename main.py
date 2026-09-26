from libs.gui_manager import GUIManager
import logging

logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler("installer.log")])

manager = GUIManager()

if __name__ == "__main__":
    manager.run()
