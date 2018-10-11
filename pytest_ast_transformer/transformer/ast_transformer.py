import ast
import types
import inspect
import pathlib
from typing import Union, Dict

from pytest_ast_transformer.exceptions import TransformedNotFound
from pytest_ast_transformer.transformer.code import Code
from pytest_ast_transformer.transformer.wrapper import PytestFunctionProxy


class BaseTransformer(ast.NodeTransformer):
    context: dict

    def transform(self, obj: object, fspath: Union[str, bytes, pathlib.Path]) -> Code:
        """ Transform ast for `obj` and compile changed ast.

            For more information about `obj` see inspect.getfile()
        """
        source = inspect.getsource(obj)
        ast_tree = ast.parse(source)
        changed_tree = self.visit(ast_tree)
        code = compile(changed_tree, filename=fspath, mode="exec")

        return Code(ast_tree=changed_tree, code_obj=code)

    @staticmethod
    def exec_transformed(compiled: Union[types.CodeType, str], context: dict = None) -> Dict[str, object]:
        """ Exec compiled code with context. Return local context.
        """
        _local_ctx = {}
        _global_ctx = context or {}

        exec(compiled, _global_ctx, _local_ctx)

        return _local_ctx


class PytestTransformer(BaseTransformer):

    def rewrite_ast(self, proxy: PytestFunctionProxy) -> Code:
        """ Transform ast tree for `pytest.Function`.

            Support test classes and single functions.
        """
        context = self.merge_contexts(proxy.obj)

        return self._rewrite(proxy, context=context)

    def merge_contexts(self, obj: types.FunctionType) -> dict:
        """ Merge global pytest ctx and transformer ctx (see `BaseTransformer.context`)
        """
        return {
            **obj.__globals__,
            **self.context
        }

    def _rewrite(self, proxy: PytestFunctionProxy, *, context: dict) -> Code:
        """ Transform ast for class or function.
        """
        ctx_module, ctx_fspath = proxy.ctx_info()
        code_info = self.transform(ctx_module, ctx_fspath)

        ctx = self.exec_transformed(
            context=context,
            compiled=code_info.code_obj,
        )
        transformed = ctx.get(proxy.ctx_name)

        if not transformed:
            raise TransformedNotFound(proxy.ctx_exception_msg)

        proxy.set_object(transformed)

        return code_info
