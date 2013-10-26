# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondComment_after_01():
    r'''Test context comments after.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])
    beam.override.beam.thickness = 3
    comment = marktools.LilyPondComment('Voice after comments here.', 'after')
    comment.attach(voice)
    comment = marktools.LilyPondComment('More voice after comments.', 'after')
    comment.attach(voice)

    assert testtools.compare(
        voice,
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

    assert inspect(voice).is_well_formed()


def test_LilyPondComment_after_02():
    r'''Leaf comments after.
    '''

    note = Note(0, (1, 8))
    note.override.beam.thickness = 3
    comment = marktools.LilyPondComment('Leaf comments after here.', 'after')
    comment.attach(note)
    comment = marktools.LilyPondComment('More comments after.', 'after')
    comment.attach(note)

    assert testtools.compare(
        note,
        r'''
        \once \override Beam #'thickness = #3
        c'8
        % Leaf comments after here.
        % More comments after.
        '''
        )

    assert inspect(note).is_well_formed()
