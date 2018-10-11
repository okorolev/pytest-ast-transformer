import ast
import types
import typing
import inspect
import pathlib
from typing import Union, Optional

import pytest

from pytest_ast_transformer.exceptions import TransformedNotFound


class CodeInfo(typing.NamedTuple):
    ast_tree: ast.AST
    code: types.CodeType


class BaseTransformer(ast.NodeTransformer):
    context: dict

    def transform(self, obj: object, fspath: Union[str, bytes, pathlib.Path]) -> CodeInfo:
        """ Transform ast for `obj` and compile changed ast.

            For more information about `obj` see inspect.getfile()
        """
        source = inspect.getsource(obj)
        ast_tree = ast.parse(source)
        changed_tree = self.visit(ast_tree)
        code = compile(changed_tree, filename=fspath, mode="exec")

        return CodeInfo(ast_tree=changed_tree, code=code)

    @staticmethod
    def exec_transformed(compiled: Union[types.CodeType, str], name: str, context: dict = None) -> Optional[object]:
        """ Exec compiled code with context. Return python object.
        """
        _local_ctx = {}
        _global_ctx = context or {}

        exec(compiled, _global_ctx, _local_ctx)

        return _local_ctx.get(name)


class PytestTransformer(BaseTransformer):

    def rewrite_ast(self, func: pytest.Function) -> CodeInfo:
        """ Transform ast tree for `pytest.Function`.

            Support test classes and single functions.
        """
        is_class = func.cls
        context = self.merge_contexts(func.obj)

        if is_class:
            return self._rewrite_class(func, context)
        else:
            return self._rewrite_func(func, context)

    def merge_contexts(self, obj: types.FunctionType) -> dict:
        """ Merge global pytest ctx and transformer ctx (see `BaseTransformer.context`)
        """
        return {
            **obj.__globals__,
            **self.context
        }

    def _rewrite_class(self, func: pytest.Function, context: dict = None) -> CodeInfo:
        """ Transform ast for test class.
        """
        func_name = func.obj.__name__
        code_info = self.transform(func.parent.module, func.parent.fspath)

        transformed_cls = self.exec_transformed(
            name=func.cls.__name__,
            context=context,
            compiled=code_info.code,
        )
        transformed_method = getattr(transformed_cls, func_name, None)

        if not transformed_cls or not transformed_method:
            raise TransformedNotFound(func=transformed_method, cls=transformed_cls)

        setattr(func.parent.cls, func_name, transformed_method)

        return code_info

    def _rewrite_func(self, func: pytest.Function, context: dict = None) -> CodeInfo:
        """ Transform ast for single test function.
        """
        code_info = self.transform(func.module, func.fspath)

        transformed_func = self.exec_transformed(
            name=func.name,
            context=context,
            compiled=code_info.code,
        )

        if not transformed_func:
            raise TransformedNotFound(func=transformed_func)

        setattr(func, 'obj', transformed_func)

        return code_info
