import csv
from pathlib import Path


class ESCOCSVReader:

    def read(
        self,
        path: Path,
    ) -> list[dict[str, str]]:

        with path.open(
            mode="r",
            encoding="utf-8",
            newline="",
        ) as file:

            reader = csv.DictReader(
                file,
            )

            return list(reader)