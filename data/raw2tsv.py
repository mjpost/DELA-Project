#!/usr/bin/env python3

import sys
from zlib import crc32
from csv import DictReader
from collections import defaultdict

docid = None
seen = defaultdict(int)
sentid = 0
for row in DictReader(sys.stdin, delimiter=","):
    if "<doc" in row["ID"]:
        text = row["text"].rstrip()

        # some document URLs are identical (probably an error)
        if text in seen:
            text += f" {seen[text]}"
        docid = crc32(text.encode()) & 0xFFFFFFFF

        seen[text] += 1
        sentid = 0

    elif "<seg" in row["ID"]:
        sentid += 1
        text = row["text"].strip()

        issues = row["issue"]
        expls = row["explanation"]

        for (issue, expl) in zip(issues.split(), expls.split()):
            if issue == "X":
                issue = ""
                expl = ""
            print(docid, sentid, issue, expl, text, sep="\t")
