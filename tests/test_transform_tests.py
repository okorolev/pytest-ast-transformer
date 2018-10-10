import pytest

from tests.transformer import AssertTransformer


class TestTransform:

    @pytest.mark.code
    def test_function__check_ast(self, testdir):
        source = """
            def test_func(): 
                assert True, 'some_msg'
        """
        testdir.makepyfile(source)
        item: pytest.Function = testdir.getitem(source)

        code = AssertTransformer().rewrite_ast(item)

        # Module -> FunctionDef -> Expr -> Call
        assert code.ast_tree.body[0].body[0].value.func.id == 'my_assert'
        assert code.ast_tree.body[0].body[0].value.args[0].value is True
        assert code.ast_tree.body[0].body[0].value.args[1].s == 'some_msg'

    @pytest.mark.code
    def test_class__check_ast(self, testdir):
        source = """
            class TestX: 
                def test_func(self): assert True, 'some_msg'
        """
        testdir.makepyfile(source)
        item: pytest.Function = testdir.getitem(source)

        code = AssertTransformer().rewrite_ast(item)

        # Module -> ClassDef -> FunctionDef -> Expr -> Call
        assert code.ast_tree.body[0].body[0].body[0].value.func.id == 'my_assert'
        assert code.ast_tree.body[0].body[0].body[0].value.args[0].value is True
        assert code.ast_tree.body[0].body[0].body[0].value.args[1].s == 'some_msg'
