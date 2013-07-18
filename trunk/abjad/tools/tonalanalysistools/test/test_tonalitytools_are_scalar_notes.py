from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_are_scalar_notes_01():
    '''Notes with the same pitch name are scalar so long
    as pitch numbers differ.'''

    assert tonalanalysistools.are_scalar_notes(Note('c', (1, 4)), Note('cs', (1, 4)))


def test_tonalanalysistools_are_scalar_notes_02():
    '''Notes with the different pitch name are scalar so long
    as they differ by exactly one staff space.'''

    assert tonalanalysistools.are_scalar_notes(Note('c', (1, 4)), Note('d', (1, 4)))
    assert tonalanalysistools.are_scalar_notes(Note('c', (1, 4)), Note('ds', (1, 4)))

    assert tonalanalysistools.are_scalar_notes(Note('c', (1, 4)), Note('b,', (1, 4)))
    assert tonalanalysistools.are_scalar_notes(Note('c', (1, 4)), Note('bf,', (1, 4)))


def test_tonalanalysistools_are_scalar_notes_03():
    '''Notes with the same pitch are not scalar.
    '''

    assert not tonalanalysistools.are_scalar_notes(Note('c', (1, 4)), Note('c', (1, 4)))


def test_tonalanalysistools_are_scalar_notes_04():
    '''Notes separated by more than 1 staff space are not scalar.
    '''

    assert not tonalanalysistools.are_scalar_notes(Note('c', (1, 4)), Note('e', (1, 4)))


def test_tonalanalysistools_are_scalar_notes_05():
    '''Contour changes in note sequence qualifies as nonscalar.
    '''

    notes = notetools.make_notes([0, 2, 4, 5, 4, 2, 0], [(1, 4)])
    t = Staff(notes)

    assert not tonalanalysistools.are_scalar_notes(t)
