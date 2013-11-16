# -*- encoding: utf-8 -*-
from abjad import *


def test_indicatortools_LilyPondComment_right_01():
    r'''Context comments right.
    Container slots interfaces do not collect contributions to right.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    override(beam).beam.thickness = 3
    comment = indicatortools.LilyPondComment('Voice right comments here.', 'right')
    attach(comment, voice)
    comment = indicatortools.LilyPondComment('More voice right comments.', 'right')
    attach(comment, voice)


    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            \override Beam #'thickness = #3
            c'8 [
            d'8
            e'8
            f'8 ]
            \revert Beam #'thickness
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_indicatortools_LilyPondComment_right_02():
    r'''Leaf comments right.
    '''

    note = Note(0, (1, 8))
    override(note).beam.thickness = 3
    comment = indicatortools.LilyPondComment('Leaf comments right here.', 'right')
    attach(comment, note)
    comment = indicatortools.LilyPondComment('More comments right.', 'right')
    attach(comment, note)

    assert systemtools.TestManager.compare(
        note,
        r'''
        \once \override Beam #'thickness = #3
        c'8 % Leaf comments right here. % More comments right.
        '''
        )

    assert inspect(note).is_well_formed()
