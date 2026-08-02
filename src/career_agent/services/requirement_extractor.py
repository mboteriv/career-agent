from career_agent.models.job_requirements import (
    JobRequirements,
)
from career_agent.models.language_skill import LanguageSkill
from career_agent.models.language_skill import LanguageSkill
import re


class RequirementExtractor:
    
    _KNOWN_SKILLS = {
        "Python": [
            "python",
        ],
        "Docker": [
            "docker",
        ],
        "Kubernetes": [
            "kubernetes",
            "k8s",
        ],
        "Java": [
            "java",
        ],
        "JavaScript": [
            "javascript",
        ],
        "TypeScript": [
            "typescript",
        ],
        "C#": [
            "csharp",
        ],
        "Go": [
            "go",
        ],
        "Rust": [
            "rust",
        ],
        "SQL": [
            "sql",
        ],
        "PostgreSQL": [
            "postgresql",
            "postgres",
        ],
        "MySQL": [
            "mysql",
        ],
        "MongoDB": [
            "mongodb",
            "mongo",
        ],
        "Redis": [
            "redis",
        ],
        "Git": [
            "git",
        ],
        "Linux": [
            "linux",
        ],
        "AWS": [
            "aws",
        ],
        "Azure": [
            "azure",
        ],
        "GCP": [
            "gcp",
            "google cloud",
        ],
        "Terraform": [
            "terraform",
        ],
    }
    
    _KNOWN_LANGUAGES = {
        "English": [
            "english",
        ],
        "Spanish": [
            "spanish",
        ],
        "French": [
            "french",
        ],
        "German": [
            "german",
        ],
    }
    
    _LANGUAGE_LEVELS = [
        "C2",
        "C1",
        "B2",
        "B1",
        "A2",
        "A1",
        "Native",
        "Fluent",
        "Intermediate",
        "Basic",
        "Spoken",
        "Written",
    ]

    def extract(
        self,
        description: str,
    ) -> JobRequirements:
        text = description.lower()

        return JobRequirements(
            skills=self._extract_skills(
                text,
            ),
            languages=self._extract_languages(
                text,
            ),
            years_experience=self._extract_experience(
                text,
            ),
        )
    
    def _extract_skills(
        self,
        text: str,
    ) -> list[str]:

        skills = []

        for skill, aliases in self._KNOWN_SKILLS.items():

            if any(
                alias in text
                for alias in aliases
            ):
                skills.append(skill)

        return skills
    
    def _extract_languages(
        self,
        text: str,
    ) -> list[LanguageSkill]:

        languages = []

        for language, aliases in self._KNOWN_LANGUAGES.items():

            if any(
                alias in text
                for alias in aliases
            ):
                languages.append(
                    LanguageSkill(
                        language=language,
                        level=self._extract_language_level(
                            text,
            ),
                    )
                )

        return languages
    
    def _extract_language_level(
        self,
        text: str,
    ) -> str:

        upper_text = text.upper()

        for level in (
            "C2",
            "C1",
            "B2",
            "B1",
            "A2",
            "A1",
        ):
            if level in upper_text:
                return level

        

        if "native" in text:
            return "Native"

        if "fluent" in text:
            return "Fluent"

        return "Unknown"
    
    def _extract_experience(
        self,
        text: str,
    ) -> int | None:

        match = re.search(
            r"(\d+)\+?\s+years?",
            text,
        )

        if match:
            return int(
                match.group(1),
            )

        return None