# -*- encoding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_TonalAnalysisAgent_are_scalar_notes_01():
    r'''Notes with the same pitch name are scalar so long
    as pitch numbers differ.
    '''

    notes = [Note('c', (1, 4)), Note('cs', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert selection.are_scalar_notes()


def test_tonalanalysistools_TonalAnalysisAgent_are_scalar_notes_02():
    r'''Notes with different pitch names are scalar so long
    as they differ by exactly one staff space.
    '''

    notes = [Note('c', (1, 4)), Note('d', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert selection.are_scalar_notes()

    notes = [Note('c', (1, 4)), Note('ds', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert selection.are_scalar_notes()

    notes = [Note('c', (1, 4)), Note('b,', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert selection.are_scalar_notes()

    notes = [Note('c', (1, 4)), Note('bf,', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert selection.are_scalar_notes()


def test_tonalanalysistools_TonalAnalysisAgent_are_scalar_notes_03():
    r'''Notes with the same pitch are not scalar.
    '''

    notes = [Note('c', (1, 4)), Note('c', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert not selection.are_scalar_notes()


def test_tonalanalysistools_TonalAnalysisAgent_are_scalar_notes_04():
    r'''Notes separated by more than 1 staff space are not scalar.
    '''

    notes = [Note('c', (1, 4)), Note('e', (1, 4))]
    selection = tonalanalysistools.select(notes)
    assert not selection.are_scalar_notes()


def test_tonalanalysistools_TonalAnalysisAgent_are_scalar_notes_05():
    r'''Contour changes in note sequence qualifies as nonscalar.
    '''

    notes = scoretools.make_notes([0, 2, 4, 5, 4, 2, 0], [(1, 4)])
    selection = tonalanalysistools.select(notes)
    assert not selection.are_scalar_notes()