import pytest

from pytest_cleanup.common import assert_return_values


def test_pytest_cleanup_sync_test_cases(fn, args, kwargs, expected):
    """See ./test-data directory for test cases"""
    actual = fn(*args, **kwargs)
    assert_return_values(actual, expected)


@pytest.mark.asyncio
async def test_pytest_cleanup_async_test_cases(fn, args, kwargs, expected):
    """See ./test-data directory for test cases.
    support for asyncio in pytest may be enabled by installing pytest-asyncio """
    actual = await fn(*args, **kwargs)
    assert_return_values(actual, expected)
