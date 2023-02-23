import pytest

import abjad


def test_Tuplet___setattr___01():
    """
    Slots constrain tuplet attributes.
    """

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")

    with pytest.raises(AttributeError):
        tuplet.foo = "bar"
