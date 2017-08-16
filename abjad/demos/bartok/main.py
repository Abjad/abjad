#! /usr/bin/env python
import abjad


if __name__ == '__main__':
    lilypond_file = abjad.demos.bartok.make_bartok_score()
    abjad.show(lilypond_file)
