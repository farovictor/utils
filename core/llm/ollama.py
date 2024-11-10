# -*- coding: utf-8 -*-
from pathlib import Path

from langchain_ollama import OllamaLLM

from core.logger.log import get_logger

logger = get_logger("default")


class DocstringGenerator:

    def __init__(self, model: str, *args, **kwargs):
        self.llm = OllamaLLM(model=model)

    def propose_docstrings_to_file(
        self, file_path: Path, write_inplace: bool = False
    ) -> str:
        with open(file_path, "r") as file:
            file_content = file.read()

        prompt = (
            "<Instruction>"
            "The following Python file contains functions and classes that may lack docstrings. "
            "For each function and class, add high-quality, PEP 257-compliant docstrings that clearly describe the purpose of the function, "
            "its parameters, any raised exceptions, and the return values (if applicable). "
            "Follow Python best practices for readability, clarity, and completeness.\n\n"
            "Guidelines:\n"
            "1. **Docstring Format**: Write docstrings that are concise yet informative, following the PEP 257 convention. "
            "Include parameter descriptions, return types, exceptions raised, and any side effects.\n"
            "2. **Type Annotations**: Use accurate and explicit type annotations in function signatures. Reference types from the `typing` module (e.g., `Optional`, `Union`, `Callable`, `Any`, `List`, etc.), `types` module (e.g., `TracebackType`), and other relevant Python modules where appropriate. "
            "For async functions, use `Coroutine` from the `typing` module, and for any I/O-related objects, use types like `IO` or `TextIO` from `typing`.\n"
            "3. **Imports**: If you introduce new type annotations that require imports (e.g., `Optional`, `List`, `Dict`, `Coroutine`, `TracebackType`), ensure these imports are included at the top of the file. Avoid using incorrect or non-existent types (e.g., `asyncio.Coroutine`, which should be `typing.Coroutine`).\n"
            "4. **Class Attributes**: For classes, ensure that class attributes have proper docstrings and type hints where possible.\n"
            "5. **Compatibility**: Make sure the resulting code is valid and executable without any undefined references or missing imports. "
            "Avoid suggesting types that aren't standard or would result in a `NameError`.\n\n"
            "Output Requirements:\n"
            "1. Only output the modified file content with added docstrings and any necessary imports.\n"
            "2. Do not add explanations, comments, or any additional text outside of the updated file content.\n\n"
            "<File Content>"
            f"{file_content}"
        )

        response = self.llm.invoke(prompt)

        if write_inplace:
            with open(file_path, "w") as file:
                file.write(response.strip())

        return response.strip()
