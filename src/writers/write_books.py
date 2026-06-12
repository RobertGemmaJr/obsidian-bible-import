from __future__ import annotations

from pathlib import Path

from src.common import OUTPUT_PATH


books_output = OUTPUT_PATH / "Bible Books"


def write_books(output_path: Path = books_output) -> None:
    """Export one markdown file per book (metadata + chapter index).

    TODO: implement. Should query the Book table and render one note
    per book under ``output_path``.
    """
    output_path.mkdir(parents=True, exist_ok=True)

    # TODO: query Book rows and render one note per book

    print(f"Wrote 0 book files to: {output_path}")
