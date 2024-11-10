# -*- coding: utf-8 -*-
from pathlib import Path

from core.llm.ollama import DocstringGenerator


if __name__ == "__main__":
    current_path = Path(".")
    file_to_check = current_path / "core" / "workers" / "base.py"

    llm = DocstringGenerator("llama3.2:3b-instruct-fp16")

    text = llm.propose_docstrings_to_file(file_to_check, True)

    print(text)
