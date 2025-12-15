from collections.abc import Iterable
from pathlib import Path
from typing import TypeVar, overload, Iterable as TypingIterable

T = TypeVar("T")


@overload
def ensure_iterable(x: None) -> list[None]: ...


@overload
def ensure_iterable(x: TypingIterable[T]) -> list[T]: ...


@overload
def ensure_iterable(x: T) -> list[T]: ...


def ensure_iterable(x):
    if x is None:
        return []
    if isinstance(x, (str, bytes, Path, dict)):
        return [x]
    if isinstance(x, Iterable):
        return list(x)
    return [x]


def main():
    x = {"test": 1}
    res = ensure_iterable(x)
    print(res)
    print(type(res))


if __name__ == "__main__":
    main()
