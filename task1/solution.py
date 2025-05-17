from __future__ import annotations

import asyncio
import functools
import inspect
from typing import Any, Awaitable, Callable, get_type_hints


def strict(
    function: Callable[..., Awaitable[Any] | Any],
) -> Callable[..., Awaitable[Any] | Any]:
    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        type_hints = get_type_hints(function)
        signature = inspect.signature(function)
        for name, value in signature.bind(*args, **kwargs).arguments.items():
            if name not in type_hints:
                continue

            parameter = signature.parameters[name]
            match parameter.kind:
                case parameter.VAR_POSITIONAL:
                    if not all(
                        isinstance(to_check, type_hints[name]) for to_check in value
                    ):
                        raise TypeError
                case parameter.VAR_KEYWORD:
                    if not all(
                        isinstance(to_check, type_hints[name])
                        for to_check in value.values()
                    ):
                        raise TypeError
                case _:
                    if not isinstance(value, type_hints[name]):
                        raise TypeError

        if asyncio.iscoroutinefunction(function):

            async def async_wrapped() -> Any:
                async_return_value = await function(*args, **kwargs)
                if (
                    async_return_type_hint := type_hints.get("return")
                ) is not None and not isinstance(
                    async_return_value, async_return_type_hint
                ):
                    raise TypeError
                return async_return_value

            return async_wrapped()
        else:
            return_value = function(*args, **kwargs)
            if (
                return_type_hint := type_hints.get("return")
            ) is not None and not isinstance(return_value, return_type_hint):
                raise TypeError
            return return_value

    return wrapper
