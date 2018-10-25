import os
from typing import List
from tempfile import NamedTemporaryFile


def delete_tmp_files(tmp_files: List[str]) -> None:
    for f_name in tmp_files:
        try:
            os.unlink(f_name)
        except FileNotFoundError:
            pass


def save_tmp_file(source: str, test_name: str) -> str:
    with NamedTemporaryFile(suffix='.py', prefix=f'{test_name}_transformed', delete=False, mode='w') as py_file:
        py_file.write(source)

        return py_file.name
