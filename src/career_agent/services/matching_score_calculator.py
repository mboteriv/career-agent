

class MatchingScoreCalculator:

    def calculate(
        self,
        criterion_matches: list[CriterionMatch],
        policy: MatchingPolicy,
    ) -> float:

        weighted_sum = 0.0

        total_weight = 0.0

        for criterion_match in criterion_matches:

            if not criterion_match.applicable:
                continue

            weight = policy.weight_for(
                criterion_match.criterion,
            )

            weighted_sum += (
                criterion_match.score * weight
            )

            total_weight += weight

        if total_weight == 0:
            return 0.0

        return (
            weighted_sum
            / total_weight
        )