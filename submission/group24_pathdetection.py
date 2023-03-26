# This is the template for the submission. If you want, you can develop your
# algorithm in a Jupyter Notebook and copy the code here for submission.
# Don't forget to test according to specification below

# Team members (e-mail, legi):
# chozhang@ethz.ch, 22-945-562
# minghli@student.ethz.ch, 22-953-293
# changli@student.ethz.ch, 22-944-474

import sys
from Lilygo.Recording import Recording
from Lilygo.Dataset import Dataset

filename = sys.argv[1]  # e.g. 'data/someDataTrace.json'
# IMPORTANT: To allow grading, the two arguments no_labels and mute must be set
#  True in the constructor when loading the data
trace = Recording(filename, no_labels=True, mute=True)
boardLocation = 0  # <- here goes your detected board location
pathIdx = 0  # <- here goes your detected path index
stepCount = 0  # <- here goes your detected stepcount
activities = []  # <- here goes a list of your detected activities, order does not matter


#
# Your algorithm goes here
# Make sure, you do not use the gps data and are tolerant for missing data
# (see task set). Your program must not crash when single smartphone data traces
# are missing.
#


# Print result, do not change!
print(boardLocation)
print(pathIdx)
print(stepCount)
print(activities)


# Test this file before submission with the data we provide to you

# 1. In the console or Anaconda Prompt execute:
# python --version

# Output should look something like (displaying your python version, which must be 3.8.x):
# Python 3.8.10
# If not, check your python installation or command

# 2. In the console execute:
# python [thisfilename.py] path/to/datafile.json

# Output should be 4 integers on seperate lines. Nothing else.
