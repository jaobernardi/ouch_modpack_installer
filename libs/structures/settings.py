from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field
from pydantic._internal._model_construction import ModelMetaclass


class SettingsPersistentInstance[T](ModelMetaclass):
    _instance: T | None = None

    def __call__(cls, *args: tuple[Any, Any], **kwds: dict[str, Any]) -> T:
        cls._instance = super().__call__(*args, **kwds)
        assert cls._instance is not None
        return cls._instance

    def get(cls) -> T | None:
        return cls._instance


class GarbageCollectorEnum(StrEnum):
    ZGC = "zgc"
    SHENANDOAH = "shenandoah"
    G1GC = "g1gc"


class InstallSettings(
    BaseModel,
    metaclass=SettingsPersistentInstance['InstallSettings']
):
    allocated_memory: int = Field(default_factory=lambda: 0)
    gargabe_collector: GarbageCollectorEnum
