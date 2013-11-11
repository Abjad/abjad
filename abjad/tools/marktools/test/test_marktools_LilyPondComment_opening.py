# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_LilyPondComment_opening_01():
    r'''Opening comments in container.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    comment = marktools.LilyPondComment('Voice opening comments here.', 'opening')
    attach(comment, voice)
    comment = marktools.LilyPondComment('More voice opening comments.', 'opening')
    attach(comment, voice)

    assert systemtools.TestManager.compare(
        voice,
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

    assert inspect(voice).is_well_formed()


def test_marktools_LilyPondComment_opening_02():
    r'''Opening comments on leaf.
    '''

    note = Note(0, (1, 8))
    override(note).beam.thickness = 3
    comment = marktools.LilyPondComment('Leaf opening comments here.', 'opening')
    attach(comment, note)
    comment = marktools.LilyPondComment('More leaf opening comments.', 'opening')
    attach(comment, note)

    assert systemtools.TestManager.compare(
        note,
        r'''
        \once \override Beam #'thickness = #3
        % Leaf opening comments here.
        % More leaf opening comments.
        c'8
        '''
        )

    assert inspect(note).is_well_formed()
