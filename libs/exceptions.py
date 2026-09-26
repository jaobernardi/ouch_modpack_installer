from functools import wraps
from logging import getLogger
from tkinter import messagebox
import traceback
from typing import Any, Callable

logger = getLogger("exceptions")


class InstallerException(BaseException):
    ...


class JavaNotInstalledException(InstallerException):
    ...


def exception_catcher[T](func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]):
        try:
            return func(*args, **kwargs)
        except Exception:
            from libs.gui_manager import GUIManager
            GUIManager().main()  # type: ignore
            _traceback: str = traceback.format_exc()
            logger.fatal(_traceback)
            messagebox.showerror("Error", _traceback)
    return wrapper  # type: ignore
