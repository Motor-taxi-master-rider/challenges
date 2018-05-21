"""
Turn the following unix pipeline into Python code using generators

$ for i in ../*/*py; do grep ^import $i|sed 's/import //g' ; done | sort | uniq -c | sort -nr
   4 unittest
   4 sys
   3 re
   3 csv
   2 tweepy
   2 random
   2 os
   2 json
   2 itertools
   1 time
   1 datetime
"""
import collections
import glob
import itertools
import re


def gen_files(pat):
    yield from glob.glob(pat)


def gen_lines(files):
    for file in files:
        with open(file, encoding='utf-8') as fh:
            yield from (line[:-1] for line in fh.readlines() if line.strip())


def gen_grep(lines, pattern):
    pattern_ = re.compile(pattern)
    match_result = (pattern_.match(line) for line in lines)
    yield from itertools.chain.from_iterable(result.groups() for result in match_result if result)


def gen_count(lines):
    yield from collections.Counter(lines).most_common()


if __name__ == "__main__":
    # call the generators, passing one to the other
    files = gen_files('../*/*.py')
    lines = gen_lines(files)
    modules = gen_grep(lines, r'^import (\w+)')
    counts = gen_count(modules)

    print('Most imported:')
    for module, count in counts:
        print(f'{count}  {module}')
