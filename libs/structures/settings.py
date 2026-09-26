from enum import StrEnum
import re
import subprocess
from pydantic import BaseModel, Field
from libs.exceptions import JavaNotInstalledException


class GarbageCollectorEnum(StrEnum):
    ZGC = "ZGC"
    SHENANDOAH = "Shenandoah"
    G1GC = "G1GC"


class InstallSettings(BaseModel):
    allocated_memory: int = Field(default_factory=lambda: 0)
    garbage_collector: GarbageCollectorEnum
    java_version: int

    @staticmethod
    def get_java_version() -> int:
        try:
            output = subprocess.check_output(
                ["java", "-version"], 
                stderr=subprocess.STDOUT, 
                text=True
            )
            match = re.search(r'"([^"]+)"', output)
            if match:
                return int(match.group(1).split(".")[0])
            raise ValueError(f"Unknown version: {output}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise JavaNotInstalledException()
        except ValueError as e:
            raise e

    @classmethod
    def get_ideal_settings(cls) -> InstallSettings:
        ideal_gc = GarbageCollectorEnum.G1GC
        java_version = cls.get_java_version()

        if java_version > 21:
            ideal_gc = GarbageCollectorEnum.ZGC

        ideal_memory = int(8.5*1024)

        return InstallSettings(
            allocated_memory=ideal_memory,
            garbage_collector=ideal_gc,
            java_version=java_version
        )
