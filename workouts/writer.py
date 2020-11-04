import csv
import json

from datetime import datetime

from .inverter import WorkoutInverter
from .reader import WorkoutReader


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(JSONEncoder, self).default(obj)


class WorkoutWriter:
    def __init__(self, reader: WorkoutReader, inverter: WorkoutInverter) -> None:
        self.reader = reader
        self.inverter = inverter
        self.data = self.reader.read()

    def write(self, file_name: str) -> None:
        with open(file_name, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)

            writer.writerow([""] * 11)
            for workout in self.data:
                workout_date = workout.date.strftime("%Y-%m-%d")
                writer.writerow([workout_date] + [""] + [str(workout.weight) if workout.weight else ""] + [""] * 8)
                for exercise in workout.exercises:
                    writer.writerow([""] + [exercise.name] + exercise.repeats)

                writer.writerow([""] * 11)

    def write_inverted(self, file_name: str) -> None:
        data = self.inverter.inverted_exercises(self.data)

        dates = [""] + [d.date.strftime("%Y.%m.%d") for d in self.data]

        with open(file_name, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL)

            writer.writerow(dates)
            for d in data:
                writer.writerow(d)
