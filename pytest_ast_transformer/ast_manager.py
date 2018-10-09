import typing

from pytest_ast_transformer.ast_transformer import PytestTransformer


class ASTManager:
    transformers: typing.Set[PytestTransformer]

    def __init__(self, transformers=None):
        self.transformers = transformers or set()

    def __repr__(self):
        return f'ASTManager <{self.transformers}>'

    @property
    def is_empty(self) -> bool:
        return not bool(self.transformers)

    def add_transformer(self, transformer):
        self.transformers.add(transformer)
