# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondComment_closing_01():
    r'''Test container comments closing.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    marktools.LilyPondComment('Voice closing comments here.', 'closing')(t)
    marktools.LilyPondComment('More voice closing comments.', 'closing')(t)

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
        % Voice closing comments here.
        % More voice closing comments.
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
            % Voice closing comments here.
            % More voice closing comments.
        }
        '''
        )


def test_LilyPondComment_closing_02():
    r'''Test leaf comments closing.
    '''

    t = Note(0, (1, 8))
    t.override.beam.thickness = 3
    marktools.LilyPondComment('Leaf closing comments here.', 'closing')(t)
    marktools.LilyPondComment('More leaf closing comments.', 'closing')(t)

    r'''
    \once \override Beam #'thickness = #3
    c'8
    % Leaf closing comments here.
    % More leaf closing comments.
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \once \override Beam #'thickness = #3
        c'8
        % Leaf closing comments here.
        % More leaf closing comments.
        '''
        )
