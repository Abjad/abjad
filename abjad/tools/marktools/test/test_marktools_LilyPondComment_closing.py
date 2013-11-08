# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_LilyPondComment_closing_01():
    r'''Test container comments closing.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    comment = marktools.LilyPondComment('Voice closing comments here.', 'closing')
    attach(comment, voice)
    comment = marktools.LilyPondComment('More voice closing comments.', 'closing')
    attach(comment, voice)

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

    assert inspect(voice).is_well_formed()


def test_marktools_LilyPondComment_closing_02():
    r'''Test leaf comments closing.
    '''

    note = Note(0, (1, 8))
    override(note).beam.thickness = 3
    comment = marktools.LilyPondComment('Leaf closing comments here.', 'closing')
    attach(comment, note)
    comment = marktools.LilyPondComment('More leaf closing comments.', 'closing')
    attach(comment, note)

    assert testtools.compare(
        note,
        r'''
        \once \override Beam #'thickness = #3
        c'8
        % Leaf closing comments here.
        % More leaf closing comments.
        '''
        )

    assert inspect(note).is_well_formed()
