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

    def test_set_source__file_changed(self, testdir):
        item = testdir.getitem(func_source)
        wrapper = PytestFunctionProxy(item)
        original_file = wrapper.module.__file__
        wrapper.is_transformed = True

        wrapper.set_source(func_source)

        assert wrapper.path_to_source == wrapper.fspath_transformed
        assert wrapper.module.__file__ is not original_file

    def test_set_source__file_not_changed(self, testdir):
        item = testdir.getitem(func_source)
        wrapper = PytestFunctionProxy(item)
        original_file = wrapper.module.__file__

        wrapper.set_source(func_source)

        assert wrapper.path_to_source == wrapper.fspath
        assert wrapper.module.__file__ is original_file

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

        assert item.obj is test_func_new

    def test_set_cls(self, testdir):
        item = testdir.getitem(cls_source)
        wrapper = PytestFunctionProxy(item)

        class TestNew: pass

        wrapper.set_cls(TestNew)

        assert item.parent.cls is TestNew

    def test_set_cls_method(self, testdir):
        item = testdir.getitem(cls_source)
        wrapper = PytestFunctionProxy(item)

        class TestNew:
            def test_x(self): pass

        method = TestNew().test_x

        wrapper.set_cls_method('test_func', method)

        assert getattr(item.parent.obj, 'test_func') is method
