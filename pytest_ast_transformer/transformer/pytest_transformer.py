import types

from pytest_ast_transformer.exceptions import TransformedNotFound, ContextIsRequired
from pytest_ast_transformer.transformer.base import BaseTransformer
from pytest_ast_transformer.transformer.code import Code
from pytest_ast_transformer.transformer.wrapper import PytestFunctionProxy


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
        proxy.set_source(code_info.source)

        compiled_code = code_info.compile(proxy.path_to_source)

        ctx = self.exec_transformed(
            context=context,
            compiled=compiled_code,
        )
        transformed = ctx.get(proxy.ctx_name)

        if not transformed:
            raise TransformedNotFound(proxy.ctx_exception_msg)

        proxy.set_object(transformed, last_code=code_info)

        return code_info
