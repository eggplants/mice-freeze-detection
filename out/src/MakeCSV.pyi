from typing import Any

class MakeCSV:
    avi: Any = ...
    delimiter: Any = ...
    header: Any = ...
    out: Any = ...
    threshold: Any = ...
    window: Any = ...
    def __init__(self, avi: str, delimiter: str=..., header: bool=..., out: str=..., threshold: int=..., window: bool=...) -> None: ...
    def make(self) -> None: ...
