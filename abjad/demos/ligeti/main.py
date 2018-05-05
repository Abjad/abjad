#! /usr/bin/env python
import abjad


if __name__ == '__main__':
    pitches = abjad.demos.ligeti.make_desordre_pitches()
    score = abjad.demos.ligeti.make_desordre_score(pitches)
    lilypond_file = abjad.demos.ligeti.make_desordre_lilypond_file(score)
    abjad.show(lilypond_file)
