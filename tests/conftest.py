import pytest

from pytest_mock import MockFixture
from pytest_ast_transformer.ast_manager import ASTManager
from tests.transformer import AssertTransformer

pytest_plugins = ["pytester"]


@pytest.fixture
def mocker(pytestconfig):
    result = MockFixture(pytestconfig)
    yield result
    result.stopall()


def pytest_register_ast_transformer(ast_manager: ASTManager):
    pass
    # ast_manager.add_transformer(AssertTransformer())
