# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_LilyPondComment_closing_01():
    r'''Test container comments closing.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    string = 'Voice closing comments here.'
    comment = indicatortools.LilyPondComment(string, 'closing')
    attach(comment, voice)
    string = 'More voice closing comments.'
    comment = indicatortools.LilyPondComment(string, 'closing')
    attach(comment, voice)

    assert format(voice) == stringtools.normalize(
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

    assert inspect_(voice).is_well_formed()


def test_indicatortools_LilyPondComment_closing_02():
    r'''Test leaf comments closing.
    '''

    note = Note(0, (1, 8))
    override(note).beam.thickness = 3
    string = 'Leaf closing comments here.'
    comment = indicatortools.LilyPondComment(string, 'closing')
    attach(comment, note)
    string = 'More leaf closing comments.'
    comment = indicatortools.LilyPondComment(string, 'closing')
    attach(comment, note)

    assert format(note) == stringtools.normalize(
        r'''
        \once \override Beam.thickness = #3
        c'8
        % Leaf closing comments here.
        % More leaf closing comments.
        '''
        )

    assert inspect_(note).is_well_formed()
