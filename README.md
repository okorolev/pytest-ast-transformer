About
-----
AST Transformer integrated with py.test.

Useful for debug, refactoring, 'clean asserts' (see [examples/replace_asserts](examples/replace_asserts))

Usage
-----
* write ast transformer
```python
# transformer.py
import ast

from pytest_ast_transformer.ast_transformer import PytestTransformer


def my_assert(test_result, msg=''):
    print(f'my assert: {test_result} {msg}')
    assert test_result, msg


class AssertTransformer(PytestTransformer):
    context = {
        'my_assert': my_assert
    }

    def visit_Assert(self, node: ast.Assert) -> ast.Expr:
        func_name = ast.Name(id='my_assert', ctx=ast.Load())
        call_func = ast.Call(func=func_name, args=[node.test, node.msg], keywords=[])
        expr = ast.Expr(value=call_func)

        return ast.fix_missing_locations(expr)
```
* register new ast transformer
```python
# conftest.py
from tests.transformer import AssertTransformer


def pytest_register_ast_transformer(ast_manager):
    ast_manager.add_transformer(AssertTransformer())
```
