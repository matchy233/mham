# -f input path to the trace file, can be relative or absolute

import os
import sys

sys.path.append('..')

import argparse
from Lilygo.Recording import Recording
from Lilygo.Dataset import Dataset

parser = argparse.ArgumentParser(description='Postprocess a trace file')
parser.add_argument('-f', '--file', help='Path to the trace file', required=True)
args = parser.parse_args()

# print the file name
print("Processing File: " + args.file.split("/")[-1])

# Get the absolute path to the trace file
trace_file = os.path.abspath(args.file)

# Create a recording object
recording = Recording(trace_file, no_labels=False)

recording.DataIntegrityCheck()
# and then it will be automatically loaded and processed
