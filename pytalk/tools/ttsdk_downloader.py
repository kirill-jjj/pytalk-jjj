"""Script for downloading and installing the TeamTalk SDK."""

#!/usr/bin/env python3

# Modified from https://github.com/gumerov-amir/TTMediaBot

import platform
import shutil
import sys
from pathlib import Path

import bs4
import patoolib
import requests

from . import downloader

url = "https://bearware.dk/teamtalksdk"
VERSION_IDENTIFIER = "5.19"

cd = Path(__file__).parent.parent.resolve()


def get_url_suffix_from_platform() -> str:
    """Determine the correct URL suffix for the SDK.

    This is based on the current platform and architecture.
    """
    machine = platform.machine()
    if sys.platform == "win32":
        architecture = platform.architecture()
        if machine in {"AMD64", "x86"}:
            if architecture[0] == "64bit":
                return "win64"
            return "win32"
        sys.exit("Native Windows on ARM is not supported")
    elif sys.platform == "darwin":
        sys.exit("Darwin is not supported")
    elif machine in {"AMD64", "x86_64"}:
        return "ubuntu22_x86_64"
    elif "arm" in machine:
        return "raspbian_armhf"
    else:
        sys.exit("Your architecture is not supported")


def download() -> None:
    """Download the TeamTalk SDK from the official website."""
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    }
<<<<<<< HEAD
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    page = bs4.BeautifulSoup(r.text, features="html.parser")
    versions = page.find_all("li")
    version = [i for i in versions if VERSION_IDENTIFIER in i.text][-1].a.get("href")[
        0:-1
    ]
    download_url = (
        url
        + "/"
        + version
        + "/"
        + f"tt5sdk_{version}_{get_url_suffix_from_platform()}.7z"
    )
    print("Downloading from " + download_url)
    downloader.download_file(download_url, str(cd / "ttsdk.7z"))


def extract() -> None:
    """Extract the downloaded TeamTalk SDK archive."""
    try:
        (cd / "ttsdk").mkdir()
    except FileExistsError:
        shutil.rmtree(cd / "ttsdk")
        (cd / "ttsdk").mkdir()
    patoolib.extract_archive(str(cd / "ttsdk.7z"), outdir=str(cd / "ttsdk"))


def move() -> None:
    """Move the extracted SDK files to their final destination."""
    path = cd / "ttsdk" / next((cd / "ttsdk").iterdir())
    libraries = ["TeamTalk_DLL", "TeamTalkPy"]
    try:
        (cd / "implementation").mkdir(parents=True)
    except FileExistsError:
        shutil.rmtree(cd / "implementation")
        (cd / "implementation").mkdir(parents=True)
    for library in libraries:
        try:
            (path / "Library" / library).rename(cd / "implementation" / library)
        except OSError:
            shutil.rmtree(cd / "implementation" / library)
            (path / "Library" / library).rename(cd / "implementation" / library)
        try:
            (cd / "implementation" / "__init__.py").unlink()
        except OSError:
            pass
        finally:
            (cd / "implementation" / "__init__.py").open("w").write("")


def clean() -> None:
    """Clean up downloaded and extracted SDK files."""
    (cd / "ttsdk.7z").unlink()
    shutil.rmtree(cd / "ttsdk")
    shutil.rmtree(cd / "implementation" / "TeamTalkPy" / "test")


def install() -> None:
    """Install the TeamTalk SDK components."""
    print("Installing TeamTalk sdk components")
    try:
        print("Downloading latest sdk version")
        download()
    except requests.exceptions.RequestException as e:
        print("Failed to download sdk. Error: ", e)
        sys.exit(1)
    try:
        print("Downloaded. extracting")
        extract()
    except patoolib.util.PatoolError as e:
        print("Failed to extract sdk. Error: ", e)
        print(
            "This can typically happen, if you do not have 7zip or equivalent "
            "installed on your system."
        )
        print(
            "On debian based systems, you can install 7zip by running "
            "'sudo apt install p7zip'"
        )
        print("On Windows, you need to have 7zip installed and added to your PATH")
        sys.exit(1)
    print("Extracted. moving")
    move()
    if not (cd / "implementation" / "TeamTalk_DLL").exists():
        print("Failed to move TeamTalk_DLL")
        sys.exit(1)
    if not (cd / "implementation" / "TeamTalkPy").exists():
        print("Failed to move TeamTalkPy")
        sys.exit(1)
    print("moved. cleaning")
    clean()
    print("cleaned.")
    print("Installed")
