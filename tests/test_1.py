import pytest


class TestTransformer:

    @pytest.mark.parametrize('kek', [1, 2])
    def test_with_parametrize(self, kek):
        assert kek == 1, f"hey {kek} is not 1"

    def test_single(self, kek=4):
        a = 1
        assert kek == 1, f"hey {kek} is not 1"


@pytest.mark.h1
class TestSimple:

    def test_simple(self):
        assert 1 == 2, '1 is not 2'


def test_without_cls():
    assert 1 == 2, 'lol'
