from career_agent.models.language_levels import (
    LANGUAGE_LEVELS,
)



def test_language_levels_are_ordered():

    assert (
        LANGUAGE_LEVELS["A1"]
        < LANGUAGE_LEVELS["A2"]
    )

    assert (
        LANGUAGE_LEVELS["A2"]
        < LANGUAGE_LEVELS["B1"]
    )

    assert (
        LANGUAGE_LEVELS["B1"]
        < LANGUAGE_LEVELS["B2"]
    )

    assert (
        LANGUAGE_LEVELS["B2"]
        < LANGUAGE_LEVELS["C1"]
    )

    assert (
        LANGUAGE_LEVELS["C1"]
        < LANGUAGE_LEVELS["C2"]
    )
    
def test_c2_is_highest_language_level():

    assert (
        LANGUAGE_LEVELS["C2"]
        == max(
            LANGUAGE_LEVELS.values(),
        )
    )