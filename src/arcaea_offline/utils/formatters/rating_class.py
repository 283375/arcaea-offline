from typing import Any, Literal, overload

from arcaea_offline.constants.enums import ArcaeaRatingClass


class RatingClassFormatter:
    abbreviations = {
        ArcaeaRatingClass.PAST: "PST",
        ArcaeaRatingClass.PRESENT: "PRS",
        ArcaeaRatingClass.FUTURE: "FTR",
        ArcaeaRatingClass.BEYOND: "BYD",
        ArcaeaRatingClass.ETERNAL: "ETR",
    }

    NAME_FORMAT_RESULTS = Literal[
        "Past", "Present", "Future", "Beyond", "Eternal", "Unknown"
    ]

    @overload
    @classmethod
    def name(cls, rating_class: ArcaeaRatingClass) -> NAME_FORMAT_RESULTS:
        """
        Returns the capitalized rating class name, e.g. Future.
        """
        ...

    @overload
    @classmethod
    def name(cls, rating_class: int) -> NAME_FORMAT_RESULTS:
        """
        Returns the capitalized rating class name, e.g. Future.

        The integer will be converted to `ArcaeaRatingClass` enum,
        and will return "Unknown" if the convertion fails.
        """
        ...

    @classmethod
    def name(cls, rating_class: Any) -> NAME_FORMAT_RESULTS:
        if isinstance(rating_class, ArcaeaRatingClass):
            return rating_class.name.lower().capitalize()  # type: ignore
        elif isinstance(rating_class, int):
            try:
                return cls.name(ArcaeaRatingClass(rating_class))
            except ValueError:
                return "Unknown"
        else:
            raise TypeError(f"Unsupported type: {type(rating_class)}, cannot format")

    ABBREVIATION_FORMAT_RESULTS = Literal["PST", "PRS", "FTR", "BYD", "ETR", "UNK"]

    @overload
    @classmethod
    def abbreviation(
        cls, rating_class: ArcaeaRatingClass
    ) -> ABBREVIATION_FORMAT_RESULTS:
        """
        Returns the uppercased rating class name, e.g. FTR.
        """
        ...

    @overload
    @classmethod
    def abbreviation(cls, rating_class: int) -> ABBREVIATION_FORMAT_RESULTS:
        """
        Returns the uppercased rating class name, e.g. FTR.

        The integer will be converted to `ArcaeaRatingClass` enum,
        and will return "UNK" if the convertion fails.
        """
        ...

    @classmethod
    def abbreviation(cls, rating_class: Any) -> ABBREVIATION_FORMAT_RESULTS:
        if isinstance(rating_class, ArcaeaRatingClass):
            return cls.abbreviations[rating_class]  # type: ignore
        elif isinstance(rating_class, int):
            try:
                return cls.abbreviation(ArcaeaRatingClass(rating_class))
            except ValueError:
                return "UNK"
        else:
            raise TypeError(f"Unsupported type: {type(rating_class)}, cannot format")
