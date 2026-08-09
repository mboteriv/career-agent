from career_agent.adapters.esco_adapter import ESCOAdapter
from career_agent.adapters.esco_csv_reader import ESCOCSVReader
from career_agent.models.knowledge import (
    Knowledge,
    KnowledgeCompiler,
)
from career_agent.models.occupation_skill_relation import OccupationSkillRelation
from career_agent.models.semantic_entity import (
    SemanticEntity,
)
from career_agent.models.external_knowledge import (
    ExternalKnowledge,
)
from pathlib import Path


ESCO_DATA = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "career_agent"
    / "data"
    / "esco"
    / "raw"
    / "v1.2.1"
)



def test_create_empty_knowledge():

    knowledge = Knowledge()

    assert knowledge.skills == []

    assert knowledge.occupations == []
    
def test_create_knowledge():

    python = SemanticEntity(
        id="python",
        preferred_label="Python",
    )

    translator = SemanticEntity(
        id="translator",
        preferred_label="Translator",
    )

    knowledge = Knowledge(
        skills=[
            python,
        ],
        occupations=[
            translator,
        ],
    )

    assert knowledge.skills == [
        python,
    ]

    assert knowledge.occupations == [
        translator,
    ]
    
def test_adapt_knowledge():

    skill_records = [
        {
            "conceptUri": "skill-1",
            "preferredLabel": "Python",
        },
        {
            "conceptUri": "skill-2",
            "preferredLabel": "SQL",
        },
    ]

    occupation_records = [
        {
            "conceptUri": "occupation-1",
            "preferredLabel": "Data analyst",
        },
    ]

    relation_records = [
        {
            "occupationUri": "occupation-1",
            "skillUri": "skill-1",
            "relationType": "essential",
        },
        {
            "occupationUri": "occupation-1",
            "skillUri": "skill-2",
            "relationType": "optional",
        },
    ]

    adapter = ESCOAdapter()

    knowledge = adapter.adapt_knowledge(
        skill_records,
        occupation_records,
        relation_records,
    )

    assert knowledge == ExternalKnowledge(
        skills=[
            SemanticEntity(
                id="skill-1",
                preferred_label="Python",
                external_ids={
                    "esco": "skill-1",
                },
            ),
            SemanticEntity(
                id="skill-2",
                preferred_label="SQL",
                external_ids={
                    "esco": "skill-2",
                },
            ),
        ],
        occupations=[
            SemanticEntity(
                id="occupation-1",
                preferred_label="Data analyst",
                external_ids={
                    "esco": "occupation-1",
                },
            ),
        ],
        occupation_skill_relations=[
            OccupationSkillRelation(
                occupation_id="occupation-1",
                skill_id="skill-1",
                relation_type="essential",
            ),
            OccupationSkillRelation(
                occupation_id="occupation-1",
                skill_id="skill-2",
                relation_type="optional",
            ),
        ],
    )
    

def test_compile_returns_knowledge():

    compiler = KnowledgeCompiler()

    external = ExternalKnowledge(
        skills=[
            SemanticEntity(
                id="python",
                preferred_label="Python",
            ),
        ],
    )

    knowledge = compiler.compile(
        external,
    )

    assert isinstance(
        knowledge,
        Knowledge,
    )

    assert knowledge.skills == external.skills
    
def test_compile_returns_empty_knowledge():

    compiler = KnowledgeCompiler()

    knowledge = compiler.compile(
        ExternalKnowledge(),
    )

    assert knowledge == Knowledge()
    
def test_compile_preserves_occupation_skill_relations():

    external = ExternalKnowledge(
        skills=[
            SemanticEntity(
                id="python",
                preferred_label="Python",
            ),
        ],
        occupations=[
            SemanticEntity(
                id="software-developer",
                preferred_label="Software developer",
            ),
        ],
        occupation_skill_relations=[
            OccupationSkillRelation(
                occupation_id="software-developer",
                skill_id="python",
                relation_type="essential",
            ),
        ],
    )

    compiler = KnowledgeCompiler()

    knowledge = compiler.compile(
        external,
    )

    assert knowledge == Knowledge(
        skills=external.skills,
        occupations=external.occupations,
        occupation_skill_relations=external.occupation_skill_relations,
    )
    
def test_compile_preserves_external_entities():

    skill = SemanticEntity(
        id="python",
        preferred_label="Python",
        description="Programming language",
        aliases=[
            "Python programming",
            "Python language",
        ],
        external_ids={
            "esco": "http://data.europa.eu/esco/skill/123",
        },
    )

    occupation = SemanticEntity(
        id="software-developer",
        preferred_label="Software developer",
        description="Develops software",
        aliases=[
            "Software engineer",
        ],
        external_ids={
            "esco": "http://data.europa.eu/esco/occupation/456",
        },
    )

    external = ExternalKnowledge(
        skills=[skill],
        occupations=[occupation],
    )

    compiler = KnowledgeCompiler()

    knowledge = compiler.compile(
        external,
    )

    assert knowledge.skills == [skill]
    assert knowledge.occupations == [occupation]
    assert knowledge.skills[0] is skill
    assert knowledge.occupations[0] is occupation
    
def test_adapt_skill_creates_semantic_entity():

    record = {
        "conceptUri": (
            "http://data.europa.eu/esco/skill/"
            "0005c151-5b5a-4a66-8aac-60e734beb1ab"
        ),
        "preferredLabel": "manage musical staff",
        "altLabels": (
            "manage music staff\n"
            "coordinate duties of musical staff\n"
            "direct musical staff\n"
            "manage staff of music"
        ),
        "description": (
            "Assign and manage staff tasks in areas such as "
            "scoring, arranging, copying music and vocal coaching."
        ),
    }

    adapter = ESCOAdapter()

    skill = adapter.adapt_skill(
        record,
    )

    assert skill == SemanticEntity(
        id=(
            "http://data.europa.eu/esco/skill/"
            "0005c151-5b5a-4a66-8aac-60e734beb1ab"
        ),
        preferred_label="manage musical staff",
        description=(
            "Assign and manage staff tasks in areas such as "
            "scoring, arranging, copying music and vocal coaching."
        ),
        aliases=[
            "manage music staff",
            "coordinate duties of musical staff",
            "direct musical staff",
            "manage staff of music",
        ],
        external_ids={
            "esco": (
                "http://data.europa.eu/esco/skill/"
                "0005c151-5b5a-4a66-8aac-60e734beb1ab"
            ),
        },
    )
    
def test_adapt_occupation_creates_semantic_entity():

    record = {
        "conceptUri": "http://data.europa.eu/esco/occupation/456",
        "preferredLabel": "Software developer",
        "description": "Develops software applications",
        "altLabels": (
            "Software engineer\n"
            "Application developer"
        ),
    }

    adapter = ESCOAdapter()

    occupation = adapter.adapt_occupation(
        record,
    )

    assert occupation == SemanticEntity(
        id="http://data.europa.eu/esco/occupation/456",
        preferred_label="Software developer",
        description="Develops software applications",
        aliases=[
            "Software engineer",
            "Application developer",
        ],
        external_ids={
            "esco": "http://data.europa.eu/esco/occupation/456",
        },
    )
    
def test_adapt_occupation_skill_relation():

    record = {
        "occupationUri": (
            "http://data.europa.eu/esco/occupation/456"
        ),
        "skillUri": (
            "http://data.europa.eu/esco/skill/123"
        ),
        "relationType": "essential",
    }

    adapter = ESCOAdapter()

    relation = adapter.adapt_occupation_skill_relation(
        record,
    )

    assert relation == OccupationSkillRelation(
        occupation_id=(
            "http://data.europa.eu/esco/occupation/456"
        ),
        skill_id=(
            "http://data.europa.eu/esco/skill/123"
        ),
        relation_type="essential",
    )
    
def test_adapt_empty_knowledge():

    adapter = ESCOAdapter()

    knowledge = adapter.adapt_knowledge(
        skill_records=[],
        occupation_records=[],
        relation_records=[],
    )

    assert knowledge == ExternalKnowledge()
    
def test_read_occupation_csv_row():

    row = {
        "conceptType": "Occupation",
        "conceptUri": (
            "http://data.europa.eu/esco/occupation/"
            "00030d09-2b3a-4efd-87cc-c4ea39d27c34"
        ),
        "preferredLabel": "technical director",
        "altLabels": (
            "director of technical arts\n"
            "technical supervisor\n"
            "head of technical\n"
            "technical and operations director\n"
            "technical manager\n"
            "head of technical department"
        ),
        "description": (
            "Technical directors realise the artistic visions "
            "of the creators within technical constraints."
        ),
    }

    adapter = ESCOAdapter()

    occupation = adapter.adapt_occupation(
        row,
    )

    assert occupation == SemanticEntity(
        id=(
            "http://data.europa.eu/esco/occupation/"
            "00030d09-2b3a-4efd-87cc-c4ea39d27c34"
        ),
        preferred_label="technical director",
        description=(
            "Technical directors realise the artistic visions "
            "of the creators within technical constraints."
        ),
        aliases=[
            "director of technical arts",
            "technical supervisor",
            "head of technical",
            "technical and operations director",
            "technical manager",
            "head of technical department",
        ],
        external_ids={
            "esco": (
                "http://data.europa.eu/esco/occupation/"
                "00030d09-2b3a-4efd-87cc-c4ea39d27c34"
            ),
        },
    )
    
def test_adapt_occupation_skill_relation():

    record = {
        "occupationUri": (
            "http://data.europa.eu/esco/occupation/"
            "00030d09-2b3a-4efd-87cc-c4ea39d27c34"
        ),
        "occupationLabel": "technical director",
        "relationType": "essential",
        "skillType": "knowledge",
        "skillUri": (
            "http://data.europa.eu/esco/skill/"
            "fed5b267-73fa-461d-9f69-827c78beb39d"
        ),
        "skillLabel": "theatre techniques",
    }

    adapter = ESCOAdapter()

    relation = adapter.adapt_occupation_skill_relation(
        record,
    )

    assert relation == OccupationSkillRelation(
        occupation_id=(
            "http://data.europa.eu/esco/occupation/"
            "00030d09-2b3a-4efd-87cc-c4ea39d27c34"
        ),
        skill_id=(
            "http://data.europa.eu/esco/skill/"
            "fed5b267-73fa-461d-9f69-827c78beb39d"
        ),
        relation_type="essential",
    )
    
def test_read_csv_returns_rows(
    tmp_path,
):

    csv_file = tmp_path / "occupations_en.csv"

    csv_file.write_text(
        (
            "conceptType,conceptUri,preferredLabel,altLabels,description\n"
            "Occupation,"
            "occupation-1,"
            "software developer,"
            "\"Software engineer\n"
            "Application developer\","
            "\"Develops software\"\n"
        ),
        encoding="utf-8",
        newline="",
    )

    reader = ESCOCSVReader()

    rows = reader.read(
        csv_file,
    )

    assert rows == [
        {
            "conceptType": "Occupation",
            "conceptUri": "occupation-1",
            "preferredLabel": "software developer",
            "altLabels": (
                "Software engineer\n"
                "Application developer"
            ),
            "description": "Develops software",
        },
    ]
    
def test_read_occupations_csv():

    reader = ESCOCSVReader()

    rows = reader.read(
        ESCO_DATA / "occupations_en.csv",
    )

    assert rows

    first = rows[0]

    assert first["conceptType"] == "Occupation"
    assert first["conceptUri"]
    assert first["preferredLabel"]
    assert first["altLabels"]
    assert first["description"]
    
def test_read_skills_csv():

    reader = ESCOCSVReader()

    rows = reader.read(
        ESCO_DATA / "skills_en.csv",
    )

    assert rows

    first = rows[0]

    assert first["conceptType"] == "KnowledgeSkillCompetence"
    assert first["conceptUri"]
    assert first["preferredLabel"]
    assert first["altLabels"]
    assert first["description"]
    
def test_read_occupation_skill_relations_csv():

    reader = ESCOCSVReader()

    rows = reader.read(
        ESCO_DATA / "occupationSkillRelations_en.csv",
    )

    assert rows

    first = rows[0]

    assert first["occupationUri"]
    assert first["occupationLabel"]
    assert first["relationType"]
    assert first["skillType"]
    assert first["skillUri"]
    assert first["skillLabel"]