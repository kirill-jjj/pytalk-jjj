"""Utility functions for downloading files."""

import shutil
from pathlib import Path

import requests


def download_file(url: str, file_path: str) -> None:
    """Download a file from a given URL to a specified path."""
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    }
    with (
        requests.get(url, headers=headers, stream=True, timeout=10) as r,
        Path(file_path).open("wb") as f,
    ):
        shutil.copyfileobj(r.raw, f)
