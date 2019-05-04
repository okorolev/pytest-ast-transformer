import ast
import types
from typing import Union, Dict

import astor

from pytest_ast_transformer.transformer.code import Code


class BaseTransformer(ast.NodeTransformer):
    context: dict = None
    allow_inheritance_ctx: bool = False

    def transform(self, ast_tree: ast.AST, context: dict, changed: bool = False) -> Code:
        """ Transform ast for `source`
        """
        changed_tree = self.visit(ast_tree)

        if changed:
            # TODO: this is hack (line fix)
            changed_tree = ast.parse(astor.to_source(changed_tree))

        return Code(ast_tree=changed_tree, context=context)

    @staticmethod
    def exec_transformed(compiled: Union[types.CodeType, str], context: dict = None) -> Dict[str, object]:
        """ Exec compiled code with context. Return local context.
        """
        _local_ctx = {}
        _global_ctx = context or {}

        exec(compiled, _global_ctx, _local_ctx)

        return _local_ctx
