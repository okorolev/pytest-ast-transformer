import pytest

from pytest_ast_transformer.transformer.wrapper import PytestFunctionProxy
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
