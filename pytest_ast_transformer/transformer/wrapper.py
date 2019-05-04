import ast
import inspect
import types
from typing import Optional

import pytest

from pytest_ast_transformer.transformer.code import Code
from pytest_ast_transformer.transformer.utils import save_tmp_file


class PytestFunctionProxy:
    """ Proxy class for `pytest.Function` with context.

        Warning: all `set_*` methods change original `pytest.Function`
    """
    code: Optional[Code]
    module: types.ModuleType
    pytest_func: pytest.Function

    is_class: bool
    is_transformed: bool
    real_obj: types.FunctionType
    real_cls_name: Optional[str]
    real_func_name: str

    def __init__(self, func: pytest.Function):
        self.pytest_func = func
        self.is_class = bool(self.pytest_func.cls)
        self.is_transformed = False

        self.real_obj = func.obj
        self.real_cls_name = getattr(self.pytest_func.cls, '__name__', None)
        self.real_func_name = self.pytest_func.obj.__name__

        self.code = None
        self.module = self.pytest_func.module
        self.fspath = self.pytest_func.fspath
        self.fspath_transformed = None

        setattr(self.module, 'transformer_tmp_files', set())

    @property
    def ast_tree(self) -> ast.AST:
        have_ast_tree = hasattr(self.module, 'ast_tree')

        if have_ast_tree:
            return getattr(self.module, 'ast_tree', None)

        return ast.parse(inspect.getsource(self.module))

    @property
    def ctx_name(self) -> str:
        if self.is_class:
            return self.real_cls_name
        return self.real_func_name

    @property
    def ctx_exception_msg(self) -> str:
        if self.is_class:
            return f'Class not found.'
        return f'Function not found.'

    @property
    def path_to_source(self) -> str:
        if self.is_transformed:
            return self.fspath_transformed
        return self.fspath

    def set_source(self, source: str):
        if self.is_transformed:
            self._set_temp_file_to_test(source)

    def set_ast_tree(self, tree: ast.AST):
        setattr(self.module, 'ast_tree', tree)

    def set_cls_method(self, fn_name: str, transformed_method: object):
        parent = self.pytest_func.getparent(pytest.Class)
        setattr(parent.obj, fn_name, transformed_method)

    def set_cls(self, transformed_cls: object):
        parent = self.pytest_func.getparent(pytest.Class)
        setattr(parent, 'obj', transformed_cls)

    def set_func(self, transformed_func: object):
        setattr(self.pytest_func, 'obj', transformed_func)

    def set_object(self, obj: object, last_code: Code = None):
        self.code = last_code
        self.is_transformed = True

        if self.is_class:
            self.set_cls(obj)
        else:
            self.set_func(obj)

    def _set_temp_file_to_test(self, source: str):
        path_to_file = save_tmp_file(source, self.pytest_func.name)

        self.module.__file__ = path_to_file
        self.module.transformer_tmp_files.add(path_to_file)
        self.fspath_transformed = path_to_file
