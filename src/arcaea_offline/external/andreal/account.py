class AndrealImageGeneratorAccount:
    def __init__(
        self,
        name: str = "Player",
        code: int = 123456789,
        rating: int = -1,
        character: int = 5,
        character_uncapped: bool = False,
    ):
        self.name = name
        self.code = code
        self.rating = rating
        self.character = character
        self.character_uncapped = character_uncapped
