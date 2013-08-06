# -*- encoding: utf-8 -*-
from abjad import *


def test_NaturalHarmonic_01():

    t = notetools.NaturalHarmonic(10, (1, 4))

    r'''
    \once \override NoteHead #'style = #'harmonic
    bf'4
    '''

    assert t.written_pitch == pitchtools.NamedChromaticPitch(10)
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \once \override NoteHead #'style = #'harmonic
        bf'4
        '''
        )
