import abjad
from abjad.demos import ligeti


def test_demos_desordre_01():

    pitches = ligeti.make_desordre_pitches()
    score = ligeti.make_desordre_score(pitches)
    lilypond_file = ligeti.make_desordre_lilypond_file(score)
