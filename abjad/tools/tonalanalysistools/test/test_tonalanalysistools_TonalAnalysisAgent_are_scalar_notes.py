# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_TonalAnalysisAgent_are_scalar_notes_01():
    r'''Notes with the same pitch name are scalar so long
    as pitch numbers differ.
    '''

    notes = [abjad.Note('c', (1, 4)), abjad.Note('cs', (1, 4))]
    selection = abjad.analyze(notes)
    assert selection.are_scalar_notes()


def test_tonalanalysistools_TonalAnalysisAgent_are_scalar_notes_02():
    r'''Notes with different pitch names are scalar so long
    as they differ by exactly one staff space.
    '''

    notes = [abjad.Note('c', (1, 4)), abjad.Note('d', (1, 4))]
    selection = abjad.analyze(notes)
    assert selection.are_scalar_notes()

    notes = [abjad.Note('c', (1, 4)), abjad.Note('ds', (1, 4))]
    selection = abjad.analyze(notes)
    assert selection.are_scalar_notes()

    notes = [abjad.Note('c', (1, 4)), abjad.Note('b,', (1, 4))]
    selection = abjad.analyze(notes)
    assert selection.are_scalar_notes()

    notes = [abjad.Note('c', (1, 4)), abjad.Note('bf,', (1, 4))]
    selection = abjad.analyze(notes)
    assert selection.are_scalar_notes()


def test_tonalanalysistools_TonalAnalysisAgent_are_scalar_notes_03():
    r'''abjad.Notes with the same pitch are not scalar.
    '''

    notes = [abjad.Note('c', (1, 4)), abjad.Note('c', (1, 4))]
    selection = abjad.analyze(notes)
    assert not selection.are_scalar_notes()


def test_tonalanalysistools_TonalAnalysisAgent_are_scalar_notes_04():
    r'''abjad.Notes separated by more than 1 staff space are not scalar.
    '''

    notes = [abjad.Note('c', (1, 4)), abjad.Note('e', (1, 4))]
    selection = abjad.analyze(notes)
    assert not selection.are_scalar_notes()


def test_tonalanalysistools_TonalAnalysisAgent_are_scalar_notes_05():
    r'''Contour changes in note sequence qualifies as nonscalar.
    '''

    maker = abjad.NoteMaker()
    notes = maker([0, 2, 4, 5, 4, 2, 0], [(1, 4)])
    selection = abjad.analyze(notes)
    assert not selection.are_scalar_notes()
