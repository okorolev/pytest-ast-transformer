import typing

from pytest_ast_transformer.transformer import PytestTransformer


class ASTManager:
    transformers: typing.List[PytestTransformer]

    def __init__(self, transformers=None):
        self.transformers = transformers or []

    def __repr__(self):
        return f'ASTManager <{self.transformers}>'

    @property
    def is_empty(self) -> bool:
        return not bool(self.transformers)

    def add_transformer(self, transformer):
        self.transformers.append(transformer)
