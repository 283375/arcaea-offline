from typing import NamedTuple


class Version(NamedTuple):
    first: int
    second: int
    third: int

    @classmethod
    def from_string(cls, version_str: str):
        version_str = version_str.removesuffix("c")
        parts = version_str.split(".")
        if len(parts) not in {2, 3}:
            raise ValueError(f"Invalid version string {version_str}")

        try:
            if len(parts) == 2:  # noqa: PLR2004
                parts.append("0")

            first, second, third = map(int, parts)
        except ValueError as e:
            raise ValueError(f"Invalid version string {version_str}") from e

        return cls(first, second, third)

    def __str__(self):
        return f"{self.first}.{self.second}.{self.third}"
