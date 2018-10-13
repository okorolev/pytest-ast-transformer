import pytest

from pytest_ast_transformer.transformer.wrapper import PytestFunctionProxy
from pytest_ast_transformer.exceptions import ContextIsRequired
from tests.transformer import AssertTransformer


class TestContext:

    def test_check_merged_contexts(self, testdir):
        source = """
            import pytest
            
            def test_func(): 
                assert True, 'some_msg'
        """
        item: pytest.Function = testdir.getitem(source)
        wrapper = PytestFunctionProxy(item)

        ctx = AssertTransformer().merge_contexts(wrapper.real_obj)

        assert 'pytest' in ctx
        assert 'my_assert' in ctx

    def test_run_without_context(self, testdir):
        source = """
            import pytest

            def test_func(): 
                assert True, 'some_msg'
        """
        item: pytest.Function = testdir.getitem(source)
        wrapper = PytestFunctionProxy(item)

        transformer = AssertTransformer()
        transformer.context = None

        with pytest.raises(ContextIsRequired) as error:
            transformer.merge_contexts(wrapper.real_obj)
