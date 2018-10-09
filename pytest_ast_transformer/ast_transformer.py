import ast
import types
import inspect
import pathlib
from typing import Union, Optional

import pytest

from pytest_ast_transformer.exceptions import TransformedNotFound


class BaseTransformer(ast.NodeTransformer):
    context: dict

    def transform(self, obj: object, fspath: Union[str, bytes, pathlib.Path]) -> types.CodeType:
        source = inspect.getsource(obj)
        ast_tree = ast.parse(source)
        changed_tree = self.visit(ast_tree)

        return compile(changed_tree, filename=fspath, mode="exec")

    @staticmethod
    def exec_transformed(compiled: Union[types.CodeType, str], name: str, context: dict = None) -> Optional[object]:
        _local_ctx = {}
        _global_ctx = context or {}

        exec(compiled, _global_ctx, _local_ctx)

        return _local_ctx.get(name)


class PytestTransformer(BaseTransformer):

    def rewrite_ast(self, func: pytest.Function):
        is_class = func.cls
        context = self.merge_contexts(func.obj)

        if is_class:
            self._rewrite_class(func, context)
        else:
            self._rewrite_func(func, context)

    def merge_contexts(self, obj: types.FunctionType) -> dict:
        return {
            **obj.__globals__,
            **self.context
        }

    def _rewrite_class(self, func: pytest.Function, context: dict = None):
        func_name = func.obj.__name__
        compiled_code = self.transform(func.parent.module, func.parent.fspath)

        transformed_cls = self.exec_transformed(
            name=func.cls.__name__,
            context=context,
            compiled=compiled_code,
        )
        transformed_method = getattr(transformed_cls, func_name, None)

        if not transformed_cls or not transformed_method:
            raise TransformedNotFound(func=transformed_method, cls=transformed_cls)

        setattr(func.parent.cls, func_name, transformed_method)

    def _rewrite_func(self, func: pytest.Function, context: dict = None):
        compiled_code = self.transform(func.module, func.fspath)

        transformed_func = self.exec_transformed(
            name=func.name,
            context=context,
            compiled=compiled_code,
        )

        if not transformed_func:
            raise TransformedNotFound(func=transformed_func)

        setattr(func, 'obj', transformed_func)
