# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondComment_before_01():
    r'''Test context comments before.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(t[:])
    beam.override.beam.thickness = 3
    marktools.LilyPondComment('Voice before comments here.', 'before')(t)
    marktools.LilyPondComment('More voice before comments.', 'before')(t)

    r'''
    % Voice before comments here.
    % More voice before comments.
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
        % Voice before comments here.
        % More voice before comments.
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


def test_LilyPondComment_before_02():
    r'''Leaf comments before.
    '''

    t = Note(0, (1, 8))
    t.override.beam.thickness = 3
    marktools.LilyPondComment('Leaf comments before here.', 'before')(t)
    marktools.LilyPondComment('More comments before.', 'before')(t)

    r'''
    % Leaf comments before here.
    % More comments before.
    \once \override Beam #'thickness = #3
    c'8'''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        % Leaf comments before here.
        % More comments before.
        \once \override Beam #'thickness = #3
        c'8
        '''
        )
