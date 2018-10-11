def pytest_register_ast_transformer(ast_manager):
    """ Register new ast transformers via `ast_manager.add_transformer`.

        Example:
            ast_manager.add_transformer(AssertTransformer())
    """
