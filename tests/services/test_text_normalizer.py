from career_agent.services.text_normalizer import TextNormalizer


def test_normalize_converts_to_lowercase():

    normalizer = TextNormalizer()

    assert normalizer.normalize(
        "Python Programming",
    ) == "python programming"
    
def test_normalize_collapses_whitespace():

    normalizer = TextNormalizer()

    assert normalizer.normalize(
        "  Python    Programming  ",
    ) == "python programming"
    
def test_normalize_empty_string():

    normalizer = TextNormalizer()

    assert normalizer.normalize("") == ""