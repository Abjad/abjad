# -*- coding: utf-8 -*-
#! /usr/bin/env python


if __name__ == '__main__':
    import aabjad
    import sys

    arguments = sys.argv[1:]
    if len(arguments) != 3:
        print('USAGE: [tuplet_duration, row_count, column_count]:')
        print('\ti.e.: /main.py 1/4 11 6')
        sys.exit(0)

    tuplet_duration = abjad.Duration(arguments[0])
    row_count = int(arguments[1])
    column_count = int(arguments[2])

    assert 0 < tuplet_duration
    assert 0 < row_count
    assert 0 < column_count

    lilypond_file = abjad.demos.ferneyhough.make_lilypond_file(
        tuplet_duration,
        row_count,
        column_count,
        )
    abjad.show(lilypond_file)
