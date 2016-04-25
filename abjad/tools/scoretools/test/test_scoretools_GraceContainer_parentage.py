# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_GraceContainer_parentage_01():
    r'''Lone grace container carrier is none.
    '''

    gracecontainer = scoretools.GraceContainer("c'4 d'4 e'4 f'4")
    assert gracecontainer._carrier is None


def test_scoretools_GraceContainer_parentage_02():
    r'''Grace containers bound to leaf do have parent.
    '''

    note = Note(1, (1, 4))
    grace_container = scoretools.GraceContainer()
    attach(grace_container, note)
    grace_container = inspect_(note).get_grace_container()
    assert isinstance(grace_container, scoretools.GraceContainer)
    assert grace_container._carrier is note
    assert grace_container._carrier is note


def test_scoretools_GraceContainer_parentage_03():
    r'''Grace containers bound to leaf have their correct carrier
    after assignment.
    '''

    note = Note(1, (1, 4))
    after_grace = scoretools.GraceContainer([Note("e'16")], kind='after')
    attach(after_grace, note)
    grace = scoretools.GraceContainer([Note("e'16")], kind='grace')
    attach(grace, note)
    assert after_grace._carrier is note
    assert grace._carrier is note
    after_grace[:] = []
    notes = [Note("c'8"), Note("d'8")]
    after_grace.extend(notes)
    grace[:] = []
    notes = [Note("c'8"), Note("d'8")]
    grace.extend(notes)
    assert after_grace._carrier is note
    assert grace._carrier is note
    after_grace[:] = []
    grace[:] = []
    assert after_grace._carrier is note
    assert grace._carrier is note
