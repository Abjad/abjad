# -*- coding: utf-8 -*-
#! /usr/bin/env python

if __name__ == '__main__':
    import sys
    from abjad import Duration
    from abjad import show
    from abjad.demos.ferneyhough import make_lilypond_file

    arguments = sys.argv[1:]
    if len(arguments) != 3:
        print('USAGE: [tuplet_duration, row_count, column_count]:')
        print('\ti.e.: /main.py 1/4 11 6')
        sys.exit(0)

    tuplet_duration = Duration(arguments[0])
    row_count = int(arguments[1])
    column_count = int(arguments[2])

    assert 0 < tuplet_duration
    assert 0 < row_count
    assert 0 < column_count

    lilypond_file = make_lilypond_file(tuplet_duration, row_count, column_count)
    show(lilypond_file)
