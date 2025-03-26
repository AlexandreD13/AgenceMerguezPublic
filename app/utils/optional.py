from typing import Optional, Callable, TypeVar

A = TypeVar('A')
B = TypeVar('B')


def map(a: Optional[A], thunk: Callable[[A], B]) -> Optional[B]:
    """
    Allows to map an optional value if defined
    """
    if a is None:
        return None
    return thunk(a)
