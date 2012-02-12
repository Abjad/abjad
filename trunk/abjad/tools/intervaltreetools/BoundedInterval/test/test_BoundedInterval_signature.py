from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval


def test_BoundedInterval_signature_01():
    i = BoundedInterval(0, 10, {'hello': 'world!'})
    assert i.signature == (0, 10)


def test_BoundedInterval_signature_02():
    i = BoundedInterval(-30, 3, {'helstart': 'world!'})
    assert i.signature == (-30, 3)
