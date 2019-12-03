import pytest

import abjad


def test_Rest___setattr___01():
    """
    Slots constrain rest attributes.
    """

    rest = abjad.Rest((1, 4))

    with pytest.raises(AttributeError):
        rest.foo = "bar"
