from typing import Any
from pathlib import Path
import json


class Store:


    def __init__(self, filePath: str):

        self.file = Path(filePath)

        self.file.parent.mkdir(parents=True, exist_ok=True)

        if not self.file.exists():

            self.file.write_text("[]")


    def load(self) -> list[dict[str, Any]]:

        return json.loads(self.file.read_text())
    

    def save(self, data: list[dict[str, Any]]):

        self.file.write_text(json.dumps(data, indent=2))
