from __future__ import annotations

from pathlib import Path

from src.common import OUTPUT_PATH


translations_output = OUTPUT_PATH / "Bible Translations"


def write_translations(output_path: Path = translations_output) -> None:
    """Export one markdown file per translation (metadata + overview).

    TODO: implement. Should query the Translation table and render one
    note per translation under ``output_path``.
    """
    output_path.mkdir(parents=True, exist_ok=True)

    # TODO: query Translation rows and render one note per translation

    print(f"Wrote 0 translation files to: {output_path}")
