import hashlib
import json
import os
from typing import Any


def create_modrinth_index(neoforge_version: str, mods_path: str) -> str:
    index: dict[str, str | list[dict[str, Any]] | dict[str, Any]] = {
        "game": "Minecraft",
        "name": "Ouch que Dificil: Vitorianos",
        "java_args": "",
        "files": [],
        "dependencies": {
            "neoforge": neoforge_version
        }
    }

    for file in os.listdir(mods_path):
        if not file.endswith(".jar"):
            continue

        hasher = hashlib.sha512()
        with open(mods_path+file, "rb") as local_file:
            hasher.update(local_file.read())
        calculated_hash = hasher.hexdigest()

        index["files"].append(  # type: ignore
            {
                "path": f"mods/{file}",
                "downloads": [
                    f"https://cdn.aiquedificil.com.br/assets/{file}"
                ],
                "hashes": {
                    "sha512": calculated_hash
                }
            }
        )
    with open("modrinth.index.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(index, indent=4))
