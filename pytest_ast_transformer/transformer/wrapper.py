import pytest
import _pytest


# def set_module(self, path: str):
#     self._func.module.__file__ = path

class PytestFunctionProxy:
    """ Proxy class for `pytest.Function` with context.

        Warning: all `set_*` method change original `pytest.Function`
    """

    def __init__(self, func: pytest.Function):
        self._func = func
        self.is_transformed = False
        self.is_class = bool(self._func.cls)
        # self._last_code = None

    def __getattr__(self, item):
        return getattr(self._func, item)

    real_cls_name: str = property(lambda self: self._func.cls.__name__)
    real_func_name: str = property(lambda self: self._func.obj.__name__)

    def ctx_info(self):
        fspath = self._func.parent.fspath if self.is_class else self._func.fspath
        module = self._func.parent.module if self.is_class else self._func.module

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

    def set_cls_method(self, fn_name, transformed_method):
        parent = self._func.getparent(_pytest.python.Class)
        setattr(parent.obj, fn_name, transformed_method)

    def set_cls(self, transformed_cls):
        parent = self._func.getparent(_pytest.python.Class)
        setattr(parent, 'obj', transformed_cls)

    def set_func(self, transformed_func):
        setattr(self._func, 'obj', transformed_func)

    def set_object(self, obj):
        if self.is_class:
            self.set_cls(obj)
        else:
            self.set_func(obj)
