from typing import Any, ClassVar, Dict, Protocol


class TDataclass(Protocol):
    __dataclass_fields__: ClassVar[Dict]

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        ...
