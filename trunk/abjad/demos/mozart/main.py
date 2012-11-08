#! /usr/bin/env python

if __name__ == '__main__':

    from abjad import *
    from abjad.demos import mozart

    lilypond_file = mozart.make_mozart_lilypond_file()
    show(lilypond_file)
