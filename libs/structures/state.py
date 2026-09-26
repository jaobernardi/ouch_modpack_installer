from typing import Any
from pydantic import BaseModel, Field, computed_field
from enum import StrEnum


class AppStateType(StrEnum):
    IDLE = "idle"
    PATH_CLEANUP = "path_cleanup"
    OVERRIDES_EXTRACTING = "overrides_extracting"
    MODPACK_DOWNLOADING = "modpack_downloading"
    LOADER_DOWNLOAD = "loader_download"
    LOADER_INSTALL = "loader_install"
    DONE = "done"
    DIFF_CHECK = "diff_check"

STATE_MSG_MAP: dict[AppStateType, str] = {
    AppStateType.PATH_CLEANUP: "Limpando .minecraft",
    AppStateType.DIFF_CHECK: "Verificando integridade e diff...\n({state.meta})",
    AppStateType.OVERRIDES_EXTRACTING: "Extraíndo overrides",
    AppStateType.MODPACK_DOWNLOADING: "Baixando modpack\n({state.meta.filename})",
    AppStateType.LOADER_DOWNLOAD: "Baixando loader\n({state.meta})",
    AppStateType.LOADER_INSTALL: "Instalando loader",
    AppStateType.DONE: "Prontinho!",
}

class AppState(BaseModel): 
    type: AppStateType
    meta: Any | dict[str, Any] | None = Field(None)

    @computed_field
    @property
    def msg(self) -> str:
        return STATE_MSG_MAP.get(self.type, str(self.type)).format(state=self)
