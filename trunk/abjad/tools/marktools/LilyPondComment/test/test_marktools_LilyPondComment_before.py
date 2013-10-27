# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_LilyPondComment_before_01():
    r'''Test context comments before.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])
    beam.override.beam.thickness = 3
    comment = marktools.LilyPondComment('Voice before comments here.', 'before')
    comment.attach(voice)
    comment = marktools.LilyPondComment('More voice before comments.', 'before')
    comment.attach(voice)

    assert testtools.compare(
        voice,
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

    assert inspect(voice).is_well_formed()


def test_marktools_LilyPondComment_before_02():
    r'''Leaf comments before.
    '''

    note = Note(0, (1, 8))
    note.override.beam.thickness = 3
    comment = marktools.LilyPondComment('Leaf comments before here.', 'before')
    comment.attach(note)
    comment = marktools.LilyPondComment('More comments before.', 'before')
    comment.attach(note)

    assert testtools.compare(
        note,
        r'''
        % Leaf comments before here.
        % More comments before.
        \once \override Beam #'thickness = #3
        c'8
        '''
        )

    assert inspect(note).is_well_formed()
