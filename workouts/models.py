from datetime import datetime
from typing import NamedTuple, List, Optional


class Exercise(NamedTuple):
    name: str
    repeats: List[str]


class Workout(NamedTuple):
    date: datetime
    weight: Optional[float]
    exercises: List[Exercise] = []
