from abjad.tools.treetools._BoundedInterval import _BoundedInterval


def test__BoundedInterval_magnitude_01( ):
    '''_BoundedInterval magnitude is the high minus the low value.'''
    i = _BoundedInterval(3, 23)
    assert (23 - 3) == i.magnitude
