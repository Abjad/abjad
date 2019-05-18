import abjad


def test_Skip__str___01():

    skip = abjad.Skip((1, 4))

    assert str(skip) == "s4"
