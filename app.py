#!/usr/bin/env python3

import os
import argparse

from workouts import WorkoutReader, WorkoutWriter, WorkoutInverter

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file(CSV)")
parser.add_argument("output", help="Output file")
args = parser.parse_args()

input_file = os.path.abspath(args.input)
output_file = os.path.abspath(args.output)

reader = WorkoutReader(file_name=input_file)
inverter = WorkoutInverter()
writer = WorkoutWriter(reader=reader, inverter=inverter)

data = reader.read()

writer.write(file_name=output_file)
