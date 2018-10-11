import pytest

from pytest_ast_transformer import exceptions

from tests.transformer import AssertTransformer


class TestTransforms:

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

    @pytest.mark.code
    def test_function__transformed_not_found(self, testdir, mocker):
        mocker.patch(
            'tests.transformer.AssertTransformer.exec_transformed',
            return_value=None,
        )
        source = """
            def test_func(): 
                assert True, 'some_msg'
        """
        testdir.makepyfile(source)
        item: pytest.Function = testdir.getitem(source)

        with pytest.raises(exceptions.TransformedNotFound) as error:
            AssertTransformer().rewrite_ast(item)

        assert error.value.func is None
        assert error.value.cls == '<Not expected>'
        assert 'Transformed object not found' in error.value.message

    @pytest.mark.code
    def test_class__transformed_not_found(self, testdir, mocker):
        mocker.patch(
            'tests.transformer.AssertTransformer.exec_transformed',
            return_value=None,
        )
        source = """
            class TestX: 
                def test_func(self): assert True, 'some_msg'
        """
        testdir.makepyfile(source)
        item: pytest.Function = testdir.getitem(source)

        with pytest.raises(exceptions.TransformedNotFound) as error:
            AssertTransformer().rewrite_ast(item)

        assert error.value.cls is None
        assert error.value.func is None
        assert 'Transformed object not found' in error.value.message
