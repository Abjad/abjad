from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval


def test_BoundedInterval_magnitude_01():
    '''BoundedInterval magnitude is the high minus the low offset.'''
    i = BoundedInterval(3, 23)
    assert (23 - 3) == i.magnitude
