# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondComment_closing_01():
    r'''Test container comments closing.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    marktools.LilyPondComment('Voice closing comments here.', 'closing')(voice)
    marktools.LilyPondComment('More voice closing comments.', 'closing')(voice)

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

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
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

    note = Note(0, (1, 8))
    note.override.beam.thickness = 3
    marktools.LilyPondComment('Leaf closing comments here.', 'closing')(note)
    marktools.LilyPondComment('More leaf closing comments.', 'closing')(note)

    r'''
    \once \override Beam #'thickness = #3
    c'8
    % Leaf closing comments here.
    % More leaf closing comments.
    '''

    assert inspect(note).is_well_formed()
    assert testtools.compare(
        note,
        r'''
        \once \override Beam #'thickness = #3
        c'8
        % Leaf closing comments here.
        % More leaf closing comments.
        '''
        )
