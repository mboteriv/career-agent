from pathlib import Path
import json


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(provider: str, filename: str) -> dict:
    path = FIXTURES_DIR / provider / filename

    with path.open(encoding="utf-8") as file:
        return json.load(file)