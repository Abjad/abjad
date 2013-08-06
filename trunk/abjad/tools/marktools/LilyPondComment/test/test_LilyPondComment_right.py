# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondComment_right_01():
    r'''Context comments right.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(t[:])
    beam.override.beam.thickness = 3
    marktools.LilyPondComment('Voice right comments here.', 'right')(t)
    marktools.LilyPondComment('More voice right comments.', 'right')(t)

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

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
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

    t = Note(0, (1, 8))
    t.override.beam.thickness = 3
    marktools.LilyPondComment('Leaf comments right here.', 'right')(t)
    marktools.LilyPondComment('More comments right.', 'right')(t)

    r'''
    \once \override Beam #'thickness = #3
    c'8 % Leaf comments right here. % More comments right.
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \once \override Beam #'thickness = #3
        c'8 % Leaf comments right here. % More comments right.
        '''
        )
