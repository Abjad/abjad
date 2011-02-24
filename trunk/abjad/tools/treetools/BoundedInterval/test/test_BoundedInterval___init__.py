import py.test
from abjad.tools.treetools.BoundedInterval import BoundedInterval


def test_BoundedInterval___init___01( ):
   '''High offset must be greater than or equal to low offset.'''
   py.test.raises(AssertionError,
      "i = BoundedInterval(0, -10, 'this should fail.')")

def test_BoundedInterval___init___02( ):
   '''BoundedIntervals cannot be instantiated from floats.'''
   py.test.raises(AssertionError,
      "i = BoundedInterval(0.5, 2.3, 'this should fail.')")

def test_BoundedInterval___init___03( ):
   '''BoundedIntervals can be instantiated from other intervals.'''
   i1 = BoundedInterval(0, 10, 'data')
   i2 = BoundedInterval(i1)
   assert i1.signature == i2.signature
   assert i1 != i2

def test_BoundedInterval___init___04( ):
   '''BoundedIntervals can be instantiated with just a low and high offset.'''
   i = BoundedInterval(0, 10)

def test_BoundedInterval___init___05( ):
   '''BoundedIntervals can be instantiated with 3 non-keyword arguments.'''
   i = BoundedInterval(0, 10, 'data')

def test_BoundedInterval___init___06( ):
   '''BoundedIntervals copy data on instantiation.'''
   data = { }
   i = BoundedInterval(0, 10, data)
   data['cat'] = 'dog'
   assert data != i.data
