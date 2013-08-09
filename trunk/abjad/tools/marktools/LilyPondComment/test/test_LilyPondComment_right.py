# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondComment_right_01():
    r'''Context comments right.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(voice[:])
    beam.override.beam.thickness = 3
    marktools.LilyPondComment('Voice right comments here.', 'right')(voice)
    marktools.LilyPondComment('More voice right comments.', 'right')(voice)

    "Container slots interfaces do not collect contributions to right."

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

    assert select(voice).is_well_formed()
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


def test_LilyPondComment_right_02():
    r'''Leaf comments right.
    '''

    note = Note(0, (1, 8))
    note.override.beam.thickness = 3
    marktools.LilyPondComment('Leaf comments right here.', 'right')(note)
    marktools.LilyPondComment('More comments right.', 'right')(note)

    r'''
    \once \override Beam #'thickness = #3
    c'8 % Leaf comments right here. % More comments right.
    '''

    assert select(note).is_well_formed()
    assert testtools.compare(
        note,
        r'''
        \once \override Beam #'thickness = #3
        c'8 % Leaf comments right here. % More comments right.
        '''
        )
