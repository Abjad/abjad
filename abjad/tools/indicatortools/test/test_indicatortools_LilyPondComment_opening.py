# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_LilyPondComment_opening_01():
    r'''Opening comments in container.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    string = 'Voice opening comments here.'
    comment = indicatortools.LilyPondComment(string, 'opening')
    attach(comment, voice)
    string = 'More voice opening comments.'
    comment = indicatortools.LilyPondComment(string, 'opening')
    attach(comment, voice)

    assert format(voice) == stringtools.normalize(
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

    assert inspect_(voice).is_well_formed()


def test_indicatortools_LilyPondComment_opening_02():
    r'''Opening comments on leaf.
    '''

    note = Note(0, (1, 8))
    override(note).beam.thickness = 3
    string = 'Leaf opening comments here.'
    comment = indicatortools.LilyPondComment(string, 'opening')
    attach(comment, note)
    string = 'More leaf opening comments.'
    comment = indicatortools.LilyPondComment(string, 'opening')
    attach(comment, note)

    assert format(note) == stringtools.normalize(
        r'''
        \once \override Beam.thickness = #3
        % Leaf opening comments here.
        % More leaf opening comments.
        c'8
        '''
        )

    assert inspect_(note).is_well_formed()
