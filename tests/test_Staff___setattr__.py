import abjad
import pytest


def test_Staff___setattr___01():
    """
    Slots constrain staff attributes.
    """

    staff = abjad.Staff([])

    with pytest.raises(AttributeError):
        staff.foo = "bar"
