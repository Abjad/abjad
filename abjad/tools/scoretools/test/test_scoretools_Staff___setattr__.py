import abjad
import pytest


def test_scoretools_Staff___setattr___01():
    """
    Slots constrain staff attributes.
    """

    staff = abjad.Staff([])

    assert pytest.raises(AttributeError, "staff.foo = 'bar'")
