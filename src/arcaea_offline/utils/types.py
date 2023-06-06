from typing import Any, Protocol, ClassVar, Dict

class TDataclass(Protocol):
    __dataclass_fields__: ClassVar[Dict]
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        ...
