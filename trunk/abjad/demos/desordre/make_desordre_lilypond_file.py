from abjad import *
from abjad.tools import documentationtools
from abjad.demos.desordre.make_desordre_pitches import make_desordre_pitches
from abjad.demos.desordre.make_desordre_score import make_desordre_score


def make_desordre_lilypond_file():

    pitches = make_desordre_pitches()

    score = make_desordre_score(pitches)

    lilypond_file = documentationtools.make_ligeti_example_lilypond_file(score)

    return lilypond_file
