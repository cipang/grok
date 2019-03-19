#!/usr/local/bin/python3
#
# A script to process all SQL files of Grok submissions, grouped by questions and users.
# Output as submission.sql and submission_marks.csv.
# Copyright (C) 2018-2019 Patrick Pang <pat.pang@unimelb.edu.au>
#
import csv
import os.path
import sys
from collections import defaultdict


LATE_POINTS = 0        # Late points for each question.
FULL_POINTS = 1        # Full points for each question.


script_name = os.path.basename(sys.argv[0])
if len(sys.argv) < 2:
    print(f"{script_name}: Please specify the path to the submission directory.")
    sys.exit(1)

sub_path = sys.argv[1]
non_anonymised_path = os.path.join(sub_path, "non-anonymised")
pass_tested_cases_path = os.path.join(sub_path, "passed-test-cases.csv")
submission_output = os.path.join(sub_path, "submission.sql")
marks_output = os.path.join(sub_path, "submission_marks.csv")
if not os.path.exists(non_anonymised_path):
    print(f"{script_name}: Cannot locate directory {non_anonymised_path}.")
    sys.exit(2)
if not os.path.exists(pass_tested_cases_path):
    print(f"{script_name}: Cannot locate file {pass_tested_cases_path}.")
    sys.exit(2)
if os.path.exists(submission_output) or os.path.exists(marks_output):
    print(f"{script_name}: Output already exists. Delete them first.")
    sys.exit(2)


# Output SQL.
data = defaultdict(dict)
for root, dirs, files in os.walk(non_anonymised_path):
    for fn in files:
        full_name = os.path.join(root, fn)
        if full_name.endswith(".sql"):
            components = full_name.split(os.sep)
            username = "{0}@student.unimelb.edu.au".format(components[-5].lower())
            qid = str(components[-4])
            with open(full_name, "r") as file_object:
                data[qid][username] = file_object.read()

with open(submission_output, mode="w") as fp:
    for qid in sorted(data.keys()):
        usernames = data[qid].keys()
        print("-- ******************************", file=fp)
        print("-- ******************************", file=fp)
        print(f"-- Problem: {qid}", file=fp)
        print(f"--   {len(usernames)} submissions.", file=fp)
        print("-- ******************************\n", file=fp)
        for username in sorted(usernames):
            print("---------------------------------", file=fp)
            print(f"-- Submission: {qid} / {username}", file=fp)
            print("---------------------------------", file=fp)
            print(data[qid][username], file=fp)
            print(file=fp)
    print("-- *** END OF OUTOUT ***", file=fp)


# Output marks.
data = {}
with open(pass_tested_cases_path, "r") as fp:
    reader = csv.reader(fp)
    next(reader)  # Skip the header row.
    for row in reader:
        username = "{0}@student.unimelb.edu.au".format(row[0].lower())
        marks = []
        col = 2
        while col < len(row):
            is_late = row[col + 1] == "TRUE"  # was late? column
            is_done = row[col + 3] == "1"     # output column
            if is_done == 0:
                marks.append(0)
            elif is_late != 0:
                marks.append(LATE_POINTS)
            else:
                marks.append(FULL_POINTS)
            col += 4    # column offset for each question
        data[username] = marks

with open(marks_output, "w") as fp:
    writer = csv.writer(fp)
    for username in sorted(data.keys()):
        writer.writerow([username] + data[username])
