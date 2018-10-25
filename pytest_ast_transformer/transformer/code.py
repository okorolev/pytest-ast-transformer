import ast
import types
import typing

import astor


class Code(typing.NamedTuple):
    ast_tree: ast.AST
    context: dict

    @property
    def source(self) -> str:
        return astor.to_source(self.ast_tree)

    def compile(self, filename: str = '<no_file>') -> types.CodeType:
        return compile(self.ast_tree, filename=filename, mode='exec')
