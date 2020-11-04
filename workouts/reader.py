import csv
from datetime import datetime

from typing import List, Tuple, Optional

from .models import Workout, Exercise

WorkoutHeadType = Tuple[datetime, Optional[float]]
WorkoutExerciseType = Tuple[str, List[str]]


class WorkoutReader(object):
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def _parse_date(self, row: List[str]) -> Optional[datetime]:
        try:
            return datetime.strptime(row[0], "%Y-%m-%d")
        except ValueError:
            pass

    def _parse_weight(self, row: List[str]) -> Optional[float]:
        try:
            return float(row[2])
        except ValueError:
            pass

    def _parse_head(self, row: List[str]) -> Optional[WorkoutHeadType]:
        workout_date = self._parse_date(row)
        if workout_date:
            return (workout_date, self._parse_weight(row))

        pass

    def _parse_exercise(self, row: List[str]) -> Optional[WorkoutExerciseType]:
        try:
            name = row[1].strip()
            repeats = [e.strip() for e in row[2:]]

            return (name, repeats)
        except (ValueError, IndexError):
            pass

    def _is_empty_row(self, row: List[str]) -> bool:
        return len("".join(row)) == 0

    def read(self) -> List[Workout]:
        workouts: List[Workout] = []

        with open(self.file_name, "r+") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")

            last_workout: Optional[Workout] = None

            for row in reader:
                if self._is_empty_row(row):
                    continue

                head = self._parse_head(row)
                if head:
                    workout_date, workout_weight = head

                    if last_workout and last_workout.date != workout_date:
                        workouts.append(last_workout)

                    last_workout = Workout(date=workout_date, weight=workout_weight, exercises=[])
                    continue

                exercise = self._parse_exercise(row)
                if exercise:
                    name, repeats = exercise
                    last_workout.exercises.append(Exercise(name=name, repeats=repeats))
            else:
                if last_workout:
                    workouts.append(last_workout)

        return workouts
