# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondComment_opening_01():
    r'''Opening comments in container.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    marktools.LilyPondComment('Voice opening comments here.', 'opening')(voice)
    marktools.LilyPondComment('More voice opening comments.', 'opening')(voice)

    r'''
    \new Voice {
        % Voice opening comments here.
        % More voice opening comments.
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            % Voice opening comments here.
            % More voice opening comments.
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )


def test_LilyPondComment_opening_02():
    r'''Opening comments on leaf.
    '''

    t = Note(0, (1, 8))
    t.override.beam.thickness = 3
    marktools.LilyPondComment('Leaf opening comments here.', 'opening')(t)
    marktools.LilyPondComment('More leaf opening comments.', 'opening')(t)

    r'''
    \once \override Beam #'thickness = #3
    % Leaf opening comments here.
    % More leaf opening comments.
    c'8
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \once \override Beam #'thickness = #3
        % Leaf opening comments here.
        % More leaf opening comments.
        c'8
        '''
        )
