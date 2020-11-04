import itertools

from collections import defaultdict
from typing import List

from .models import Workout


class WorkoutInverter(object):
    def inverted_exercises(self, data: List[Workout]):
        hash = defaultdict(lambda: [None] * len(data))

        for index, workout in enumerate(data):
            date, weight, exercises = workout

            for exercise in exercises:
                arr = [None] * len(data)

                if len(exercise.repeats) > 0:
                    repeats = exercise.repeats
                    repeats = [e for e in repeats if len(e) > 0]
                    repeats = repeats if repeats else ["V"]

                    hash[exercise.name][index] = repeats

        result = []

        for key in sorted(hash.keys()):
            result.append([key] + hash[key])

        return result
