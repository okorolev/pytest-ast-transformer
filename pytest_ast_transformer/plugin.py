import typing

import pytest

from pytest_ast_transformer import newhooks
from pytest_ast_transformer.ast_manager import ASTManager

if typing.TYPE_CHECKING:
    from _pytest.config import Config, PytestPluginManager


def pytest_collection_modifyitems(config: 'Config', items: typing.List[pytest.Function]):
    manager: ASTManager = config.ast_manager

    if manager.is_empty:
        return

    for func in items:
        for transformer in manager.transformers:
            transformer.rewrite_ast(func)


def pytest_configure(config: 'Config'):
    ast_manager = ASTManager()

    config.ast_manager = ast_manager
    config.hook.pytest_register_ast_transformer(ast_manager=ast_manager)


def pytest_addhooks(pluginmanager: 'PytestPluginManager'):
    pluginmanager.add_hookspecs(newhooks)
