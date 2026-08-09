from pathlib import Path

from career_agent.adapters.esco_csv_reader import ESCOCSVReader
from career_agent.importers.esco_importer import ESCOImporter
from career_agent.models.external_knowledge import ExternalKnowledge
from collections import Counter
from collections import defaultdict

ESCO_DATA = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "career_agent"
    / "data"
    / "esco"
    / "raw"
    / "v1.2.1"
)


def test_import_knowledge_from_esco_csv():

    importer = ESCOImporter()

    knowledge = importer.import_knowledge(
        occupations_path=ESCO_DATA / "occupations_en.csv",
        skills_path=ESCO_DATA / "skills_en.csv",
        relations_path=(
            ESCO_DATA
            / "occupationSkillRelations_en.csv"
        ),
    )

    assert isinstance(
        knowledge,
        ExternalKnowledge,
    )

    assert knowledge.occupations
    assert knowledge.skills
    assert knowledge.occupation_skill_relations
    
def test_imported_relations_reference_existing_entities():

    importer = ESCOImporter()

    knowledge = importer.import_knowledge(
        occupations_path=ESCO_DATA / "occupations_en.csv",
        skills_path=ESCO_DATA / "skills_en.csv",
        relations_path=(
            ESCO_DATA
            / "occupationSkillRelations_en.csv"
        ),
    )

    occupation_ids = {
        occupation.id
        for occupation in knowledge.occupations
    }

    skill_ids = {
        skill.id
        for skill in knowledge.skills
    }

    assert all(
        relation.occupation_id in occupation_ids
        for relation in knowledge.occupation_skill_relations
    )

    assert all(
        relation.skill_id in skill_ids
        for relation in knowledge.occupation_skill_relations
    )
    
def test_import_keeps_latest_version_of_duplicate_entities():

    importer = ESCOImporter()

    knowledge = importer.import_knowledge(
        occupations_path=ESCO_DATA / "occupations_en.csv",
        skills_path=ESCO_DATA / "skills_en.csv",
        relations_path=(
            ESCO_DATA
            / "occupationSkillRelations_en.csv"
        ),
    )

    occupation = next(
        occupation
        for occupation in knowledge.occupations
        if occupation.id
        == (
            "http://data.europa.eu/esco/"
            "occupation/4d27152a-a8ee-4f5a-9f93-a2fb4fb2b2e3"
        )
    )

    assert occupation.preferred_label == (
        "early years teaching assistant"
    )
    
def test_import_keeps_latest_version_of_duplicate_entities(
    tmp_path,
):

    occupations_csv = tmp_path / "occupations.csv"

    occupations_csv.write_text(
        (
            "conceptUri,preferredLabel,description,altLabels,"
            "modifiedDate\n"
            "occupation-1,Old label,Old description,,"
            "2025-01-01T00:00:00Z\n"
            "occupation-1,New label,New description,,"
            "2025-06-01T00:00:00Z\n"
        ),
        encoding="utf-8",
    )

    skills_csv = tmp_path / "skills.csv"

    skills_csv.write_text(
        (
            "conceptUri,preferredLabel,description,altLabels,"
            "modifiedDate\n"
            "skill-1,Python,Old description,,"
            "2025-01-01T00:00:00Z\n"
            "skill-1,Python,New description,,"
            "2025-06-01T00:00:00Z\n"
        ),
        encoding="utf-8",
    )

    relations_csv = tmp_path / "relations.csv"

    relations_csv.write_text(
        (
            "occupationUri,occupationLabel,relationType,"
            "skillType,skillUri,skillLabel\n"
            "occupation-1,New label,essential,"
            "skill/competence,skill-1,Python\n"
        ),
        encoding="utf-8",
    )

    importer = ESCOImporter()

    knowledge = importer.import_knowledge(
        occupations_path=occupations_csv,
        skills_path=skills_csv,
        relations_path=relations_csv,
    )

    assert knowledge.occupations[0].preferred_label == "New label"
    assert knowledge.occupations[0].description == "New description"
    assert knowledge.skills[0].description == "New description"
    
def test_imported_entities_have_unique_ids():

    importer = ESCOImporter()

    knowledge = importer.import_knowledge(
        occupations_path=ESCO_DATA / "occupations_en.csv",
        skills_path=ESCO_DATA / "skills_en.csv",
        relations_path=(
            ESCO_DATA
            / "occupationSkillRelations_en.csv"
        ),
    )

    occupation_ids = [
        occupation.id
        for occupation in knowledge.occupations
    ]

    skill_ids = [
        skill.id
        for skill in knowledge.skills
    ]

    assert len(occupation_ids) == len(set(occupation_ids))
    assert len(skill_ids) == len(set(skill_ids))