from abjad import *
import types

def test_listtools_phasor_01( ):
   '''phasor( ) defaults to positive 1 step and start index 0.'''   

   l = [1, 2, 3, 4, 5, 6, 7]
   t = listtools.phasor(l)

   assert isinstance(t, types.GeneratorType)
   for i in range(20):
      assert t.next( ) == l[i % len(l)]


def test_listtools_phasor_02( ):
   '''phase can be > 1.'''

   l = [1, 2, 3, 4, 5, 6, 7]
   t = listtools.phasor(l, 2, length = 20)

   assert list(t) == [1,3,5,7,2,4,6,1,3,5,7,2,4,6,1,3,5,7,2,4]


def test_listtools_phasor_03( ):
   '''start index can be other than 0.'''

   l = [1, 2, 3, 4, 5, 6, 7]
   t = listtools.phasor(l, 2, 3, length = 20)

   assert list(t) == [4,6,1,3,5,7,2,4,6,1,3,5,7,2,4,6,1,3,5,7]


def test_listtools_phasor_04( ):
   '''phase can be negative.'''

   l = [1, 2, 3, 4, 5, 6, 7]
   t = listtools.phasor(l, -2, 5, length = 20)

   assert list(t) == [6,4,2,7,5,3,1,6,4,2,7,5,3,1,6,4,2,7,5,3]


