from operator import attrgetter

import pytest

from pytest_ast_transformer.transformer.wrapper import PytestFunctionProxy

func_source = """
    import pytest

    def test_func(): 
        assert True, 'some_msg'
"""

cls_source = """
    class TestX: 
        def test_func(self): assert True, 'some_msg'
"""


class TestWrapper:

    @pytest.mark.parametrize('source, expected', [
        (func_source, False),
        (cls_source, True)
    ])
    def test_is_class(self, testdir, source, expected):
        item = testdir.getitem(source)
        wrapper = PytestFunctionProxy(item)

        assert wrapper.is_class is expected

    def test_real_obj(self, testdir):
        item = testdir.getitem(func_source)
        wrapper = PytestFunctionProxy(item)

        assert wrapper.real_obj == item.obj

    @pytest.mark.parametrize('source, expected', [
        (func_source, type(None)),
        (cls_source, str)
    ])
    def test_real_cls_name(self, testdir, source, expected):
        item = testdir.getitem(source)
        wrapper = PytestFunctionProxy(item)

        assert isinstance(wrapper.real_cls_name, expected)

    def test_real_func_name(self, testdir):
        item = testdir.getitem(func_source)
        wrapper = PytestFunctionProxy(item)

        assert wrapper.real_func_name == item.obj.__name__

    def test_ctx_info_func(self, testdir):
        item = testdir.getitem(func_source)
        wrapper = PytestFunctionProxy(item)

        assert wrapper.ctx_info() == (item.module, item.fspath)

    def test_ctx_info_class(self, testdir):
        item = testdir.getitem(cls_source)
        wrapper = PytestFunctionProxy(item)

        assert wrapper.ctx_info() == (item.parent.module, item.parent.fspath)

    @pytest.mark.parametrize('source, expected', [
        (func_source, attrgetter('real_func_name')),
        (cls_source, attrgetter('real_cls_name')),
    ])
    def test_ctx_name(self, testdir, source, expected):
        item = testdir.getitem(source)
        wrapper = PytestFunctionProxy(item)

        assert wrapper.ctx_name == expected(wrapper)

    def test_set_func(self, testdir):
        item = testdir.getitem(func_source)
        wrapper = PytestFunctionProxy(item)

        def test_func_new(): pass

        wrapper.set_func(test_func_new)

        assert item.obj == test_func_new

    def test_set_cls(self, testdir):
        item = testdir.getitem(cls_source)
        wrapper = PytestFunctionProxy(item)

        class TestNew: pass

        wrapper.set_cls(TestNew)

        assert item.parent.cls == TestNew
