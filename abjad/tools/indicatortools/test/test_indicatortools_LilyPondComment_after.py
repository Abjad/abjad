# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_LilyPondComment_after_01():
    r'''Test context comments after.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    override(beam).beam.thickness = 3
    string = 'Voice after comments here.'
    comment = indicatortools.LilyPondComment(string, 'after')
    attach(comment, voice)
    string = 'More voice after comments.'
    comment = indicatortools.LilyPondComment(string, 'after')
    attach(comment, voice)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \override Beam.thickness = #3
            c'8 [
            d'8
            e'8
            f'8 ]
            \revert Beam.thickness
        }
        % Voice after comments here.
        % More voice after comments.
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_indicatortools_LilyPondComment_after_02():
    r'''Leaf comments after.
    '''

    note = Note(0, (1, 8))
    override(note).beam.thickness = 3
    string = 'Leaf comments after here.'
    comment = indicatortools.LilyPondComment(string, 'after')
    attach(comment, note)
    string = 'More comments after.'
    comment = indicatortools.LilyPondComment(string, 'after')
    attach(comment, note)

    assert format(note) == stringtools.normalize(
        r'''
        \once \override Beam.thickness = #3
        c'8
        % Leaf comments after here.
        % More comments after.
        '''
        )

    assert inspect_(note).is_well_formed()
