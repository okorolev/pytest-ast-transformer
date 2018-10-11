import ast
import types
import typing

import astunparse


class Code(typing.NamedTuple):
    ast_tree: ast.AST
    code_obj: types.CodeType

    @property
    def source(self) -> str:
        return astunparse.unparse(self.ast_tree)
