#! /usr/bin/env python
import abjad


if __name__ == '__main__':
    lilypond_file = abjad.demos.mozart.make_mozart_lilypond_file()
    abjad.show(lilypond_file)
