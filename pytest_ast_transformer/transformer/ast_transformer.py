import ast
import types
from typing import Union, Dict

import astor

from pytest_ast_transformer.exceptions import TransformedNotFound, ContextIsRequired
from pytest_ast_transformer.transformer.code import Code
from pytest_ast_transformer.transformer.wrapper import PytestFunctionProxy


class BaseTransformer(ast.NodeTransformer):
    context: dict = None
    allow_inheritance_ctx: bool = False

    def transform(self, ast_tree: str, context: dict, changed: bool = False) -> Code:
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


class PytestTransformer(BaseTransformer):

    def rewrite_ast(self, proxy: PytestFunctionProxy, *, show_code=False) -> Code:
        """ Transform ast tree for `pytest.Function`.

            Support test classes and single functions.
        """
        context = self.merge_contexts(proxy.real_obj)

        if proxy.is_transformed and self.allow_inheritance_ctx:
            context = {**context, **proxy.code.context}

        code = self._rewrite(proxy, context=context)

        if show_code:
            print(code.source)

        return code

    def merge_contexts(self, obj: types.FunctionType) -> dict:
        """ Merge global pytest ctx and transformer ctx (see `BaseTransformer.context`).
            Return new context.
        """
        if self.context is None:
            raise ContextIsRequired()

        return {
            **obj.__globals__,
            **self.context
        }

    def _rewrite(self, proxy: PytestFunctionProxy, *, context: dict) -> Code:
        """ Transform ast for class or function.
        """
        code_info = self.transform(proxy.ast_tree, context, proxy.is_transformed)

        proxy.set_ast_tree(code_info.ast_tree)

        path_to_source = proxy.set_source(code_info.source)
        compiled_code = code_info.compile(path_to_source)

        ctx = self.exec_transformed(
            context=context,
            compiled=compiled_code,
        )
        transformed = ctx.get(proxy.ctx_name)

        if not transformed:
            raise TransformedNotFound(proxy.ctx_exception_msg)

        proxy.set_object(transformed, last_code=code_info)

        return code_info
