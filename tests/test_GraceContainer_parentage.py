import abjad


def test_GraceContainer_parentage_01():
    """
    Lone grace container main leaf is none.
    """

    grace_container = abjad.GraceContainer("c'4 d'4 e'4 f'4")
    assert grace_container._main_leaf is None


def test_GraceContainer_parentage_02():
    """
    Grace containers bound to leaf do have parent.
    """

    note = abjad.Note(1, (1, 4))
    grace_container = abjad.GraceContainer()
    abjad.attach(grace_container, note)
    grace_container = abjad.inspect(note).grace_container()
    assert isinstance(grace_container, abjad.GraceContainer)
    assert grace_container._main_leaf is note
    assert grace_container._main_leaf is note


def test_GraceContainer_parentage_03():
    """
    Grace containers bound to leaf have their correct main leaf after
    assignment.
    """

    note = abjad.Note(1, (1, 4))
    after_grace = abjad.AfterGraceContainer([abjad.Note("e'16")])
    abjad.attach(after_grace, note)
    grace = abjad.GraceContainer([abjad.Note("e'16")])
    abjad.attach(grace, note)
    assert after_grace._main_leaf is note
    assert grace._main_leaf is note
    after_grace[:] = []
    notes = [abjad.Note("c'8"), abjad.Note("d'8")]
    after_grace.extend(notes)
    grace[:] = []
    notes = [abjad.Note("c'8"), abjad.Note("d'8")]
    grace.extend(notes)
    assert after_grace._main_leaf is note
    assert grace._main_leaf is note
    after_grace[:] = []
    grace[:] = []
    assert after_grace._main_leaf is note
    assert grace._main_leaf is note
