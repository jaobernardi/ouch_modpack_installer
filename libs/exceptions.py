from functools import wraps
from tkinter import messagebox
import traceback
from typing import Any, Callable


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
            messagebox.showerror("Error", traceback.format_exc())
    return wrapper  # type: ignore
