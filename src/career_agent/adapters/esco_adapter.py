from career_agent.models.external_knowledge import ExternalKnowledge
from career_agent.models.occupation_skill_relation import OccupationSkillRelation
from career_agent.models.semantic_entity import SemanticEntity


class ESCOAdapter:

    def adapt_skill(
        self,
        record: dict,
    ) -> SemanticEntity:

        uri = record["conceptUri"]

        aliases = [
            alias
            for alias in record.get("altLabels", "").splitlines()
            if alias
        ]

        return SemanticEntity(
            id=uri,
            preferred_label=record["preferredLabel"],
            description=record.get("description"),
            aliases=aliases,
            external_ids={
                "esco": uri,
            },
        )
        
    def adapt_occupation(
        self,
        record: dict,
    ) -> SemanticEntity:

        uri = record["uri"]

        return SemanticEntity(
            id=uri,
            preferred_label=record["preferredLabel"],
            description=record.get("description"),
            aliases=record.get("altLabels", []),
            external_ids={
                "esco": uri,
            },
        )
        
    def adapt_occupation(
        self,
        record: dict,
    ) -> SemanticEntity:

        uri = record["conceptUri"]

        aliases = [
            alias
            for alias in record.get("altLabels", "").splitlines()
            if alias
        ]

        return SemanticEntity(
            id=uri,
            preferred_label=record["preferredLabel"],
            description=record.get("description"),
            aliases=aliases,
            external_ids={
                "esco": uri,
            },
        )
    def adapt_occupation_skill_relation(
        self,
        record: dict,
    ) -> OccupationSkillRelation:

        return OccupationSkillRelation(
            occupation_id=record["occupationUri"],
            skill_id=record["skillUri"],
            relation_type=record["relationType"],
        )
        
    def adapt_knowledge(
        self,
        skill_records: list[dict],
        occupation_records: list[dict],
        relation_records: list[dict],
    ) -> ExternalKnowledge:

        return ExternalKnowledge(
            skills=[
                self.adapt_skill(record)
                for record in skill_records
            ],
            occupations=[
                self.adapt_occupation(record)
                for record in occupation_records
            ],
            occupation_skill_relations=[
                self.adapt_occupation_skill_relation(record)
                for record in relation_records
            ],
        )