# -*- encoding: utf-8 -*-
from abjad import *


def test_GraceContainer_parentage_01():
    r'''Lone grace container carrier is none.
    '''

    gracecontainer = containertools.GraceContainer(notetools.make_repeated_notes(4))
    assert gracecontainer._carrier is None


def test_GraceContainer_parentage_02():
    r'''Grace containers bound to leaf do have parent.
    '''

    note = Note(1, (1, 4))
    containertools.GraceContainer()(note)
    assert isinstance(note.grace, containertools.GraceContainer)
    assert note.grace._carrier is note
    assert note.grace._carrier is note


def test_GraceContainer_parentage_03():
    r'''Grace containers bound to leaf have their correct carrier after assignment.
    '''

    note = Note(1, (1, 4))
    containertools.GraceContainer([Note(4, (1, 16))], kind = 'after')(note)
    containertools.GraceContainer([Note(4, (1, 16))], kind = 'grace')(note)
    assert note.after_grace._carrier is note
    assert note.grace._carrier is note
    note.after_grace[:] = []
    notes = [Note("c'8"), Note("d'8")]
    note.after_grace.extend(notes)
    note.grace[:] = []
    notes = [Note("c'8"), Note("d'8")]
    note.grace.extend(notes)
    assert note.after_grace._carrier is note
    assert note.grace._carrier is note
    note.after_grace[:] = []
    note.grace[:] = []
    assert note.after_grace._carrier is note
    assert note.grace._carrier is note
