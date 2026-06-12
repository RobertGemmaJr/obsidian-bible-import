from __future__ import annotations

from pathlib import Path

from src.common import OUTPUT_PATH


chapters_output = OUTPUT_PATH / "Bible Books"


def write_chapters(output_path: Path = chapters_output) -> None:
    """Export one markdown file per chapter (metadata + chapter index + links to verses).

    TODO: implement. Should query the Book table and render one note
    per book under ``output_path``.
    """
    output_path.mkdir(parents=True, exist_ok=True)

    # TODO: query Book rows and render one note per book

    print(f"Wrote 0 book files to: {output_path}")
