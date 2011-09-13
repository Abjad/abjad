from abjad import *


def test_durtools_Duration___init___01():

    duration = Duration(3, 5)
    assert isinstance(duration, Duration)

    duration = Duration((3, 5))
    assert isinstance(duration, Duration)
