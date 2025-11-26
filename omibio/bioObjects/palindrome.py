from dataclasses import dataclass


@dataclass
class Palindrome:
    start: int
    end: int
    length: int
    seq: str
