# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_LilyPondComment_right_01():
    r'''Context comments right.
    Container slots interfaces do not collect contributions to right.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    override(beam).beam.thickness = 3
    string = 'Voice right comments here.'
    comment = indicatortools.LilyPondComment(string, 'right')
    attach(comment, voice)
    string = 'More voice right comments.'
    comment = indicatortools.LilyPondComment(string, 'right')
    attach(comment, voice)


    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \override Beam.thickness = #3
            c'8 [
            d'8
            e'8
            f'8 ]
            \revert Beam.thickness
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_indicatortools_LilyPondComment_right_02():
    r'''Leaf comments right.
    '''

    note = Note(0, (1, 8))
    override(note).beam.thickness = 3
    string = 'Leaf comments right here.'
    comment = indicatortools.LilyPondComment(string, 'right')
    attach(comment, note)
    string = 'More comments right.'
    comment = indicatortools.LilyPondComment(string, 'right')
    attach(comment, note)

    assert format(note) == stringtools.normalize(
        r'''
        \once \override Beam.thickness = #3
        c'8 % Leaf comments right here. % More comments right.
        '''
        )

    assert inspect_(note).is_well_formed()
