import dataclasses
from typing import Generic, TypeVar
from typing import List

T = TypeVar('T')


@dataclasses.dataclass
class PageResult(Generic[T]):
    results: List[T]
    total_count: int
