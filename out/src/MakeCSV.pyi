from . import DetectFreezing as DetectFreezing
from typing import Any, Union

class MakeCSV:
    avi: Any = ...
    delimiter: Any = ...
    header: Any = ...
    out: Any = ...
    threshold: Any = ...
    window: Any = ...
    def __init__(self, avi: str, delimiter: str=..., header: bool=..., out: Union[str, int]=..., threshold: int=..., window: bool=...) -> None: ...
    def make(self) -> None: ...
