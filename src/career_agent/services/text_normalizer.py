class TextNormalizer:

    def normalize(
        self,
        text: str,
    ) -> str:

        return " ".join(
            text.lower().split()
        )