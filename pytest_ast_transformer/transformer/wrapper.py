import types
import tempfile
from typing import Optional, Union

import pytest
from py._path.local import LocalPath

from pytest_ast_transformer.transformer.code import Code

PathLikeOrStr = Union[LocalPath, str]


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

    def __hash__(self):
        return hash(self.module)

    def __eq__(self, other):
        return self.module is other.module

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

    def set_source(self, source: str) -> PathLikeOrStr:
        test_name = self.pytest_func.name
        fspath = self.pytest_func.fspath
        module = self.module

        if self.is_transformed:
            # TODO: remove all tmp files
            with tempfile.NamedTemporaryFile(suffix='.py', prefix=test_name, delete=False, mode='w') as f:
                f.write(source)
                module.__file__ = f.name
                return f.name

        return fspath

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
