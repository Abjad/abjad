# -*- coding: utf-8 -*-
#! /usr/bin/env python
import abjad
import sys


if __name__ == '__main__':

    arguments = sys.argv[1:]
    if len(arguments) != 3:
        print('USAGE: tuplet_duration row_count column_count')
        print(' e.g.: python main.py 1/4 11 6')
        sys.exit(0)

    tuplet_duration = abjad.Duration(arguments[0])
    row_count = int(arguments[1])
    column_count = int(arguments[2])

    assert 0 < tuplet_duration
    assert 0 < row_count
    assert 0 < column_count

    demo = abjad.demos.ferneyhough.FerneyhoughDemo()
    lilypond_file = demo(
        tuplet_duration=tuplet_duration,
        row_count=row_count,
        column_count=column_count,
        )
    abjad.show(lilypond_file)
