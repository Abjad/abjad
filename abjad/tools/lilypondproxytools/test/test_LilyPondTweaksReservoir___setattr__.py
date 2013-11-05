from abjad import *


def test_LilyPondTweaksReservoir___setattr___01():
    '''Tweak chord note head.
    '''

    chord = Chord("<d' ef' e'>4")
    chord.note_heads[0].tweak.transparent = True

    assert testtools.compare(
        chord,
        r'''
        <
            \tweak #'transparent ##t
            d'
            ef'
            e'
        >4
        '''
        )


def test_LilyPondTweaksReservoir___setattr___02():
    r'''Tweak chord note head.
    '''

    chord = Chord("<d' ef' e'>4")
    chord.note_heads[0].tweak.style = 'harmonic'

    assert testtools.compare(
        chord,
        r'''
        <
            \tweak #'style #'harmonic
            d'
            ef'
            e'
        >4
        '''
        )
