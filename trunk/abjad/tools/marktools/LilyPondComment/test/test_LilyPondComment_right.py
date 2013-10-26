# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondComment_right_01():
    r'''Context comments right.
    Container slots interfaces do not collect contributions to right.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])
    beam.override.beam.thickness = 3
    comment = marktools.LilyPondComment('Voice right comments here.', 'right')
    comment.attach(voice)
    comment = marktools.LilyPondComment('More voice right comments.', 'right')
    comment.attach(voice)


    assert testtools.compare(
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


def test_LilyPondComment_right_02():
    r'''Leaf comments right.
    '''

    note = Note(0, (1, 8))
    note.override.beam.thickness = 3
    comment = marktools.LilyPondComment('Leaf comments right here.', 'right')
    comment.attach(note)
    comment = marktools.LilyPondComment('More comments right.', 'right')
    comment.attach(note)

    assert testtools.compare(
        note,
        r'''
        \once \override Beam #'thickness = #3
        c'8 % Leaf comments right here. % More comments right.
        '''
        )

    assert inspect(note).is_well_formed()
