from pathlib import Path


from career_agent.adapters.esco_adapter import ESCOAdapter
from career_agent.adapters.esco_csv_reader import ESCOCSVReader
from career_agent.models.external_knowledge import ExternalKnowledge


class ESCOImporter:

    def __init__(
        self,
        reader: ESCOCSVReader | None = None,
        adapter: ESCOAdapter | None = None,
    ):
        self._reader = reader or ESCOCSVReader()
        self._adapter = adapter or ESCOAdapter()

    def import_knowledge(
        self,
        occupations_path: Path,
        skills_path: Path,
        relations_path: Path,
    ) -> ExternalKnowledge:

        occupation_records = self._reader.read(
            occupations_path,
        )

        skill_records = self._reader.read(
            skills_path,
        )

        relation_records = self._reader.read(
            relations_path,
        )

        occupation_records = self._keep_latest_versions(
            occupation_records,
        )

        skill_records = self._keep_latest_versions(
            skill_records,
        )

        return self._adapter.adapt_knowledge(
            skill_records=skill_records,
            occupation_records=occupation_records,
            relation_records=relation_records,
        )
        
    def _keep_latest_versions(
        self,
        records: list[dict],
    ) -> list[dict]:

        latest_by_uri = {}

        for record in records:

            uri = record["conceptUri"]

            current = latest_by_uri.get(uri)

            if (
                current is None
                or record["modifiedDate"]
                > current["modifiedDate"]
            ):
                latest_by_uri[uri] = record

        return list(latest_by_uri.values())
    
    