from typing import Any


class SingletonMeta(type):
    _instance_map: dict[type, object] = {}

    def __call__(cls: ..., *args: tuple[Any], **kwargs: dict[str, Any]) -> object:  # noqa: 501
        if cls not in cls._instance_map:
            cls._instance_map[cls] = super().__call__(*args, **kwargs)

        return cls._instance_map[cls]