from abjad.tools.treetools import BoundedInterval


def test_BoundedInterval___eq___01( ):
   a = BoundedInterval(0, 10)
   b = BoundedInterval(0, 10)
   assert a == b


def test_BoundedInterval___eq__02( ):
   a = BoundedInterval(0, 10)
   b = BoundedInterval(-1, 10)
   assert a != b


def test_BoundedInterval___eq__03( ):
   a = BoundedInterval(0, 10)
   b = BoundedInterval(0, 11)
   assert a != b


def test_BoundedInterval___eq__04( ):
   a = BoundedInterval(0, 10)
   b = BoundedInterval(0, 10, { })
   assert a == b


def test_BoundedInterval___eq__05( ):
   a = BoundedInterval(0, 10)
   b = BoundedInterval(0, 10, 'duck')
   assert a != b
