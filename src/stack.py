from __future__ import annotations
from typing import Optional, TypeVar

T = TypeVar("T")


class Stack[T]:
    def __init__(self, e: T, next: Optional[Stack[T]] = None):
        self.e = e
        self.next = next

    def push(self, e: T):
        return Stack(e, next=self)

    def pop(self):
        return self.e, self.next
