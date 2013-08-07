# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondComment_after_01():
    r'''Test context comments after.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(voice[:])
    beam.override.beam.thickness = 3
    marktools.LilyPondComment('Voice after comments here.', 'after')(voice)
    marktools.LilyPondComment('More voice after comments.', 'after')(voice)

    r'''
    \new Voice {
        \override Beam #'thickness = #3
        c'8 [
        d'8
        e'8
        f'8 ]
        \revert Beam #'thickness
    }
    % Voice after comments here.
    % More voice after comments.'''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            \override Beam #'thickness = #3
            c'8 [
            d'8
            e'8
            f'8 ]
            \revert Beam #'thickness
        }
        % Voice after comments here.
        % More voice after comments.
        '''
        )


def test_LilyPondComment_after_02():
    r'''Leaf comments after.
    '''

    note = Note(0, (1, 8))
    note.override.beam.thickness = 3
    marktools.LilyPondComment('Leaf comments after here.', 'after')(note)
    marktools.LilyPondComment('More comments after.', 'after')(note)

    r'''
    \once \override Beam #'thickness = #3
    c'8
    % Leaf comments after here.
    % More comments after.'''

    assert select(note).is_well_formed()
    assert testtools.compare(
        note.lilypond_format,
        r'''
        \once \override Beam #'thickness = #3
        c'8
        % Leaf comments after here.
        % More comments after.
        '''
        )
