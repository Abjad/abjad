#! /usr/bin/env python

"""
If no pickled parser tables have been created, e.g. because Abjad has just
been downloaded and installed for the first time, PLY will print an error
message along the lines of "WARNING: yacc table file version is out of date.".
This can cause doctests to fail should the warning appear during the middle of
those tests.

This script simply finds each Parser subclass in Abjad and instantiates it,
thereby causing PLY to create and persist the appropriate parser tables.
"""

import abjad
from abjad.parsers.parser import LilyPondParser
from abjad.parsers.reduced import ReducedLyParser
from abjad.parsers.scheme import SchemeParser

print("AAA!")
parsers = (
    LilyPondParser,
    SchemeParser,
    abjad.rhythmtrees.RhythmTreeParser,
    ReducedLyParser,
)

print("FOO!")
for parser in parsers:
    print(f"Priming {parser.__name__} parser tables.")
    parser()
print("BAR!")
