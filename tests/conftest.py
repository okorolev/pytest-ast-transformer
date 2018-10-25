import pytest

from pytest_mock import MockFixture

pytest_plugins = ["pytester"]


@pytest.fixture
def mocker(pytestconfig):
    result = MockFixture(pytestconfig)
    yield result
    result.stopall()


@pytest.fixture
def load_plugin(testdir):
    testdir.makeconftest(
        """
        from tests import transformer

        def pytest_register_ast_transformer(ast_manager):
            ast_manager.add_transformer(transformer.AssertTransformer())
        """
    )
