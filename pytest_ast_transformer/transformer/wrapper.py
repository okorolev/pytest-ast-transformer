import types
from typing import Optional

import pytest
import _pytest


class PytestFunctionProxy:
    """ Proxy class for `pytest.Function` with context.

        Warning: all `set_*` method change original `pytest.Function`
    """
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

        self._last_code = None

    def ctx_info(self):
        fspath = self.pytest_func.parent.fspath if self.is_class else self.pytest_func.fspath
        module = self.pytest_func.parent.module if self.is_class else self.pytest_func.module

        if self.is_transformed:
            return ()

        return module, fspath

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

    def set_cls_method(self, fn_name: str, transformed_method: object):
        parent = self.pytest_func.getparent(_pytest.python.Class)
        setattr(parent.obj, fn_name, transformed_method)

    def set_cls(self, transformed_cls: object):
        parent = self.pytest_func.getparent(_pytest.python.Class)
        setattr(parent, 'obj', transformed_cls)

    def set_func(self, transformed_func: object):
        setattr(self.pytest_func, 'obj', transformed_func)

    def set_object(self, obj: object):
        if self.is_class:
            self.set_cls(obj)
        else:
            self.set_func(obj)
