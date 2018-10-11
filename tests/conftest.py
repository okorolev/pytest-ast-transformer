import pytest

from pytest_mock import MockFixture

pytest_plugins = ["pytester"]


@pytest.fixture
def mocker(pytestconfig):
    result = MockFixture(pytestconfig)
    yield result
    result.stopall()
