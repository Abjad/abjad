# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_LilyPondComment_before_01():
    r'''Test context comments before.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    override(beam).beam.thickness = 3
    string = 'Voice before comments here.'
    comment = indicatortools.LilyPondComment(string, 'before')
    attach(comment, voice)
    string = 'More voice before comments.'
    comment = indicatortools.LilyPondComment(string, 'before')
    attach(comment, voice)

    assert format(voice) == stringtools.normalize(
        r'''
        % Voice before comments here.
        % More voice before comments.
        \new Voice {
            \override Beam.thickness = #3
            c'8 [
            d'8
            e'8
            f'8 ]
            \revert Beam.thickness
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_indicatortools_LilyPondComment_before_02():
    r'''Leaf comments before.
    '''

    note = Note(0, (1, 8))
    override(note).beam.thickness = 3
    string = 'Leaf comments before here.'
    comment = indicatortools.LilyPondComment(string, 'before')
    attach(comment, note)
    string = 'More comments before.'
    comment = indicatortools.LilyPondComment(string, 'before')
    attach(comment, note)

    assert format(note) == stringtools.normalize(
        r'''
        % Leaf comments before here.
        % More comments before.
        \once \override Beam.thickness = #3
        c'8
        '''
        )

    assert inspect_(note).is_well_formed()
