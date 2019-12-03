import pytest

import abjad


def test_MultimeasureRest___setattr___01():

    rest = abjad.MultimeasureRest((1, 4))

    with pytest.raises(AttributeError):
        rest.foo = "bar"
