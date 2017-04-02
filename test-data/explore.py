#!/usr/bin/env python
import re

found = set([])

with open('raw_data', 'r') as f:
    for i, line in enumerate(f):
        m = re.search('(HTTP/.{10})', line)
        if (m):
            f = m.group(0)
            found.add(f)
print found
