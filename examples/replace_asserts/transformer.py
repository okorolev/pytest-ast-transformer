import ast

from pytest_ast_transformer.transformer import PytestTransformer


def my_assert(test_result, msg):
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
