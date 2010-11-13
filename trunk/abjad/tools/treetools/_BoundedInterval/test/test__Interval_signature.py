from abjad.tools.treetools._BoundedInterval import _BoundedInterval


def test__BoundedInterval_signature_01( ):
    i = _BoundedInterval(0, 10, 'hello world!')
    assert i.signature == (0, 10)


def test__BoundedInterval_signature_02( ):
    i = _BoundedInterval(-30, 3, 'hellow world!')
    assert i.signature == (-30, 3)
