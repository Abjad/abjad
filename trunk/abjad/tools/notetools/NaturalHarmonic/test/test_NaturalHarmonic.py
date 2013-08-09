# -*- encoding: utf-8 -*-
from abjad import *


def test_NaturalHarmonic_01():

    naturalharmonic = notetools.NaturalHarmonic(10, (1, 4))

    r'''
    \once \override NoteHead #'style = #'harmonic
    bf'4
    '''

    assert naturalharmonic.written_pitch == pitchtools.NamedChromaticPitch(10)
    assert testtools.compare(
        naturalharmonic,
        r'''
        \once \override NoteHead #'style = #'harmonic
        bf'4
        '''
        )
