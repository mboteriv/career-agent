from pathlib import Path

from career_agent.models.candidate_profile import (
    CandidateProfile,
)


class CandidateProfileRepository:

    def __init__(
        self,
        file_path: str = "candidate_profile.json",
    ):

        self._file_path = Path(
            file_path,
        )

    def save(
        self,
        profile: CandidateProfile,
    ) -> None:

        self._file_path.write_text(
            profile.model_dump_json(
                indent=4,
            ),
            encoding="utf-8",
        )

    def load(
        self,
    ) -> CandidateProfile:

        if not self._file_path.exists():
            return CandidateProfile()

        return CandidateProfile.model_validate_json(
            self._file_path.read_text(
                encoding="utf-8",
            ),
        )
        
    def exists(
        self,
    ) -> bool:

        return self._file_path.exists()
    
    def delete(
        self,
    ) -> None:

        if self._file_path.exists():
            self._file_path.unlink()