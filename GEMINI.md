# Gemini Context: Pytalk Project

## 1. Project Overview

**Pytalk** is a Python library designed to simplify the creation of bots for the TeamTalk 5 Conferencing System. It provides a high-level, asynchronous, event-driven API that wraps the underlying TeamTalk 5 SDK, abstracting away much of the low-level complexity.

The library's architecture is centered around two main classes:
-   `TeamTalkBot`: The primary entry point for creating a bot. It manages the asyncio event loop, dispatches events, and holds multiple server connections.
-   `TeamTalkInstance`: Represents a single connection to a TeamTalk server. It handles all direct communication with the SDK, event processing, and actions related to that specific server.

The project is built for Python 3.11+ and relies heavily on `asyncio` for its asynchronous operations.

## 2. Project Structure

-   `.github/workflows/`: Contains GitHub Actions workflows for Continuous Integration (CI).
-   `docs/`: Contains all files related to the Sphinx documentation.
-   `for_gemini/`: A dedicated directory for user-provided files for the Gemini agent. This directory is ignored by Git.
-   `pytalk/`: The main source code for the library.
    -   `implementation/`: Houses the pre-compiled TeamTalk 5 SDK files. This directory is populated automatically by a download script.
    -   `tools/`: Contains helper scripts, primarily for downloading the SDK.
-   **Root Directory**: Contains project configuration files (`pyproject.toml`, `.pre-commit-config.yaml`, etc.), the main README, and license information.

## 3. Commit Message Conventions

To maintain a clear, readable, and automated commit history, this project adheres to the following conventions for all Git commits.

-   **Language**: All commit messages must be written in English.
-   **Structure**: Commits must follow the **Conventional Commits** specification.
-   **Emoji Prefix**: Each commit message should be prefixed with a relevant **Gitmoji** icon.

### Conventional Commits

This is a specification for adding human and machine-readable meaning to commit messages. It provides a simple set of rules for creating an explicit commit history, which makes it easier to write automated tools on top of. The commit message should be structured as follows:

```
<gitmoji> <type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

-   **type**: Must be one of the following: `feat` (new feature), `fix` (bug fix), `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
-   **scope**: An optional noun describing a section of the codebase (e.g., `instance`, `docs`, `ci`).
-   **subject**: A concise description of the change.

**Reference**: [Conventional Commits Specification](https://www.conventionalcommits.org/)

### Gitmoji

Gitmoji is an emoji guide for commit messages, making them easier to identify and browse. The chosen emoji should correspond to the type and content of the commit.

**Example Commit Messages:**
-   `✨ feat(auth): implement user registration endpoint`
-   `🐛 fix(streamer): prevent crash on empty audio data`
-   `📚 docs(api): add documentation for the new `Server` class`

**Reference**: [Gitmoji Website & Emoji List](https://gitmoji.dev/)

## 4. File-by-File Breakdown

### 4.1. Configuration & Metadata

-   **`.gitignore`**: A standard Python gitignore file. It excludes common files like `__pycache__`, virtual environments (`.venv`), build artifacts (`dist/`, `build/`), and test reports. It also specifically ignores the downloaded SDK files (`pytalk/implementation/TeamTalk*`) and the `/for_gemini/` directory.
-   **`.pre-commit-config.yaml`**: Configures pre-commit hooks to ensure code quality before commits. It uses:
    -   `pre-commit-hooks`: For basic checks like trailing whitespace, file endings, and syntax validation (YAML, TOML, AST).
    -   `black`: For consistent code formatting.
    -   `flake8`: For linting, with plugins (`flake8-docstrings`, `darglint`) to enforce docstring standards.
-   **`.python-version`**: Specifies that the project uses Python `3.11`. This is likely used by tools like `pyenv`.
-   **`.readthedocs.yaml`**: Configuration for building the documentation on Read the Docs. It defines the build environment (Ubuntu 22.04), system dependencies (`libpulse0`, `p7zip-full`), Python version (3.11), and the steps to install project dependencies using `uv` before building the Sphinx documentation.
-   **`pyproject.toml`**: The primary project definition file.
    -   `[project]`: Defines metadata like the package name (`py-talk-ex`), version, dependencies (`beautifulsoup4`, `patool`, `requests`), and supported Python version (`>=3.11`).
    -   `[project.optional-dependencies]`: Defines dependencies for building documentation (`docs`).
    -   `[tool.black]` & `[tool.flake8]`: Configures the behavior of the Black formatter and Flake8 linter.
    -   `[dependency-groups]`: Defines development dependencies (`dev`), such as `pre-commit`.
-   **`uv.lock`**: The lock file generated by `uv`. It pins the exact versions of all dependencies and transitive dependencies to ensure reproducible builds.
-   **`tea.yaml`**: A configuration file for `tea.xyz`, a universal package manager. It specifies the code owners for the project.

### 4.2. Core Library (`pytalk/`)

-   **`__init__.py`**: The main entry point of the `pytalk` package. Its primary role is to ensure the TeamTalk SDK is available. It attempts to import the SDK, and if it fails (i.e., the SDK hasn't been downloaded), it calls `download_sdk.py` to fetch and install it. It also exposes the main classes (`TeamTalkBot`, `Channel`, `User`, etc.) for easy import.
-   **`bot.py`**: Defines the `TeamTalkBot` class, the main user-facing class. It manages the asyncio event loop, holds a list of `TeamTalkInstance` objects (one for each server connection), and contains the event dispatching system (`@bot.event` decorator).
-   **`instance.py`**: Defines the `TeamTalkInstance` class, which is the heart of the library. This class inherits from the raw `TeamTalk5` SDK class and wraps its functionality. It handles connecting, logging in, processing the event queue (`_process_events`), sending commands, managing user/channel objects, and implementing features like automatic reconnection with backoff.
-   **`_utils.py`**: A collection of internal helper functions. This includes functions for waiting for specific SDK events (`_waitForEvent`), converting between volume percentages and internal SDK values (`percent_to_ref_volume`), and dynamically getting/setting attributes on SDK objects (`_get_tt_obj_attribute`).
-   **`audio.py`**: Defines wrapper classes (`AudioBlock`, `MuxedAudioBlock`) for audio data received from the server. It also defines the CTypes function factories (`_AcquireUserAudioBlock`, `_ReleaseUserAudioBlock`) for safe interaction with the SDK's audio buffer.
-   **`backoff.py`**: Implements the `Backoff` class, which provides an exponential backoff strategy with jitter. This is used by `TeamTalkInstance` to handle connection retries without overwhelming the server.
-   **`channel.py`**: Defines the `Channel` class, a high-level wrapper around the SDK's channel object. It provides methods for sending messages to the channel, getting users/files, and managing channel properties.
-   **`codec.py`**: Defines the `CodecType` helper class, which allows accessing SDK media codec identifiers (e.g., `CodecType.WEBM_VP8`) using user-friendly names.
-   **`device.py`**: Defines the `SoundDevice` class, a wrapper for the SDK's `SoundDevice` struct, making it easier to inspect available audio devices.
-   **`enums.py`**: Contains Pythonic enumerations and helper classes for various TeamTalk concepts, such as `TeamTalkServerInfo` (a dataclass for server connection details), `UserStatusMode`, and the `Status` helper for building complex user statuses.
-   **`exceptions.py`**: Defines custom exceptions for the library, like `TeamTalkException` (the base exception) and `PermissionError`.
-   **`message.py`**: Defines classes for different message types (`ChannelMessage`, `DirectMessage`, `BroadcastMessage`). They inherit from a base `Message` class and provide context-aware `reply()` methods.
-   **`permission.py`**: Defines the `Permission` helper class (using a metaclass) to provide easy, attribute-style access to the SDK's user permission flags (e.g., `Permission.KICK_USERS`).
-   **`server.py`**: Defines the `Server` class, which represents the server itself and provides methods for server-wide actions like getting all users/channels, managing server properties, and sending broadcast messages.
-   **`statistics.py`**: Defines the `Statistics` class, a wrapper for the server statistics object provided by the SDK.
-   **`streamer.py`**: Contains the `Streamer` class for streaming audio to a channel. It uses `ffmpeg` and `yt-dlp` (if available) to process local files and URLs into a raw PCM audio stream that can be fed into the TeamTalk SDK.
-   **`subscription.py`**: Defines the `Subscription` helper class, similar to `Permission`, for accessing user subscription flags (e.g., `Subscription.USER_TEXTMESSAGE`).
-   **`tt_file.py`**: Defines the `RemoteFile` class, a wrapper for file objects on the server.
-   **`user.py`**: Defines the `User` class, a wrapper for a connected user, providing methods to send direct messages, kick, ban, etc.
-   **`user_account.py`**: Defines `UserAccount` and `BannedUserAccount` classes, which represent stored user accounts on the server (as opposed to currently connected users).

### 4.3. SDK Downloader (`pytalk/tools/`)

-   **`downloader.py`**: A simple utility with a `download_file` function that uses the `requests` library to download a file from a URL.
-   **`ttsdk_downloader.py`**: The main script responsible for fetching the TeamTalk SDK. It scrapes the BearWare.dk website to find the correct SDK version (`5.15`), downloads the 7z archive for the appropriate OS and architecture, extracts it using `patoolib`, and moves the necessary `TeamTalk_DLL` and `TeamTalkPy` folders into the `pytalk/implementation/` directory.

### 4.4. Documentation (`docs/`)

-   **`conf.py`**: The main Sphinx configuration file. It sets up the project version, extensions (`napoleon`, `autodoc`, etc.), HTML theme (`scrolls`), and other settings.
-   **`index.rst`**: The main landing page for the documentation.
-   **`api.rst`**: Uses `autodoc` directives to generate the API reference from the docstrings in the source code.
-   **`events.rst`**: Documents the available events using `csv-table` directives, which pull data from the `.csv` files in `_static/csv/`.
-   **`whats-new.rst`**: The project's changelog.
-   **`make.bat` & `Makefile`**: Build scripts for Sphinx on Windows and Unix-like systems, respectively.

### 4.5. Continuous Integration (`.github/workflows/`)

-   **`ci.yaml`**: Defines the GitHub Actions CI pipeline.
    -   **`test` job**: Runs on every push and pull request across multiple operating systems (Ubuntu, Windows) and Python versions (3.9-3.13). It installs dependencies with `uv`, downloads the SDK, and runs `pre-commit`.
    -   **`builder_pytalk` job**: After tests pass, this job builds the Python wheel distribution.
    -   **`publisher_release` job**: This job runs only when a version tag (e.g., `v1.2.3`) is pushed. It verifies the tag is on the `master` branch and then publishes the built wheel to PyPI.

## 5. Areas for Investigation & Doubts

-   **Direct SDK Interaction (`ctypes`)**: The library interacts with the C-based SDK via `ctypes`. This is most evident in `pytalk/instance.py` and `pytalk/audio.py`. This layer is inherently complex and a common source of bugs (e.g., memory management, segmentation faults). The use of `_AcquireUserAudioBlock` and `_ReleaseUserAudioBlock` shows an awareness of this, but it remains a critical area to watch during development.
-   **Threading Model**: The core library is `asyncio`-based, but some parts use the `threading` module.
    -   `_utils._do_after`: This function runs a callback after a delay in a separate thread. This is a bit unusual in an asyncio application, where `asyncio.sleep()` and `loop.call_later()` would be more conventional. This might be a remnant of older code or a workaround for a specific blocking issue.
    -   `streamer.py`: The `Streamer` class heavily uses threads to manage the audio decoding (via `ffmpeg`) and the streaming loop (`_do_stream`) without blocking the main asyncio event loop. This is a valid approach but adds complexity.
-   **Testing Strategy**: The `ci.yaml` file runs `pre-commit`, but it does not run a dedicated test suite (e.g., `pytest` or `unittest`). The `pyproject.toml` also excludes a `tests/*` directory from `flake8`, suggesting tests might exist or are planned, but they are not currently integrated into the CI pipeline. A robust test suite would be crucial for verifying the correctness of the SDK interaction.
-   **Synchronous SDK Calls**: The `TeamTalkInstance.connect` and `login` methods are synchronous, blocking calls that wait for an event from the SDK. In the `async` methods (`initial_connect_loop`, `_reconnect`), these are correctly run in a thread pool executor (`run_in_executor`) to avoid blocking the event loop. This is a good pattern, but it highlights the challenge of integrating a synchronous, callback-based SDK into an async/await paradigm.
