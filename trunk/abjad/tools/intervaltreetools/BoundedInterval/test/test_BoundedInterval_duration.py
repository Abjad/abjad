from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval


def test_BoundedInterval_duration_01():
    '''BoundedInterval duration is the stop minus the start offset.'''
    i = BoundedInterval(3, 23)
    assert (23 - 3) == i.duration
