

class MatchingScoreCalculator:

    def calculate(
        self,
        scores: list[float],
    ) -> float:

        if not scores:
            return 0.0

        return max(scores)