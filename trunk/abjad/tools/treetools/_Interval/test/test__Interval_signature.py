from abjad.tools.treetools._Interval import _Interval


def test__Interval_signature_01( ):
    i = _Interval(0, 10, 'hello world!')
    assert i.signature == (0, 10)


def test__Interval_signature_02( ):
    i = _Interval(-30, 3, 'hellow world!')
    assert i.signature == (-30, 3)
