"""
Tasks to be invoked via "poetry run".

Any task added here must also be specified as a "script" in pyproject.toml.
"""

import os
import subprocess
import sys
from typing import List, Union

repo_root = os.path.dirname(__file__)


def _command(command: Union[List[str], str], shell: bool = False):
    command_exit_code = subprocess.call(
        command,
        cwd=repo_root,
        shell=shell,
    )

    if command_exit_code != 0:
        sys.exit(command_exit_code)


def setup():
    import nltk

    nltk.download("omw-1.4")
    nltk.download("wordnet")

    _command(["spacy", "download", "en_core_web_sm"])


def format():
    _command(["black", "."])
    _command(["isort", "."])
