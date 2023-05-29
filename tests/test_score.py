import pytest

import abjad


def test_score_01():
    """
    Slots constrain component attributes.
    """

    for component in (
        abjad.MultimeasureRest((1, 4)),
        abjad.Chord("<ef' cs' f''>4"),
        abjad.Container(),
        abjad.Context(),
        abjad.Note("c'4"),
        abjad.NoteHead("cs''"),
        abjad.Rest((1, 4)),
        abjad.Score(),
        abjad.Skip((1, 4)),
        abjad.Staff(),
        abjad.Tuplet((2, 3), "c'8 d'8 e'8"),
        abjad.Voice(),
    ):
        with pytest.raises(AttributeError):
            component.foo = "bar"
