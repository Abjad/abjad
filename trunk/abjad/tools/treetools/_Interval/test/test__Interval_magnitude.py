from abjad.tools.treetools._Interval import _Interval


def test__Interval_magnitude_01( ):
    '''_Interval magnitude is the high minus the low value.'''
    i = _Interval(3, 23)
    assert (23 - 3) == i.magnitude
