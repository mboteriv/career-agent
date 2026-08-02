import pytest
from pydantic import ValidationError

from career_agent.models.language_skill import LanguageSkill

def test_create_language_skill():

    skill = LanguageSkill(
        language="English",
        level="C1",
    )

    assert skill.language == "English"
    assert skill.level == "C1"