import typing

import pytest

from pytest_ast_transformer import newhooks
from pytest_ast_transformer.ast_manager import ASTManager
from pytest_ast_transformer.transformer.utils import delete_tmp_files
from pytest_ast_transformer.transformer.wrapper import PytestFunctionProxy

if typing.TYPE_CHECKING:
    from _pytest.config import Config, PytestPluginManager
    from _pytest.runner import CallInfo


def pytest_collection_modifyitems(config: 'Config', items: typing.List[pytest.Function]):
    manager: ASTManager = config.ast_manager
    transformers = manager.transformers

    allow_show_code = config.option.show_code
    disable_transforms = config.option.disable_transforms

    if not manager or manager.is_empty:
        return

    if disable_transforms:
        return

    proxy_items = set(map(PytestFunctionProxy, items))

    for item in proxy_items:
        for transformer in transformers:
            transformer.rewrite_ast(item, show_code=allow_show_code)


def pytest_configure(config: 'Config'):
    ast_manager = ASTManager()

    config.ast_manager = ast_manager
    config.hook.pytest_register_ast_transformer(ast_manager=ast_manager, config=config)


def pytest_addhooks(pluginmanager: 'PytestPluginManager'):
    pluginmanager.add_hookspecs(newhooks)


def pytest_addoption(parser: 'Parser'):
    parser.addoption("--show-code", action="store_true", dest="show_code", default=False)
    parser.addoption("--disable-transforms", action="store_true", dest="disable_transforms", default=False)


def pytest_runtest_makereport(item: pytest.Function, call: 'CallInfo'):
    if call.when == 'teardown':
        tmp_files = getattr(item.module, 'transformer_tmp_files', None)

        if tmp_files is not None:
            # NOTE: only for 2+ transformers
            delete_tmp_files(tmp_files)
