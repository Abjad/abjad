# -*- coding: utf-8 -*-
import abjad
from abjad.tools import documentationtools


def make_desordre_lilypond_file():
    '''Makes Désordre LilyPond file.
    '''

    pitches = abjad.demos.desordre.make_desordre_pitches()
    score = abjad.demos.desordre.make_desordre_score(pitches)
    lilypond_file = documentationtools.make_ligeti_example_lilypond_file(score)
    return lilypond_file
