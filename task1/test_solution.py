from __future__ import annotations

import pytest

from solution import strict


@strict
def func_no_annotations_returning_3(a, b):
    return 3


def test_func_no_annotations_do_nothing() -> None:
    assert func_no_annotations_returning_3(1, 1) == 3
    assert func_no_annotations_returning_3(True, 2.2) == 3


@strict
def func_no_parameters_annotations_returning_wrong_type() -> int:
    return 1.1  # noqa


def test_func_no_parameters_annotations_returning_wrong_type() -> None:
    with pytest.raises(TypeError):
        func_no_parameters_annotations_returning_wrong_type()


@strict
def function(a: int, b: int) -> int:
    return a + b


def test_function_invalid_with_invalid_parameters() -> None:
    with pytest.raises(TypeError):
        function(1, 1.1)
    with pytest.raises(TypeError):
        function(1.1, 1)


def test_function_with_valid_parameters() -> None:
    assert function(1, 1) == 2


def test_function_with_valid_parameters_with_keyword() -> None:
    assert function(1, b=1) == 2


@strict
def function_all_positional(*args: int) -> int:
    return sum(args)


def test_function_all_positional_with_invalid_parameters() -> None:
    with pytest.raises(TypeError):
        function_all_positional(1, 1, 1.1)


def test_function_all_positional_with_valid_parameters() -> None:
    assert function_all_positional(1, 1, 1) == 3


@strict
def function_strange(a: int, /, b, *, c: int) -> int:
    return a + b + c


def test_function_strange_with_invalid_parameters() -> None:
    with pytest.raises(TypeError):
        function_strange(1, 1, c=1.1)
    with pytest.raises(TypeError):
        function_strange(1, 1.1, c=1)


def test_function_strange_with_valid_parameters() -> None:
    assert function_strange(1, 1, c=1) == 3
    assert function_strange(1, b=1, c=1) == 3


class Some:
    def __init__(self, b: int) -> None:
        self.b = b


@strict
def function_with_user_type(a: Some) -> int:
    return a.b


def test_function_with_user_type_with_invalid_parameters() -> None:
    with pytest.raises(TypeError):
        function_with_user_type(1)
    with pytest.raises(TypeError):
        function_with_user_type(Some(b=1.1))  # noqa


def test_function_with_user_type_with_valid_parameters() -> None:
    assert function_with_user_type(Some(b=1)) == 1


@strict
async def async_function(a: int, b: int) -> int:
    return a + b


@pytest.mark.asyncio
async def test_async_function_with_invalid_parameters() -> None:
    with pytest.raises(TypeError):
        await async_function(1, 1.1)


@pytest.mark.asyncio
async def test_async_function_with_valid_parameters() -> None:
    assert await async_function(1, 1) == 2
