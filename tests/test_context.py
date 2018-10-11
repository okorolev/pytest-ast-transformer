import pytest

from tests.transformer import AssertTransformer


class TestContext:

    def test_check_merged_contexts(self, testdir, mocker):
        source = """
            import pytest
            
            def test_func(): 
                assert True, 'some_msg'
        """
        testdir.makepyfile(source)
        item: pytest.Function = testdir.getitem(source)

        ctx = AssertTransformer().merge_contexts(item.obj)

        assert 'pytest' in ctx
        assert 'my_assert' in ctx
